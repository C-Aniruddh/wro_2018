import config
import actuators.dynamixel.super_servo_functions as super
import actuators.dynamixel.forwardK as kf
import actuators.dynamixel.dynamixel_utils as d_utils

SERVO_SPEED = 350

if __name__ == "__main__":
    super.init()

    super.enable(6)
    super.enable(7)
    super.enable(16)
    super.enable(11)
    super.enable(9)
    super.enable(8)

    super.setSpeed(6, SERVO_SPEED)
    super.setSpeed(7, SERVO_SPEED)
    super.setSpeed(16, SERVO_SPEED)
    super.setSpeed(11, SERVO_SPEED)
    super.setSpeed(9, SERVO_SPEED)
    super.setSpeed(8, SERVO_SPEED)

    while True:
        a0 = float(input("Enter Angle0:"))
        a1 = float(input("Enter Angle1:"))
        a2 = float(input("Enter Angle2:"))
        a3 = float(input("Enter Angle3:"))
        a4 = float(input("Enter Angle4:"))
        a5 = float(input("Enter Angle5:"))

        kf.process(a0, a1, a2, a3, a4)

        # print("Transformed Servo Angle Values are:")
        tfa0 = d_utils.transform2ServoAngles(a0, 0)
        tfa1 = d_utils.transform2ServoAngles(a1, 1)
        tfa2 = d_utils.transform2ServoAngles(a2, 2)
        tfa3 = d_utils.transform2ServoAngles(a3, 3)
        tfa4 = d_utils.transform2ServoAngles(a4, 4)
        tfa5 = d_utils.transform2ServoAngles(a5, 5)

        # print(tfa0,tfa1,tfa2,tfa3,tfa4)

        a = input("Enter Any Key to Upload 2 Servo ")

        super.setAngle(6, tfa0)
        super.setAngle(7, tfa1)
        super.setAngle(16, tfa2)
        super.setAngle(11, tfa3)
        super.setAngle(9, tfa4)
        super.setAngle(8, tfa5)

        super.setAngle(8, tfa5)
        super.setAngle(9, tfa4)
        super.setAngle(11, tfa3)
        super.setAngle(16, tfa2)
        super.setAngle(7, tfa1)
        super.setAngle(6, tfa0)
