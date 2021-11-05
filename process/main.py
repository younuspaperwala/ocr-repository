import base64
import json

from google.cloud import pubsub


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


def process_image(image):
    """
    Add image processing steps here!!
    """

    return image


def process_publish(event):
    # Extract the image and arguments from the message
    image, bucket, filename = unpack_message(event)

    # Process the image
    processed_image = process_image(image)

    # Re-package the image and arguments and publish to Pub/Sub
    message = pack_message(processed_image, bucket, filename)
    pubsub.PublisherClient().publish(topic='ocr-detection-pickup',
                                     data=message)
