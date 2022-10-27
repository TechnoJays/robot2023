from cscore import CameraServer


def main():
    cs1 = CameraServer.getInstance()
    cs1.enableLogging()

    cs2 = CameraServer.getInstance()
    cs2.enableLogging()

    usb1 = cs1.startAutomaticCapture(dev=0)
    usb2 = cs2.startAutomaticCapture(dev=1)

    cs1.waitForever()
    cs2.waitForever()
