from functools import reduce

from google.cloud import vision
from google.cloud.vision_v1 import EntityAnnotation

from store import store_output


def format_response(text_detection_response):
    text_json_list = [EntityAnnotation.to_json(a)
                      for a in text_detection_response.text_annotations]

    return '[\n' + reduce(lambda a, b: a + ',\n' + b, text_json_list) + '\n]'


def text_detection(image):
    # Call Vision API
    text_detection_response = vision.ImageAnnotatorClient().text_detection(image=image)

    # Export as JSON string
    return format_response(text_detection_response)


def run_ocr(image, filename):
    # Package the image in a request format for Google Vision
    request_image = {'content': image}

    # Detect the text
    text = text_detection(request_image)

    # Store the output
    print(filename)
    store_output(text, filename)

    return "Detected text and published to next step."
