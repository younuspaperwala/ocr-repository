from google.cloud import pubsub
import numpy as np
import cv2

from message import pack_message, topic_res_name

processing_param_sets = {'A':
                             {"morph_kernel_size": 3,
                              "gauss_kernel_size": 5,
                              "thresh_window_size": 11,
                              "thresh_C": 2,
                              "rgb_threshold": False,
                              "debug": False},
                         'B':
                             {"morph_kernel_size": 3,
                              "gauss_kernel_size": 5,
                              "thresh_window_size": 11,
                              "thresh_C": 2,
                              "rgb_threshold": True,
                              "debug": False},
                         }


def cv_import(image):
    np_image = np.frombuffer(image, dtype=np.uint8)
    return cv2.imdecode(np_image, cv2.IMREAD_UNCHANGED)


def cv_export(processed_cv_image):
    return cv2.imencode('.png', processed_cv_image, [int(cv2.IMWRITE_PNG_BILEVEL), 1])[1]


def process_image(cv_image, param_set='A'):
    """
    Add image processing steps here!!
    """
    morph_kernel_size, \
    gauss_kernel_size, \
    thresh_window_size, \
    thresh_C, \
    rgb_threshold, \
    debug = processing_param_sets[param_set].values()

    # Thresholding
    if rgb_threshold:
        channels = cv2.split(cv_image)
        for i in range(len(channels)):
            channels[i] = cv2.GaussianBlur(channels[i], (gauss_kernel_size, gauss_kernel_size), 0)
            channels[i] = cv2.adaptiveThreshold(channels[i], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                                thresh_window_size, thresh_C)
        thresholded_image = cv2.cvtColor(cv2.merge(channels), cv2.COLOR_RGB2GRAY)

    else:
        grayed_img = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        blurred_img = cv2.GaussianBlur(grayed_img, (gauss_kernel_size, gauss_kernel_size), 0)
        thresholded_image = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                  cv2.THRESH_BINARY_INV, thresh_window_size, thresh_C)

    # Morphological operations
    morphological_kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
    opened_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, morphological_kernel)
    closed_image = cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, morphological_kernel)

    return closed_image


def publish(message):
    pubsub.PublisherClient() \
        .publish(topic=topic_res_name('ocr-detection-pickup'),
                 data=message)


def process_publish(image, filename):
    # Process the image
    cv_image = cv_import(image)
    processed_cv_image = process_image(cv_image)
    processed_image = cv_export(processed_cv_image)

    # Re-package the image and arguments and publish to Pub/Sub
    message = pack_message(processed_image, filename)
    publish(message)

    return "Ran processing and published to next step."
