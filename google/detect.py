from functools import reduce
import os

from google.cloud import vision, storage, pubsub
from google.cloud.vision_v1 import EntityAnnotation

from message import topic_res_name


def format_response(text_detection_response):
    text_json_list = [EntityAnnotation.to_json(a)
                      for a in text_detection_response.text_annotations]

    return '[\n' + reduce(lambda a, b: a + ',\n' + b, text_json_list) + '\n]'


def text_detection(image):
    # Call Vision API
    text_detection_response = vision.ImageAnnotatorClient().text_detection(image=image)

    # Export as JSON string
    return format_response(text_detection_response)


def publish(message):
    pubsub.PublisherClient() \
        .publish(topic=topic_res_name('ocr-store-pickup'),
                 data=message)


def store_output(filename, text):
    bucket = os.getenv('BUCKET')

    return storage.Client() \
        .get_bucket(bucket) \
        .blob(f"output/{filename}.txt") \
        .upload_from_string(text)


def run_ocr(image, filename):
    # Package the image in a request format for Google Vision
    request_image = {'content': image}

    # Detect the text
    text = text_detection(request_image)

    # Store the text in an output file
    store_output(filename, text)

    return "Stored OCR text."
