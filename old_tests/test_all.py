from __future__ import division
import time

import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

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
angle_0 = 60
angle_1 = 70
angle_2 = 85
angle_3 = 0

pulse_0 = int(translate(angle_0, 0, 180, servo_min, servo_max))
pulse_1 = int(translate(angle_1, 0, 180, servo_min, servo_max))
pulse_2 = int(translate(angle_2, 0, 180, servo_min, servo_max))
pulse_3 = int(translate(angle_3, 0, 180, servo_min, servo_max))

pwm.set_pwm(2, 0, pulse_2)
time.sleep(0.1)
pwm.set_pwm(1, 0, pulse_1)
time.sleep(0.1)
pwm.set_pwm(0, 0, pulse_0)
time.sleep(0.1)
pwm.set_pwm(3, 0, pulse_3)
time.sleep(0.1)
print("Done!")

while True:
    angle_0_old = angle_0
    angle_1_old = angle_1
    angle_2_old = angle_2
    angle_3_old = angle_3
    print("Old", angle_0_old, angle_1_old, angle_2_old, angle_3_old)
    angle_0 = int(input("Enter angle 0 : "))
    angle_1 = int(input("Enter angle 1 : "))
    angle_2 = int(input("Enter angle 2 : "))
    angle_3 = int(input("Enter angle 3 : "))
    # pulse_0 = int(translate(angle_0, 0, 180, servo_min, servo_max))
    # pulse_1 = int(translate(angle_1, 0, 180, servo_min, servo_max))
    # pulse_2 = int(translate(angle_2, 0, 180, servo_min, servo_max))

    range_1 = get_range(angle_0_old, angle_0)
    range_2 = get_range(angle_1_old, angle_1)
    range_3 = get_range(angle_2_old, angle_2)
    range_4 = get_range(angle_3_old, angle_3)

    a = input("Enter any key to actuate channel 0 : ")
    # pwm.set_pwm(0, 0, pulse_0)
    actuate(range_3, 2)
    b = input("Enter any key to actuate channel 1 : ")
    # pwm.set_pwm(1, 0, pulse_1)
    actuate(range_2, 1)
    c = input("Enter any key to actuate channel 2 : ")
    # pwm.set_pwm(2, 0, pulse_2)
    actuate(range_1, 0)
    d = input("Enter any key to actuate channel 3 : ")
    actuate(range_4, 3)

"""while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, servo_min)
    pwm.set_pwm(1, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_max)
    pwm.set_pwm(1, 0, servo_max)
    time.sleep(1)
"""
