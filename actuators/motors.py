import time
import utils.utils

class PCA9685:
    '''
    PWM motor controler using PCA9685 boards.
    '''
    def __init__(self, channel, address=0x40, frequency=60, busnum=None):
        import Adafruit_PCA9685
        # Initialise the PCA9685 using the default address (0x40).
        if busnum is not None:
            from Adafruit_GPIO import I2C
            #replace the get_bus function with our own
            def get_bus():
                return busnum
            I2C.get_default_bus = get_bus
        self.pwm = Adafruit_PCA9685.PCA9685(address=address)
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel

    def set_pulse(self, pulse):
        self.pwm.set_pwm(self.channel, 0, pulse)

    def run(self, pulse):
        self.set_pulse(pulse)


class PWMThrottle:
    """
    Wrapper over a PWM motor cotnroller to convert -1 to 1 throttle
    values to PWM pulses.
    """
    MIN_THROTTLE = -1
    MAX_THROTTLE = 1

    def __init__(self, controller=None,
                 max_pulse=300,
                 min_pulse=490,
                 zero_pulse=350):

        self.controller = controller
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse

        # send zero pulse to calibrate ESC
        print("Init ESC")
        self.controller.set_pulse(self.max_pulse)
        time.sleep(0.01)
        self.controller.set_pulse(self.min_pulse)
        time.sleep(0.01)
        self.controller.set_pulse(self.zero_pulse)
        time.sleep(1)

    def run(self, throttle):
        if throttle > 0:
            pulse = utils.utils.map_range(throttle,
                                       0, self.MAX_THROTTLE,
                                       self.zero_pulse, self.max_pulse)
        else:
            pulse = utils.utils.map_range(throttle,
                                       self.MIN_THROTTLE, 0,
                                       self.min_pulse, self.zero_pulse)

        self.controller.set_pulse(pulse)

    def shutdown(self):
        self.run(0)  # stop


