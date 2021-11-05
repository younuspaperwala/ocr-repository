from google.cloud import pubsub

from message import pack_message, topic_res_name


def process_image(image):
    """
    Add image processing steps here!!
    """

    return image


def publish(message):
    pubsub.PublisherClient() \
        .publish(topic=topic_res_name('ocr_detection_pickup'),
                 data=message)


def process_publish(image, filename):
    # Process the image
    processed_image = process_image(image)

    # Re-package the image and arguments and publish to Pub/Sub
    message = pack_message(processed_image, filename)
    publish(message)

    return "Ran processing and published to next step."
