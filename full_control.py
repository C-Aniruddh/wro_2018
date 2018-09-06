import cv2
import config
import calculations
import threading
import time

from RPi import GPIO
import Adafruit_PCA9685
import serial

ArduinoSerial = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)

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

counter = 0
clkLastState = GPIO.input(clk)
print("Encoder at {}".format(clkLastState))

min_x = calculations.world_coordinates(0, 0)[0]
max_x = calculations.world_coordinates(320, 0)[0]

position_home = {'first': 90, 'second': 123, 'third': 85, 'fourth': 0, 'stack_b': 100, 'stack_u': 60}
position_pre_grip = {'first': 30, 'second': 145, 'third': 85, 'fourth': 0, 'stack_b': 100, 'stack_u': 60}
position_grip = {'first': 5, 'second': 145, 'third': 85, 'fourth': 90, 'stack_b': 130, 'stack_u': 90}
position_lift = {'first': 90, 'second': 160, 'third': 85, 'fourth': 90, 'stack_b': 130, 'stack_u': 90}
position_place = {'first': 140, 'second': -20, 'third': 85, 'fourth': 90, 'stack_b': 130, 'stack_u': 90}
position_drop = {'first': 145, 'second': -20, 'third': 85, 'fourth': 0, 'stack_b': 130, 'stack_u': 90}

print("Initializing")

angle_0 = 90
angle_1 = 123
angle_2 = 85
angle_3 = 0
angle_4 = 100
angle_5 = 60

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
pwm.set_pwm(7, 0, pulse_4)
time.sleep(0.1)
pwm.set_pwm(5, 0, pulse_5)
time.sleep(0.1)
print("Done!")

command = "GT-1-0"
command = command.encode('utf-8')

vbc = input("Enter any key to start : ")
print("Sleeping for 3")
time.sleep(3)
print("START")
ArduinoSerial.write(bytes(SLF))

avc = input("Eter any key to send to 1,1 : ")
ArduinoSerial.write(bytes(command))


def get_range(initial_value, final_value):
    if initial_value < final_value:
        range_1 = list(range(initial_value, final_value, 3))
    else:
        range_1 = list(range(initial_value, final_value, -3))
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

    first = position_dict['first']
    second = position_dict['second']
    third = position_dict['third']
    fourth = position_dict['fourth']
    stack_b = position_dict['stack_b']
    stack_u = position_dict['stack_u']

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
    actuate(range_5, 7)
    time.sleep(0.1)
    actuate(range_6, 5)
    time.sleep(0.1)
    print("Bot at given position!")


def detect_holes(im):
    overlay = im.copy()
    keypoints = detector.detect(im)
    x_points = []
    for k in keypoints:
        u = int(k.pt[0]) - 160
        v = int(k.pt[1]) + 120
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
    if no_points == 2 and (not start_pick.wait(timeout=0.5)):
        start_pick.set()
        time.sleep(0.1)
        ArduinoSerial.write(bytes(NLF))
        time.sleep(0.3)
        threading.Thread(target=pickup_thread, args=[x_points]).start()
    opacity = 0.5
    cv2.addWeighted(overlay, opacity, im, 1 - opacity, 0, im)
    return im


def pickup_thread(x_points):
    while start_pick.wait(timeout=0.5):
        print("Found block! Stopping camera and starting actuation in 5 seconds")
        time.sleep(5)
        chosen_x = min((abs(x), x) for x in x_points)[1]
        print(chosen_x)
        time.sleep(2)
        block_pickup.set()
        camera_calculation.set()
        hole_detection.clear()
        actuate_to_x(int(chosen_x))


def actuate_to_value(in_value):
    global counter, clkLastState
    if counter < in_value:
        pulse = int(calculations.translate(106, 0, 180, config.servo_min, config.servo_max))
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
        pulse = int(calculations.translate(97, 0, 180, config.servo_min, config.servo_max))
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


def temp_position_handler(in_string):
    if in_string == "home":
        actuate_to_position(position_home)
    elif in_string == "pre_grip":
        actuate_to_position(position_pre_grip)
    elif in_string == "grip":
        actuate_to_position(position_grip)
    elif in_string == "lift":
        actuate_to_position(position_lift)
    elif in_string == "place":
        actuate_to_position(position_place)
    elif in_string == "drop":
        actuate_to_position(position_drop)


def actuate_to_x(distance):
    while not hole_detection.wait(timeout=0.5):
        print("Moving in X")
        steps = int(calculations.translate(distance, -6.5, 6.5, -45, 45))
        done = actuate_to_value(int(steps))

        if done:
            print("Moved in X. Picking up in 3 seconds")
            time.sleep(3)

            positions = ["home", "pre_grip", "grip", "lift", "place", "drop"]

            for position in positions:
                temp_position_handler(position)
                print("Completed a position, sleeping for 2")
                time.sleep(2)

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
        scale_percent = 50  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        if hole_detection.is_set():
            holes = detect_holes(resized)
        else:
            holes = resized
        cv2.imshow("Holes", holes)
        kc = cv2.waitKey(1) & 0xff
        if kc == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break

threading.Thread(target=camera_vision).start()
