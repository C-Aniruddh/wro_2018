from __future__ import division
import time

import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

angle_0 = 60
angle_1 = 70
angle_2 = 90

position_home = {'first' : 60, 'second' : 70, 'third' : 90}
position_pre_grip = {'first' : 0, 'second' : 87, 'third' : 90}
position_grip = {'first' : 0, 'second' : 100, 'third' : 90}
position_example = {'first' : 130, 'second' : 0, 'third' : 90}

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


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
        pulse = int(translate(r, 0, 180, servo_min, servo_max))
        pwm.set_pwm(channel, 0, pulse)
        time.sleep(0.05)
    print("Channel is {} at {}".format(channel, range_in[-1]))

def actuate_to_position(position_dict):
    global angle_0
    global angle_1
    global angle_2
    first = position_dict['first']
    second = position_dict['second']
    third = position_dict['third']
    range_1 = get_range(angle_0, first)
    range_2 = get_range(angle_1, second)
    range_3 = get_range(angle_2, third)
    angle_0 = first
    angle_1 = second
    angle_2 = third
    print("Actuating to given position")
    actuate(range_3, 2)
    time.sleep(0.1)
    actuate(range_2, 1)
    time.sleep(0.1)
    actuate(range_1, 0)
    time.sleep(0.1)
    print("Bot at given position!")

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print("Initializing")
pulse_0 = int(translate(angle_0, 0, 180, servo_min, servo_max))
pulse_1 = int(translate(angle_1, 0, 180, servo_min, servo_max))
pulse_2 = int(translate(angle_2, 0, 180, servo_min, servo_max))

pwm.set_pwm(2, 0, pulse_2)
time.sleep(0.1)
pwm.set_pwm(1, 0, pulse_1)
time.sleep(0.1)
pwm.set_pwm(0, 0, pulse_0)
time.sleep(0.1)
print("Done!")

def temp_position_handler(in_string):
    if in_string == "home":
        actuate_to_position(position_home)
    elif in_string == "pre_grip":
        actuate_to_position(position_pre_grip)
    elif in_string == "grip":
        actuate_to_position(position_grip)
    elif in_string == "example":
        actuate_to_position(position_example)

positions = ["home", "pre_grip", "grip", "example"]

while True:
    for position in positions:
        temp_position_handler(position)
        time.sleep(0.5)

