import base64
import json

from altchars import base64_altchars


def pack_message(image, bucket, filename):
    message = {'image': base64.b64encode(image, base64_altchars),
               'bucket': bucket,
               'filename': filename}

    return json.dumps(message).encode('utf-8')


def unpack_message(event):
    message_data = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(message_data)

    image = base64.b64decode(message['image'], base64_altchars)

    return image, message['bucket'], message['filename']
