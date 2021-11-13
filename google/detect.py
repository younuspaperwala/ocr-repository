from functools import reduce

from google.cloud import vision, pubsub
from google.cloud.vision_v1 import EntityAnnotation

from message import topic_res_name, pack_text_message


def format_response(text_detection_response):
    text_json_list = [EntityAnnotation.to_json(a)
                      for a in text_detection_response.text_annotations]

    if not text_json_list:
        return '[]'

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


def run_ocr(image, filename, approach):
    # Package the image in a request format for Google Vision
    request_image = {'content': image}

    # Detect the text
    text = text_detection(request_image)

    # Re-package the image and arguments and publish to Pub/Sub
    message = pack_text_message(text, filename, approach)
    publish(message)

    return "Detected text and published to next step."
