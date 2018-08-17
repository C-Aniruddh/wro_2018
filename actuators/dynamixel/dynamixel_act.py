import actuators.dynamixel.super_servo_functions as super
import actuators.dynamixel.dynamixel_utils as d_utils
from inverse.perform_inverse import InverseKinematics

SERVO_SPEED = 50


class DynamixelActuator:

    def __init__(self):
        super.init()

        super.enable(6)
        super.enable(7)
        super.enable(16)
        super.enable(11)
        super.enable(9)
        # super.enable(8)

        super.setSpeed(6, SERVO_SPEED)
        super.setSpeed(7, SERVO_SPEED)
        super.setSpeed(16, SERVO_SPEED)
        super.setSpeed(11, SERVO_SPEED)
        super.setSpeed(9, SERVO_SPEED)
        # super.setSpeed(8,SERVO_SPEED)
        self.ik = InverseKinematics()

    def actuate(self, x, y, z):
        a0, a1, a2, a3, a4, isPossible = self.ik.solve(x, y, z)

        if isPossible:
            print("Output Angles are:", a0, a1, a2, a3, a4)

            # print("Transformed Servo Angle Values are:")
            tfa0 = d_utils.transform2ServoAngles(a0, 0)
            tfa1 = d_utils.transform2ServoAngles(a1, 1)
            tfa2 = d_utils.transform2ServoAngles(a2, 2)
            tfa3 = d_utils.transform2ServoAngles(a3, 3)
            tfa4 = d_utils.transform2ServoAngles(a4, 4)

            # print(tfa0,tfa1,tfa2,tfa3,tfa4)

            a = input("Enter Any Key to Upload 2 Servo ")

            super.setAngle(6, tfa0)
            super.setAngle(7, tfa1)
            super.setAngle(16, tfa2)
            super.setAngle(11, tfa3)
            super.setAngle(9, tfa4)
            # super.setAngle(8,tfa4)

        else:
            pass
