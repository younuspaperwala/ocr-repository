import base64
import json
import os


def pack_message(image, filename, approach):
    # Convert the image to a string in base64 format
    content_str = base64.b64encode(image).decode('ascii')

    return pack_text_message(content_str, filename, approach)


def unpack_message(event):
    content_str, filename, approach = unpack_text_message(event)

    # Get the image from the coded string
    image = base64.b64decode(content_str.encode('ascii'))

    return image, filename, approach


def pack_text_message(text, filename, approach):
    message = {'content': text,
               'filename': filename,
               'approach': approach}

    # Convert the complete package into a binary object containing JSON
    return json.dumps(message).encode('utf-8')


def unpack_text_message(event):
    # Unpack the binary JSON object
    message_data = base64.b64decode(event["data"])
    message = json.loads(message_data.decode("utf-8"))

    return message['content'], message['filename'], message['approach']


def extract_args_http(request):
    data = request.get_json(silent=True)['data']

    approach = data['approach'] if ('approach' in data) and data['is_processing_on'] else {}

    return data['filenames'], data['is_processing_on'], approach


def topic_res_name(topic_id):
    project = os.getenv('PROJECT')

    return f"projects/{project}/topics/{topic_id}"
