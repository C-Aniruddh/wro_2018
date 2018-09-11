from __future__ import division
from tkinter import *

import time

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096


def get_range(initial_value, final_value):
    if initial_value < final_value:
        range_1 = list(range(initial_value, final_value, 2))
    else:
        range_1 = list(range(initial_value, final_value, -2))
    range_1.append(final_value)
    return range_1


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def actuate(angle, channel):
    pulse = int(translate(angle, 0, 180, servo_min, servo_max))
    pwm.set_pwm(channel, 0, pulse)


# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print("Initializing")
angle_0 = 90
angle_1 = 110
angle_2 = 85
angle_3 = 0
angle_4 = 100
angle_5 = 60

pulse_0 = int(translate(angle_0, 0, 180, servo_min, servo_max))
pulse_1 = int(translate(angle_1, 0, 180, servo_min, servo_max))
pulse_2 = int(translate(angle_2, 0, 180, servo_min, servo_max))
pulse_3 = int(translate(angle_3, 0, 180, servo_min, servo_max))
pulse_4 = int(translate(angle_4, 0, 180, servo_min, servo_max))
pulse_5 = int(translate(angle_5, 0, 180, servo_min, servo_max))

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


def actuate_angle_0(value):
    angle = int(value)
    actuate(angle, 0)


def actuate_angle_1(value):
    angle = int(value)
    actuate(angle, 1)


def actuate_angle_2(value):
    angle = int(value)
    actuate(angle, 2)


def actuate_angle_3(value):
    angle = int(value)
    actuate(angle, 3)


def actuate_angle_4(value):
    angle = int(value)
    actuate(angle, 7)


def actuate_angle_5(value):
    angle = int(value)
    actuate(angle, 5)


root = Tk()
angle_0_gui = DoubleVar()
scale_0 = Scale(root, variable=angle_0_gui, orient=HORIZONTAL, label="Servo 0", from_=-20, to=200, command=actuate_angle_0)
scale_0.set(angle_0)
scale_0.pack()

angle_1_gui = DoubleVar()
scale_1 = Scale(root, variable=angle_1_gui, orient=HORIZONTAL, label="Servo 1", from_=-20, to=200, command=actuate_angle_1)
scale_1.set(angle_1)
scale_1.pack()

angle_2_gui = DoubleVar()
scale_2 = Scale(root, variable=angle_2_gui, orient=HORIZONTAL, label="Servo 2", from_=-20, to=200, command=actuate_angle_2)
scale_2.set(angle_2)
scale_2.pack()

angle_3_gui = DoubleVar()
scale_3 = Scale(root, variable=angle_3_gui, orient=HORIZONTAL, label="Gripper", from_=-20, to=200, command=actuate_angle_3)
scale_3.set(angle_3)
scale_3.pack()

angle_4_gui = DoubleVar()
scale_4 = Scale(root, variable=angle_4_gui, orient=HORIZONTAL, label="Stack (bottom)", from_=-20, to=200, command=actuate_angle_4)
scale_4.set(angle_4)
scale_4.pack()

angle_5_gui = DoubleVar()
scale_5 = Scale(root, variable=angle_5_gui, orient=HORIZONTAL, label="Stack (Up)", from_=-20, to=200, command=actuate_angle_5)
scale_5.set(angle_5)
scale_5.pack()

root.mainloop()
