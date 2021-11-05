import threading

from google.cloud import storage, pubsub

from message.message import message as mp


# Request format may be specific to Google
def extract_arguments(request):
    data = request.get_json(silent=True)['data']

    return data['bucket'], data['filenames'], data['is_processing_on']


def select_publish_topic(is_processing_on):
    return 'ocr-process-pickup' if is_processing_on \
        else 'ocr_detection_pickup'


def load_and_publish(bucket, filename, is_processing_on):
    # Load image from bucket
    image = storage.Client().get_bucket(bucket) \
        .blob(f"img/{filename}") \
        .download_as_bytes()

    # Pack image and arguments into a message data object
    message_data = mp.pack_message(image, bucket, filename)

    pubsub.PublisherClient().publish(topic=select_publish_topic(is_processing_on),
                                     data=message_data)


def start_batch(request):
    # Extract the arguments
    bucket, filenames, is_processing_on = extract_arguments(request)

    # Create threads to process batch
    threads = [threading.Thread(target=load_and_publish,
                                args=(bucket, filename, is_processing_on))
               for filename in filenames]

    # Start threads
    for thread in threads:
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

    # Complete
    return "All calls batched to image step."
