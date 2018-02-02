from __future__ import print_function, division

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import imutils
import cv2

from camera.panorama import Stitcher
from Servos import PanTilt

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.hflip = True
camera.vflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))


def takePano(tilt_overlap=20, pan_overlap=20):
    pt = PanTilt()
    pan_range = pt.pan.cal.max - pt.pan.cal.min
    tilt_range = pt.tilt.cal.max - pt.tilt.cal.min

    num_rows = tilt_range // tilt_overlap
    num_cols = pan_range // pan_overlap

    tilt_delta = tilt_range // num_rows
    pan_delta = pan_range // num_cols

    imageMatrix = [[None] * num_cols] * num_rows

    row_count = 0
    for tiltVal in range(pt.tilt.cal.min,
                         pt.tilt.cal.min + num_cols * tilt_delta,
                         tilt_delta):
        col_count = 0
        for panVal in range(pt.pan.cal.min,
                            pt.pan.cal.min + num_cols * pan_delta,
                            pan_delta):

            pt.vecMoveAbsolute([panVal, tiltVal])
            time.sleep(0.5)
            rawCapture = PiRGBArray(camera, size=(640, 480))
            camera.capture(rawCapture, format="bgr")
            imageMatrix[row_count][col_count] = rawCapture.array
            cv2.imshow("Image",
                       imageMatrix[row_count][col_count])
            cv2.waitKey(500)
            col_count += 1
        row_count += 1
    pt.center()
    cv2.destroyAllWindows()
    return imageMatrix
