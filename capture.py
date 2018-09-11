import cv2
import time 

cpt = 0
maxFrames = 25 # if you want 5 frames only.

try:
    vidStream = cv2.VideoCapture(0) # index of your camera
except:
    print("problem opening input stream")
    sys.exit(1)

while cpt < maxFrames:
    ret, frame = vidStream.read() # read frame and return code.
    if not ret: # if return code is bad, abort.
        sys.exit(0)
    cv2.imshow("test window", frame) # show image in window
    cv2.imwrite("image%04i.jpg" %cpt, frame)
    time.sleep(0.2)
    cpt += 1
