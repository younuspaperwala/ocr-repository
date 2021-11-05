from google.cloud import pubsub

import message_packing.message_packing as mp


def process_image(image):
    """
    Add image processing steps here!!
    """

    return image


def process_publish(event):
    # Extract the image and arguments from the message
    image, bucket, filename = mp.unpack_message(event)

    # Process the image
    processed_image = process_image(image)

    # Re-package the image and arguments and publish to Pub/Sub
    message = mp.pack_message(processed_image, bucket, filename)
    pubsub.PublisherClient().publish(topic='ocr-detection-pickup',
                                     data=message)
