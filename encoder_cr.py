from __future__ import division
import time
import threading

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

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

def rotary_encoder():
    global clkLastState, counter
    while True:
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

print('Moving servo on channel 0, press Ctrl-C to quit...')

threading.Thread(target=rotary_encoder).start()

while True:
    angle = int(input("Enter angle : "))
    pulse = int(translate(angle, 0, 180, servo_min, servo_max))
    pwm.set_pwm(11, 0, pulse)

