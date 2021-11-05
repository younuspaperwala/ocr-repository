from google.cloud import vision, storage

import message_packing.message_packing as mp


def text_detection(image):
    # Call Vision API
    text_detection_response = vision.ImageAnnotatorClient().text_detection(image=image)

    # Extract needed data from response
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ""

    return text


def store_output(bucket, filename, text):
    storage.Client() \
        .get_bucket(bucket) \
        .blob(f"output/{filename}.txt") \
        .upload_from_string(text)


def run_ocr(event):
    # Extract the image and arguments from the message
    image, bucket, filename = mp.unpack_message(event)

    # Package the image in a request format for Google Vision
    request_image = {'content': image}

    # Detect the text
    text = text_detection(request_image)

    # Store the text in an output file
    store_output(bucket, filename, text)


