import threading

from google.cloud import storage, pubsub

from message_package import pack_message


# Request format may be specific to Google
def extract_arguments(request):
    request_json = request.get_json(silent=True)

    return request_json['bucket'], request_json['filenames'], request_json['is_processing_on']


def select_publish_topic(is_processing_on):
    return 'ocr-process-pickup' if is_processing_on \
        else 'ocr_detection_pickup'


def load_image(bucket, filename):
    client = storage.Client()
    return client.get_bucket(bucket) \
        .blob(f"img/{filename}") \
        .download_as_bytes()


def load_and_publish(bucket, filename, is_processing_on):
    # Load image from bucket
    image = load_image(bucket, filename)

    # Pack image and arguments into a message data object
    message_data = pack_message(image, bucket, filename)

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
