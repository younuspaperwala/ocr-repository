import os

from google.cloud import pubsub

from message import pack_message


def process_image(image):
    """
    Add image processing steps here!!
    """

    return image


def publish(message):
    project = os.getenv('PROJECT')
    topic_id = 'ocr_detection_pickup'

    topic_res_name = f"projects/{project}/topics/{topic_id}"

    pubsub.PublisherClient().publish(topic=topic_res_name,
                                     data=message)


def process_publish(image, filename):
    # Process the image
    processed_image = process_image(image)

    # Re-package the image and arguments and publish to Pub/Sub
    message = pack_message(processed_image, filename)
    publish(message)

    return "Ran processing and published to next step."
