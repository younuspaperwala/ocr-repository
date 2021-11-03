import threading
from google.cloud import vision


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


def text_detection(bucket, filename):
    print(f"Instantiating client for {filename}.")
    client = vision.ImageAnnotatorClient()

    print(f"Looking for text in {filename}.")
    image = vision.Image({'source': {'image_uri': f"gs://{bucket}/{filename}"}})
    text_detection_response = client.text_detection(image=image)
    annotations = text_detection_response.text_annotations

    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ""
    print(f"Extracted text {text} ({len(text)} chars) from {filename}.")


def main(request):
    # Extract the arguments
    bucket, filenames = extract_arguments(request)

    # Create threads to process batch
    threads = [threading.Thread(target=text_detection, args=(bucket, filename))
               for filename in filenames]

    # Start threads
    for thread in threads:
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

    # Complete
    return "Batch processing complete."
