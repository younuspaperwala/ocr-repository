import base64
import json


def pack_message(image, bucket, filename):
    message = {'image': base64.b64encode(image),
               'bucket': bucket,
               'filename': filename}

    return json.dumps(message).encode('utf-8')


def unpack_message(event):
    message_data = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(message_data)

    image = base64.b64decode(message['image'])

    return image, message['bucket'], message['filename']


def extract_args_http(request):
    data = request.get_json(silent=True)['data']

    return data['bucket'], data['filenames'], data['is_processing_on']