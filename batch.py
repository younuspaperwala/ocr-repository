import threading
import os

from google.cloud import storage, pubsub

from message import pack_message, topic_res_name


def select_publish_topic(is_processing_on):
    topic_id = 'ocr-process-pickup' if is_processing_on \
        else 'ocr_detection_pickup'

    return topic_res_name(topic_id)


def load_input(filename):
    bucket = os.getenv('BUCKET')

    return storage.Client().get_bucket(bucket) \
        .blob(f"img/{filename}") \
        .download_as_bytes()


def handle_image(filename, is_processing_on):
    # Load image from bucket
    image = load_input(filename)

    # Pack image and arguments into a message data object
    message_data = pack_message(image, filename)

    pubsub.PublisherClient().publish(topic=select_publish_topic(is_processing_on),
                                     data=message_data)


def start_batch(filenames, is_processing_on):
    # Create threads to process batch
    threads = [threading.Thread(target=handle_image,
                                args=(filename, is_processing_on))
               for filename in filenames]

    # Start threads
    for thread in threads:
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

    # Complete
    return "All calls batched to image step."
