import os
import threading

from google.cloud import vision

project_id = os.environ["essential-text-330923"]


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


def main(bucket, filenames):
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
    print("Batch processing complete.")




if __name__ == '__main__':
    main()
