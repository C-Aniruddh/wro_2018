import cv2
import math

cam = cv2.VideoCapture(0)

detector = cv2.SimpleBlobDetector_create()
params = cv2.SimpleBlobDetector_Params()

# Filter by Area.
params.filterByArea = True
params.minArea = 100
params.maxArea = 4000

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.6

# Filter by Convexity
params.filterByConvexity = False
# params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.8

# Distance Between Blobs
params.minDistBetweenBlobs = 5

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)


def getDelta():
    _, frame = cam.read()
    _, dx, dy = detect_holes(frame)
    return (-dy), dx  # shifting to Normal Co-ordinates


def detect_holes(im):
    overlay = im.copy()

    keypoints = detector.detect(im)

    for k in keypoints:
        cv2.circle(overlay, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (0, 0, 255), 2)
        cv2.line(overlay, (int(k.pt[0]) - 20, int(k.pt[1])), (int(k.pt[0]) + 20, int(k.pt[1])), (0, 0, 0), 3)
        cv2.line(overlay, (int(k.pt[0]), int(k.pt[1]) - 20), (int(k.pt[0]), int(k.pt[1]) + 20), (0, 0, 0), 3)

    opacity = 0.5
    cv2.addWeighted(overlay, opacity, im, 1 - opacity, 0, im)
    return im


if __name__ == "__main__":
    while True:
        _, frame = cam.read()
        scale_percent = 50  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        holes = detect_holes(resized)
        cv2.imshow("holes", holes)
        kc = cv2.waitKey(1) & 0xff
        if kc == ord('q'):
            break;

    cv2.destroyALlWindows()
    cam.release()
