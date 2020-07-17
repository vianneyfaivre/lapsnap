from imutils.video import VideoStream
import cv2
import os
from datetime import date, datetime
import sched
import time
from twisted.internet import task, reactor
import threading
from time import sleep

OUT_FOLDER = '/home/vianney/Pictures/Yoga'
LAP_DURATION_SECONDS = 15
DEBUG = False


def main():
    folder = createFolder(OUT_FOLDER)
    startCamera(folder, LAP_DURATION_SECONDS)


def createFolder(outFolder):

    subfolder = date.today().strftime("%Y-%m-%d")
    path = outFolder + "/" + subfolder

    if not os.path.isdir(path):
        os.makedirs(path)

    return path


def snap(folder, camera):

    # Generate file name
    now = datetime.fromtimestamp(time.time()).strftime('%Hh%M_%S')
    path = folder + "/" + now + ".png"
    print("Saving picture in " + path)

    # Snap!
    image = captureImage(camera)

    # Save file
    cv2.imwrite(path, image)


def startCamera(folder, lapDuration):

    task = None
    camera = VideoStream(src=0).start()

    shown = False

    while True:

        # Init window
        if not shown:
            print("Initialize camera and snap task")
            cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)

            if DEBUG is False:
                cv2.setWindowProperty(
                    "Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            task = RepeatedTimer(lapDuration, snap, folder, camera)

            shown = True

        # Display it
        cv2.imshow("Camera", captureImage(camera))

        # Close window when pressing "esc" or "q"
        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord("q") or pressedKey == 27:
            break

    cv2.destroyAllWindows()
    task.stop()


def captureImage(camera):

    image = camera.read()
    if image is None:
        print("No image")
        return None

    return image


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(
                self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


main()
