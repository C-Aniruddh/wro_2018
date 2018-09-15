# For more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import cv2
import numpy as np

# Playing video from file:
# cap = cv2.VideoCapture('vtest.avi')
# Capturing video from webcam:
cap = cv2.VideoCapture(1)
cap.set(3, 320)
cap.set(4, 240)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))

currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Handles the mirroring of the current frame
    frame = cv2.flip(frame,1)

    # Our operations on the frame come here
    gray = frame

    # Saves image of the current frame in jpg file
    # name = 'frame' + str(currentFrame) + '.jpg'
    # cv2.imwrite(name, frame)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# Potential Error:
# OpenCV: Cannot Use FaceTime HD Kamera
# OpenCV: camera failed to properly initialize!
# Segmentation fault: 11
#
# Solution:
# I solved this by restarting my computer.
# http://stackoverflow.com/questions/40719136/opencv-cannot-use-facetime/42678644#42678644
