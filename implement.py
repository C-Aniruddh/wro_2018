import cv2
import config
import calculations
import threading
import time

import tetris_utils

from RPi import GPIO
import Adafruit_PCA9685
import serial

import eshita_god

import color_utils

ArduinoSerial = serial.Serial(config.ARDUINO_SERIAL_PORT, 9600, timeout=.1)

block_pickup = threading.Event()
block_pickup.clear()

camera_calculation = threading.Event()
camera_calculation.set()

hole_detection = threading.Event()
hole_detection.set()

start_pick = threading.Event()
start_pick.clear()

bot_running = threading.Event()
bot_running.clear()

cam = cv2.VideoCapture(config.CAMERA_ID)
cam.set(3, 320)
cam.set(4, 240)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))

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

cam_offset = 2.5

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

clk = 17
dt = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

SLF = "SLF"
SLF = SLF.encode('utf-8')

NLF = "NLF"
NLF = NLF.encode('utf-8')

PSH = "PSH"
PSH = PSH.encode('utf-8')

counter = 0
clkLastState = GPIO.input(clk)
print("Encoder at {}".format(clkLastState))

min_x = calculations.world_coordinates(0, 0)[0]
max_x = calculations.world_coordinates(320, 0)[0]

position_home = {'first': 80, 'second': 100, 'third': 85, 'fourth': 0, 'stack_b': 150, 'stack_u': 45}
position_pre_grip = {'first': 13, 'second': 134, 'third': 85, 'fourth': 0, 'stack_b': 150, 'stack_u': 45}
position_grip_2 = {'first': 5, 'second': 130, 'third': 85, 'fourth': 135, 'stack_b': 150, 'stack_u': 45}
position_grip = {'first': -5, 'second': 125, 'third': 85, 'fourth': 135, 'stack_b': 150, 'stack_u': 45}
position_lift = {'first': 60, 'second': 160, 'third': 85, 'fourth': 135, 'stack_b': 150, 'stack_u': 45}
position_lift_2 = {'first': 90, 'second': 160, 'third': 85, 'fourth': 135, 'stack_b': 150, 'stack_u': 45}
position_place = {'first': 125, 'second': -20, 'third': 85, 'fourth': 135, 'stack_b': 150, 'stack_u': 45}
position_drop = {'first': 125, 'second': -20, 'third': 85, 'fourth': 0, 'stack_b': 150, 'stack_u': 45}

print("Initializing")

angle_0 = 80
angle_1 = 100
angle_2 = 85
angle_3 = 0
angle_4 = 150
angle_5 = 45

pulse_0 = int(calculations.translate(angle_0, 0, 180, config.servo_min, config.servo_max))
pulse_1 = int(calculations.translate(angle_1, 0, 180, config.servo_min, config.servo_max))
pulse_2 = int(calculations.translate(angle_2, 0, 180, config.servo_min, config.servo_max))
pulse_3 = int(calculations.translate(angle_3, 0, 180, config.servo_min, config.servo_max))
pulse_4 = int(calculations.translate(angle_4, 0, 180, config.servo_min, config.servo_max))
pulse_5 = int(calculations.translate(angle_5, 0, 180, config.servo_min, config.servo_max))

pwm.set_pwm(2, 0, pulse_2)
time.sleep(0.1)
pwm.set_pwm(1, 0, pulse_1)
time.sleep(0.1)
pwm.set_pwm(0, 0, pulse_0)
time.sleep(0.1)
pwm.set_pwm(3, 0, pulse_3)
time.sleep(0.1)
pwm.set_pwm(15, 0, pulse_4)
time.sleep(0.1)
pwm.set_pwm(7, 0, pulse_5)
time.sleep(0.1)
print("Done!")

command = "GT-1-0"
command = command.encode('utf-8')

current_block = 0
current_f_position = []


def get_range(initial_value, final_value):
    if initial_value < final_value:
        range_1 = list(range(initial_value, final_value, 4))
    else:
        range_1 = list(range(initial_value, final_value, -4))
    range_1.append(final_value)
    return range_1


def actuate(range_in, channel):
    print("Actuating {} to {}".format(channel, range_in[-1]))
    for r in range_in:
        pulse = int(calculations.translate(r, 0, 180, config.servo_min, config.servo_max))
        pwm.set_pwm(channel, 0, pulse)
        time.sleep(0.05)
    print("Channel is {} at {}".format(channel, range_in[-1]))


def actuate_to_position(position_dict):
    global angle_0
    global angle_1
    global angle_2
    global angle_3
    global angle_4
    global angle_5
    global position

    first = position_dict['first']
    second = position_dict['second']
    third = position_dict['third']
    fourth = position_dict['fourth']
    stack_b = position_dict['stack_b']
    stack_u = position_dict['stack_u']

    if 'linear' in position_dict:
        linear = position_dict['linear']
        actuate_to_value(linear)

    range_1 = get_range(angle_0, first)
    range_2 = get_range(angle_1, second)
    range_3 = get_range(angle_2, third)
    range_4 = get_range(angle_3, fourth)
    range_5 = get_range(angle_4, stack_b)
    range_6 = get_range(angle_5, stack_u)

    angle_0 = first
    angle_1 = second
    angle_2 = third
    angle_3 = fourth
    angle_4 = stack_b
    angle_5 = stack_u

    print("Actuating to given position")
    actuate(range_3, 2)
    time.sleep(0.1)
    actuate(range_2, 1)
    time.sleep(0.1)
    actuate(range_1, 0)
    time.sleep(0.1)
    actuate(range_4, 3)
    time.sleep(0.1)
    actuate(range_5, 15)
    time.sleep(0.1)
    actuate(range_6, 7)
    time.sleep(0.1)
    print("Bot at given position!")


def choose_x(in_coordinates, block):
    global current_f_position
    indexes = []
    row_number = 0
    block_id = tetris_utils.get_block_id(block)
    solution_list = tetris_utils.solve_tetris()
    for row in solution_list:
        index = tetris_utils.indices(row, block_id, row_number)
        indexes.extend(index)
        row_number = row_number + 1

    f = tetris_utils.get_feasible_coordinates(indexes)
    feasible_coordinate = f[0]
    current_f_position = feasible_coordinate
    print(f)

    # chosen_x = min((abs(x), x) for x in x_points)[1]
    chosen_x = eshita_god.get_correct_hole(in_coordinates, feasible_coordinate)
    return chosen_x


def get_final_holes(im):
    keypoints = detector.detect(im)
    coordinates = []
    x_points = []
    for k in keypoints:
        u = int(k.pt[0]) - 160
        v = int(k.pt[1]) + 120
        x, y = calculations.world_coordinates(int(u), int(v))
        x = x + cam_offset
        coordinates.append([x, y])

    sorted_coordinates = sorted(coordinates, key=lambda x: x[1], reverse=True)
    """for index in range(0, 2, 1):
        x_point = sorted_coordinates[index][0]
        x_points.append(x_point)"""

    return sorted_coordinates


def detect_holes(im):
    overlay = im.copy()
    keypoints = detector.detect(im)
    x_points = []
    for k in keypoints:
        u = int(k.pt[0]) - 160
        x, y = calculations.world_coordinates(int(u), int(u))
        x = x + cam_offset
        x_points.append(x)
        cv2.circle(overlay, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (0, 0, 255), 2)
        cv2.line(overlay, (int(k.pt[0]) - 20, int(k.pt[1])), (int(k.pt[0]) + 20, int(k.pt[1])), (0, 0, 0), 3)
        cv2.line(overlay, (int(k.pt[0]), int(k.pt[1]) - 20), (int(k.pt[0]), int(k.pt[1]) + 20), (0, 0, 0), 3)
        cv2.putText(overlay, str("({:.2f}, {:.2f})".format(float(x), float(y))), (int(k.pt[0]), int(k.pt[1])),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)

    no_points = len(x_points)
    if no_points >= 2 and (not start_pick.wait(timeout=0.5)):
        global current_block
        start_pick.set()
        print("Sending NLF")
        ArduinoSerial.write(bytes(NLF))
        print("NLF Sent")
        time.sleep(1)
        print("Pushing block")
        ArduinoSerial.write(bytes(PSH))
        time.sleep(0.3)
        print("Pushed block")
        print("Waiting for 1 second before calculating points")
        time.sleep(1)
        final_pts = get_final_holes(im)
        shape = color_utils.get_color(im)
        current_block = tetris_utils.get_block_id(shape)
        chosen_x = choose_x(final_pts, shape)
        threading.Thread(target=pickup_thread, args=[chosen_x, shape]).start()
    opacity = 0.5
    cv2.addWeighted(overlay, opacity, im, 1 - opacity, 0, im)
    return im


def pickup_thread(chosen_x, shape):
    while start_pick.wait(timeout=0.5):
        print("FOUND BLOCK : {}".format(shape))
        print("Found block! Stopping camera and starting actuation in 3 seconds")
        print(chosen_x)
        time.sleep(3)
        block_pickup.set()
        camera_calculation.set()
        hole_detection.clear()
        actuate_to_x(int(chosen_x))


def actuate_to_value(in_value):
    global counter, clkLastState
    if counter < in_value:
        pulse = int(calculations.translate(108, 0, 180, config.servo_min, config.servo_max))
        while counter <= in_value:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if dtState != clkState:
                    counter += 1
                else:
                    counter -= 1
            print(counter)
            clkLastState = clkState
            time.sleep(0.01)
            pwm.set_pwm(11, 0, pulse)
            if counter == in_value:
                pwm.set_pwm(11, 0, 0)
                break
    else:
        pulse = int(calculations.translate(95, 0, 180, config.servo_min, config.servo_max))
        while counter >= in_value:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if dtState != clkState:
                    counter += 1
                else:
                    counter -= 1
            print(counter)
            clkLastState = clkState
            time.sleep(0.01)
            pwm.set_pwm(11, 0, pulse)
            if counter == in_value:
                pwm.set_pwm(11, 0, 0)
                break
    return True


def temp_position_handler(in_string, f_position):
    if in_string == "home":
        actuate_to_position(position_home)
    elif in_string == "pre_grip":
        actuate_to_position(position_pre_grip)
    elif in_string == "grip_2":
        actuate_to_position(position_grip_2)
    elif in_string == "grip":
        actuate_to_position(position_grip)
    elif in_string == "lift":
        actuate_to_position(position_lift)
    elif in_string == "lift_2":
        actuate_to_position(position_lift_2)
    elif in_string == "place":
        actuate_to_position(position_place)
    elif in_string == "drop":
        position_f = get_drop_position(f_position)
        actuate_to_position(position_f)


def get_drop_position(coordinate):
    return position_drop


def actuate_to_x(distance):
    while not hole_detection.wait(timeout=0.5):
        print("Moving in X")
        steps = int(calculations.translate(distance, -6.5, 6.5, -45, 45))
        done = actuate_to_value(int(steps))

        if done:
            print("Moved in X. Picking up in 3 seconds")
            time.sleep(3)

            positions = ["home", "pre_grip", "grip_2", "grip", "lift", "lift_2", "place", "drop"]

            for position in positions:
                temp_position_handler(position, current_f_position)
                print("Completed a position, sleeping for 1")
                time.sleep(1)

            print("Going back home!")
            temp_position_handler("home")
            actuate_to_value(0)
            print("At home, sleeping for 2")
            time.sleep(2)
            ArduinoSerial.write(bytes(SLF))
            print("Sleep over, camera starting")
            block_pickup.clear()
            start_pick.clear()
            hole_detection.set()
            camera_calculation.set()


def camera_vision():
    while camera_calculation.wait(timeout=0.5):
        _, frame = cam.read()
        """scale_percent = 50  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)"""

        if hole_detection.is_set():
            holes = detect_holes(frame)
        else:
            holes = frame
        """cv2.imshow("Holes", holes)
        kc = cv2.waitKey(1) & 0xff
        if kc == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break
        """


threading.Thread(target=camera_vision).start()
vbc = input("Enter any key to start : ")
print("Sleeping for 3")
time.sleep(3)
print("START")
ArduinoSerial.write(bytes(SLF))

avc = input("Enter any key to send to 1,1 : ")
ArduinoSerial.write(bytes(command))
