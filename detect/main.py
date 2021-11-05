import base64
import json

from google.cloud import vision, storage


def pack_message(image, bucket, filename):
    message = {'image': base64.b64encode(image),
               'bucket': bucket,
               'filename': filename}

    return json.dumps(message).encode('utf-8')


def unpack_message(event):
    message_data = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(message_data)

    image = base64.b64decode(message['image'])

    return image, message['bucket'], message['filename']


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
    image, bucket, filename = unpack_message(event)

    # Package the image in a request format for Google Vision
    request_image = {'content': image}

    # Detect the text
    text = text_detection(request_image)

    # Store the text in an output file
    store_output(bucket, filename, text)


