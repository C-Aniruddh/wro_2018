from __future__ import division
from tkinter import *

import time
from RPi import GPIO

import Adafruit_PCA9685

clk = 17
dt = 18

pwm = Adafruit_PCA9685.PCA9685()
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)
print("Encoder at {}".format(clkLastState))

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


def actuate(range_in, channel):
    print("Actuating {}".format(channel))
    for r in range_in:
        print(r)
        pulse = int(translate(r, 0, 180, servo_min, servo_max))
        pwm.set_pwm(channel, 0, pulse)
        time.sleep(0.05)


# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print("Initializing")
angle_0 = 90
angle_1 = 110
angle_2 = 85
angle_3 = 0
angle_4 = 180
angle_5 = 120
position = 0

pulse_0 = int(translate(angle_0, 0, 180, servo_min, servo_max))
pulse_1 = int(translate(angle_1, 0, 180, servo_min, servo_max))
pulse_2 = int(translate(angle_2, 0, 180, servo_min, servo_max))
pulse_3 = int(translate(angle_3, 0, 180, servo_min, servo_max))
pulse_4 = int(translate(angle_4, 0, 180, servo_min, servo_max))
pulse_5 = int(translate(angle_5, 0, 180, servo_min, servo_max))


pwm.set_pwm(2, 0, pulse_2)
time.sleep(1)
pwm.set_pwm(1, 0, pulse_1)
time.sleep(1)
pwm.set_pwm(0, 0, pulse_0)
time.sleep(1)
pwm.set_pwm(3, 0, pulse_3)
time.sleep(1)
pwm.set_pwm(15, 0, pulse_4)
time.sleep(1)
pwm.set_pwm(7, 0, pulse_5)
time.sleep(1)


"""
range_1 = get_range(0, angle_0)
range_2 = get_range(0, angle_1)
range_3 = get_range(0, angle_2)
range_4 = get_range(0, angle_3)
range_5 = get_range(0, angle_4)
range_6 = get_range(0, angle_5)

actuate(range_3, 2)
time.sleep(1)
actuate(range_2, 1)
time.sleep(1)
actuate(range_1, 0)
time.sleep(1)
actuate(range_4, 3)
time.sleep(1)
actuate(range_5, 15)
time.sleep(1)
actuate(range_6, 7)
time.sleep(1)
"""
print("Done!")


def actuate_to_value(in_value):
    global counter, clkLastState
    if counter < in_value:
        pulse = int(translate(106, 0, 180, servo_min, servo_max))
        while (counter <= in_value):
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
            if (counter == in_value):
                pwm.set_pwm(11, 0, 0)
                break;
    else:
        pulse = int(translate(96, 0, 180, servo_min, servo_max))
        while (counter >= in_value):
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
            if (counter == in_value):
                pwm.set_pwm(11, 0, 0)
                break;


def go_home():
    global angle_0, angle_1, angle_2, angle_3, angle_4, angle_5, position
    angle_0_old = angle_0
    angle_1_old = angle_1
    angle_2_old = angle_2
    angle_3_old = angle_3
    angle_4_old = angle_4
    angle_5_old = angle_5

    angle_0 = int(90)
    angle_1 = int(120)
    angle_2 = int(85)
    angle_3 = int(0)
    angle_4 = int(180)
    angle_5 = int(120)
    position = int(0)

    range_1 = get_range(angle_0_old, angle_0)
    range_2 = get_range(angle_1_old, angle_1)
    range_3 = get_range(angle_2_old, angle_2)
    range_4 = get_range(angle_3_old, angle_3)
    range_5 = get_range(angle_4_old, angle_4)
    range_6 = get_range(angle_5_old, angle_5)

    actuate(range_3, 2)
    time.sleep(1)
    actuate(range_2, 1)
    time.sleep(1)
    actuate(range_1, 0)
    time.sleep(1)
    actuate(range_4, 3)
    time.sleep(1)
    actuate(range_5, 15)
    time.sleep(1)
    actuate(range_6, 7)
    time.sleep(1)
    actuate_to_value(position)
    time.sleep(1)
    label.config(text="Home")


def sel():
    global angle_0, angle_1, angle_2, angle_3, angle_4, angle_5, position
    angle_0_old = angle_0
    angle_1_old = angle_1
    angle_2_old = angle_2
    angle_3_old = angle_3
    angle_4_old = angle_4
    angle_5_old = angle_5
    print("Old", angle_0_old, angle_1_old, angle_2_old, angle_3_old)
    angle_0 = int(angle_0_gui.get())
    angle_1 = int(angle_1_gui.get())
    angle_2 = int(angle_2_gui.get())
    angle_3 = int(angle_3_gui.get())
    angle_4 = int(angle_4_gui.get())
    angle_5 = int(angle_5_gui.get())
    position = int(linear_0_gui.get())

    range_1 = get_range(angle_0_old, angle_0)
    range_2 = get_range(angle_1_old, angle_1)
    range_3 = get_range(angle_2_old, angle_2)
    range_4 = get_range(angle_3_old, angle_3)
    range_5 = get_range(angle_4_old, angle_4)
    range_6 = get_range(angle_5_old, angle_5)

    actuate(range_3, 2)
    time.sleep(1)
    actuate(range_2, 1)
    time.sleep(1)
    actuate(range_1, 0)
    time.sleep(1)
    actuate(range_4, 3)
    time.sleep(1)
    actuate(range_5, 15)
    time.sleep(1)
    actuate(range_6, 7)
    time.sleep(1)
    actuate_to_value(position)
    time.sleep(1)
    label.config(text="Actuated")


root = Tk()
angle_0_gui = DoubleVar()
scale_0 = Scale(root, variable=angle_0_gui, orient=HORIZONTAL, label="Servo 0", from_=-20, to=200)
scale_0.set(angle_0)
scale_0.pack()

angle_1_gui = DoubleVar()
scale_1 = Scale(root, variable=angle_1_gui, orient=HORIZONTAL, label="Servo 1", from_=-20, to=200)
scale_1.set(angle_1)
scale_1.pack()

angle_2_gui = DoubleVar()
scale_2 = Scale(root, variable=angle_2_gui, orient=HORIZONTAL, label="Servo 2", from_=-20, to=200)
scale_2.set(angle_2)
scale_2.pack()

angle_3_gui = DoubleVar()
scale_3 = Scale(root, variable=angle_3_gui, orient=HORIZONTAL, label="Gripper", from_=0, to=180)
scale_3.set(angle_3)
scale_3.pack()

angle_4_gui = DoubleVar()
scale_4 = Scale(root, variable=angle_4_gui, orient=HORIZONTAL, label="Stack (bottom)", from_=-20, to=200)
scale_4.set(angle_4)
scale_4.pack()

angle_5_gui = DoubleVar()
scale_5 = Scale(root, variable=angle_5_gui, orient=HORIZONTAL, label="Stack (Up)", from_=-20, to=200)
scale_5.set(angle_5)
scale_5.pack()

linear_0_gui = DoubleVar()
scale_6 = Scale(root, variable=linear_0_gui, orient=HORIZONTAL, label="Linear Actuator", from_=-60, to=60)
scale_6.set(0)
scale_6.pack()

button = Button(root, text="Actuate", command=sel)
button.pack(anchor=CENTER)

button2 = Button(root, text="Go Home", command=go_home)
button2.pack(anchor=CENTER)

label = Label(root)
label.pack()

root.mainloop()
