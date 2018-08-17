import actuators.dynamixel.servo_functions as servos
import config
import actuators.dynamixel.dynamixel_utils as d_utils


def init():
    return servos.enable_port()


def enable(ID):
    return servos.enable_bot(ID)


# enable all the Assigned Servo Motors
def enableAll():
    for ids in config.servoIDArm:
        enable(ids)
        setSpeed(ids, config.servoSpeedArm)


def disable(ID):
    return servos.disable_bot(ID)


def setSpeed(ID, Speed):  # (0-1023)
    return servos.set_speed(ID, Speed)


# writes the Servo Angle Value(UnMapped)
def setAngle(ID, Angle):  # ( _ , 0-1023)
    return servos.write_pos(ID, Angle)


# Writes the Angle to the Mapped Servo Accepted Values
def setTransformedAngle(index, Angle):  # (_,0-360)
    return setAngle(config.servoIDArm[index], d_utils.transform2ServoAngles(Angle, index))


# gets the Servo Angle Value (Unmapped)
def getAngle(ID):
    return servos.read_pos(ID, 0)


# gets Mapped Angle Values from Servo Received Values
def getAngleTransformed(index):  # (0-360)
    # Apply the Transformation
    return d_utils.transform2StandardAngles(getAngle(config.servoIDArm[index]), index)


# Hard-Coded Standard Position for Arm
def setPositionStandard():
    print("Setting Arm Angles as :", config.standardArmAngle[0], config.standardArmAngle[1],
          config.standardArmAngle[2], config.standardArmAngle[3], config.standardArmAngle[4],
          config.standardArmAngle[5])
    setTransformedAngle(0, config.standardArmAngle[0])
    setTransformedAngle(1, config.standardArmAngle[1])
    setTransformedAngle(2, config.standardArmAngle[2])
    setTransformedAngle(3, config.standardArmAngle[3])
    setTransformedAngle(4, config.standardArmAngle[4])
    setTransformedAngle(5, config.standardArmAngle[5])


def setPositionTopView():
    pass


def gripEnable():
    setSpeed(5, config.servoGripperSpeed)
    setTransformedAngle(5, config.GRIPCLOSE)


def gripDisable():
    setSpeed(5, config.servoGripperSpeed)
    setTransformedAngle(5, config.GRIPOPEN)
