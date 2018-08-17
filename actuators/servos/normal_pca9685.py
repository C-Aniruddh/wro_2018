import utils.utils


class PWMServo:

    zero_ANGLE = 0
    full_ANGLE = 180

    def __init__(self, controller=None,
                 zero_pulse=290,
                 full_pulse=490):
        self.controller = controller
        self.zero_pulse = zero_pulse
        self.full_pulse = full_pulse

    def run(self, angle):

        pulse = utils.utils.map_range(angle,
                                      self.zero_ANGLE, self.full_ANGLE,
                                      self.zero_pulse, self.zero_pulse)

        self.controller.set_pulse(pulse)

    def shutdown(self):
        self.run(0)
