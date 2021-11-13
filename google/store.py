import json
import os

from google.cloud import storage


def store_output(text, filename, approach):
    bucket = os.getenv('BUCKET')

    return storage.Client() \
        .get_bucket(bucket) \
        .blob(f"output/{filename}.txt") \
        .upload_from_string(text)
