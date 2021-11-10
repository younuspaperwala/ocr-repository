import json
import os

from google.cloud import vision, storage


def text_detection(image):
    # Call Vision API
    text_detection_response = vision.ImageAnnotatorClient().text_detection(image=image)

    # Export as JSON string
    text_json = json.dumps(text_detection_response)

    return text_json


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


