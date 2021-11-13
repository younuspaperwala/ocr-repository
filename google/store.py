import json
import os

from google.cloud import storage


def store_output(text, filename, approach):
    is_processing_on = True if json.loads(approach) else False

    bucket = os.getenv('BUCKET')

    return storage.Client() \
        .get_bucket(bucket) \
        .blob(f"output/{filename}_{is_processing_on}.txt") \
        .upload_from_string(text)
