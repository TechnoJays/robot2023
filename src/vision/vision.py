from cscore import CameraServer
import numpy as np
import cv2


def start_camera():
    camera_server = CameraServer.getInstance()
    camera_server.enableLogging()
    usb_camera = camera_server.startAutomaticCapture()
    usb_camera.setResolution(320, 420)

    camera_server.getVideo()

    cv_sink = camera_server.getVideo()

    output_stream = camera_server.putVideo("Rectangle", 324, 420)

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        time, img = cv_sink.grabFrame(img)
        if time == 0:
            output_stream.notify_error(cv_sink.getError())
            continue
        cv2.rectangle(img, (100, 100), (300, 300), (255, 255, 255), 5)
        output_stream.putFrame(img)
