import base64
import json


def pack_message(image, filename):
    # Convert the image to a string in base64 format
    image_str = base64.b64encode(image).decode('ascii')

    # Package the image along with other arguments
    message = {'image': image_str,
               'filename': filename}

    # Convert the complete package into a binary object containing JSON
    return json.dumps(message).encode('utf-8')


def unpack_message(event):
    # Unpack the binary JSON object
    message_data = base64.b64decode(event["data"])
    message = json.loads(message_data.decode("utf-8"))

    image_str = message['image']

    # Get the image from the coded string
    image = base64.b64decode(image_str.encode('ascii'))

    return image, message['filename']


def extract_args_http(request):
    data = request.get_json(silent=True)['data']

    return data['filenames'], data['is_processing_on']
