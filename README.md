OCR Pipeline with swappable image pre-processing
------------------------------------------------

This code runs with Google Cloud Functions. Please see requirements.txt for dependencies from the Google Cloud platform.

The main.py script contains three entry points, one for each of three Google Cloud Functions (defined separately in a .py file of the same name).
* batch: triggered by HTTP request. Loads images from storage bucket and fans them out into threads.
* process: triggered by Pub/Sub message. Runs custom image pre-processing (*currently does nothing*)
* detect: triggered by Pub/Sub message. Sends images to Vision API for OCR and stores detected text in bucket.

The code is configured to reference several platform-specific and implementation-specific details:
* Argument and data structure formats for Google Cloud services such as Pub/Sub, Storage, and Vision.
* *Environment variables*. Other implementations should set these up on the serverless compute unit's settings.
* Names of message-passing topics and storage buckets.



