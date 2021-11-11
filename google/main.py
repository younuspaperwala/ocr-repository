import batch
import detect
import message as msg
import process


# Request format may be specific to Google
def batch_entry(request):
    return batch.start_batch(
        *msg.extract_args_http(request))


def process_entry(event, context):
    return process.process_publish(
        *msg.unpack_message(event))


def detect_entry(event, context):
    return detect.run_ocr(
        *msg.unpack_message(event))
