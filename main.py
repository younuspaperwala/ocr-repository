import batch
import process
import detect


def batch_entry(request):
    return batch.start_batch(request)


def process_entry(event):
    return process.process_publish(event)


def detect_entry(event):
    return detect.run_ocr(event)
