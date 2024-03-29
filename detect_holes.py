import cv2
import config
import calculations
import threading
# import color_nn

# block_pickup = threading.Event()
# block_pickup.clear()

cam = cv2.VideoCapture(config.CAMERA_ID)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))
cam.set(3, 320)
cam.set(4, 240)

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

# blocks_graph = color_nn.load_graph(model_file="./models/model/stack_graph.pb")
# labels = color_nn.load_labels(label_file="./models/model/stack_label.txt")

max_x = 0


def detect_holes(im):
    overlay = im.copy()
    keypoints = detector.detect(im)
    x_points = []
    x_coords = []
    for k in keypoints:
        x_coords.append(int(k.pt[0]))
        x, y = calculations.world_coordinates(int(k.pt[0]), int(k.pt[1]))
        x_points.append(x)
        cv2.circle(overlay, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (0, 0, 255), 2)
        cv2.line(overlay, (int(k.pt[0]) - 20, int(k.pt[1])), (int(k.pt[0]) + 20, int(k.pt[1])), (0, 0, 0), 3)
        cv2.line(overlay, (int(k.pt[0]), int(k.pt[1]) - 20), (int(k.pt[0]), int(k.pt[1]) + 20), (0, 0, 0), 3)
        cv2.putText(overlay, str("({:.2f}, {:.2f})".format(float(x), float(y))), (int(k.pt[0]), int(k.pt[1])),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # chosen_x = min((abs(x), x) for x in x_points)[1]
    # block_pickup.set()
    max_x = max(x_coords)
    opacity = 0.5
    cv2.addWeighted(overlay, opacity, im, 1 - opacity, 0, im)
    return im


def camera_vision():
    # while not block_pickup.wait(timeout=5000):
    while True:
        _, frame = cam.read()
        # print(frame.shape[0], frame.shape[1])
        """scale_percent = 50  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)"""
        holes = detect_holes(frame)
        cv2.imshow("holes", holes)
        crop = frame[80:240, 0:320]
        cv2.imshow("crop", crop)
        kc = cv2.waitKey(1) & 0xff
        if kc == ord('q'):
            # cv2.imwrite("1.jpg", frame)
            # shape = color_nn.get_block_shape(graph_instance=blocks_graph, file_name="1.jpg", label_instance=labels)
            # print(shape)
            break
    cv2.destroyALlWindows()
    cam.release()


threading.Thread(target=camera_vision).start()
