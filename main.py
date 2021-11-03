import threading
from google.cloud import vision, storage


def extract_arguments(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'bucket' in request_json and 'filenames' in request_json:
        bucket = request_json['bucket']
        filenames = request_json['filenames']
    elif request_args and 'bucket' in request_args and 'filenames' in request_json:
        bucket = request_args['bucket']
        filenames = request_args['filenames']

    return bucket, filenames


def text_detection(client, bucket, filename):
    image = vision.Image({'source': {'image_uri': f"gs://{bucket}/img/{filename}"}})
    text_detection_response = client.text_detection(image=image)
    annotations = text_detection_response.text_annotations

    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ""

    return text


def store_output(client, bucket_name, filename, text):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(f"output/{filename}.txt")
    blob.upload_from_string(text)


def process_one_image(bucket, filename):
    print(f"Instantiating clients for {filename}.")
    vision_client = vision.ImageAnnotatorClient()
    storage_client = storage.Client()

    print(f"Looking for text in {filename}.")
    text = text_detection(vision_client, bucket, filename)
    print(f"Extracted text {text} ({len(text)} chars) from {filename}.")

    print(f"Storing text in output file")
    store_output(storage_client, bucket, filename, text)


def main(request):
    # Extract the arguments
    bucket, filenames = extract_arguments(request)

    # Create threads to process batch
    threads = [threading.Thread(target=process_one_image, args=(bucket, filename))
               for filename in filenames]

    # Start threads
    for thread in threads:
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

    # Complete
    return "Batch processing complete."
