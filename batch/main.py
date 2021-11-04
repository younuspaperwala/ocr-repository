import threading

from google.cloud import storage, pubsub

from message_package import pack_message


# Request format may be specific to Google
def extract_arguments(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    print(request_json)
    print(request_args)

    has_all_args = lambda args: all(a in args for a in ('bucket', 'filenames', 'is_processing_on'))

    if request_json and has_all_args(request_json):
        bucket = request_json['bucket']
        filenames = request_json['filenames']
        is_processing_on = request_json['is_processing_on']
    elif request_args and has_all_args(request_args):
        bucket = request_json['bucket']
        filenames = request_json['filenames']
        is_processing_on = request_json['is_processing_on']
    else:
        print("Default hard-coded values used because json extraction failed.")
        bucket = 'ocr-orionlowy'
        filenames = ["00_00.jpg", "00_01.jpg", "00_02.jpg", "00_03.jpg", "00_04.jpg"]
        is_processing_on = True

    return bucket, filenames, is_processing_on


def select_publish_topic(is_processing_on):
    return 'ocr-process-pickup' if is_processing_on \
        else 'ocr_detection_pickup'


def load_image(bucket, filename):
    client = storage.Client()
    return client.get_bucket(bucket) \
        .blob(filename) \
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
