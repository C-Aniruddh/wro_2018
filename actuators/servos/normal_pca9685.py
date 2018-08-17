import utils.utils

import Adafruit_PCA9685

class PWMServo:

    zero_ANGLE = 0
    full_ANGLE = 180

    def __init__(self, channel,
                 zero_pulse=290,
                 full_pulse=490):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.channel = channel
        self.zero_pulse = zero_pulse
        self.full_pulse = full_pulse

    def run(self, angle):

        pulse = utils.utils.map_range(angle,
                                      self.zero_ANGLE, self.full_ANGLE,
                                      self.zero_pulse, self.zero_pulse)
        pwm.set_pwm(self.channel, 0, pulse)

    def shutdown(self):
        self.run(0)
