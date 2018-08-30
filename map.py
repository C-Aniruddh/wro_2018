import cv2
import config
import calculations
import threading


# block_pickup = threading.Event()
# block_pickup.clear()

cam = cv2.VideoCapture(config.CAMERA_ID)

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


def detect_holes(im):
    overlay = im.copy()
    keypoints = detector.detect(im)
    x_points = []
    for k in keypoints:
        u = int(k.pt[0]) - 320
        v = int(k.pt[1]) - 240
        print(u, v)
        x, y = calculations.world_coordinates(int(u), int(v))
        x_points.append(x)
        cv2.circle(overlay, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (0, 0, 255), 2)
        cv2.line(overlay, (int(k.pt[0]) - 20, int(k.pt[1])), (int(k.pt[0]) + 20, int(k.pt[1])), (0, 0, 0), 3)
        cv2.line(overlay, (int(k.pt[0]), int(k.pt[1]) - 20), (int(k.pt[0]), int(k.pt[1]) + 20), (0, 0, 0), 3)
        cv2.putText(overlay, str("({:.2f}, {:.2f})".format(float(x), float(y))), (int(k.pt[0]), int(k.pt[1])),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # chosen_x = min((abs(x), x) for x in x_points)[1]
    # block_pickup.set()

    opacity = 0.5
    cv2.addWeighted(overlay, opacity, im, 1 - opacity, 0, im)
    return im


def camera_vision():
    # while not block_pickup.wait(timeout=5000):
    while True:
        _, frame = cam.read()
        holes = detect_holes(frame)
        cv2.imshow("holes", holes)
        kc = cv2.waitKey(1) & 0xff
        if kc == ord('q'):
            break;

    cv2.destroyALlWindows()
    cam.release()


threading.Thread(target=camera_vision).start()
