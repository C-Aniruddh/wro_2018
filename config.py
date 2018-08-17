import numpy as np

"""
    Config File. Define all ports here so it is easier to change them later on
"""

# Video
FPS = 30
CAMERA_ID = 1

# Serial
ARDUINO_SERIAL_PORT = "/dev/tty"
BAUD_RATE = 9600
DYNAMIXEL_PORT = ""

# Camera Configuration
# Get these values from calibration file.

# 3x3

cameraMatrix = np.array([[807.436816003674, 0., 0.],
                         [2.03900754532943, 807.610112298853, 0.],
                         [302.651456007652, 263.724593595848, 1.]])

# 5 values
distortionCoeffs = np.array([1.87840399e-01, -1.34123291e+00, 1.21747252e-03, -2.00202920e-03, 2.23674740e+00])

# 3 values
rvct = np.array([-0.10056308, 0.00848036, 1.59080042])

# 3 values
tvct = np.array([37.47226676, -68.12233158, 256.68262234])

# whatever unit is chosen here, the coordinates will be in the same unit
distance_cam = 270  # cm

# Dynamixel Library
dxl_lib = "/home/eshita/DynamixelSDK/c/build/linux64/libdxl_x64_c.so"
ttyUSB_USB2DYNAMIXEL = "/dev/ttyUSB3"
CP2102 = ""
CP_BAUDRATE = 0
ENABLE_CP_DEBUG = True
ENABLE_DEBUG_MESSAGES = True
ENABLE_KINEMATIC_DEBUG_MESSAGES_MAT = False
ENABLE_KINEMATIC_DEBUG_MESSAGES_RES = True

servoSpeed = 200
servoSpeedArm = 200
servoSpeedStack = 200
servoSpeedCentre = 200
servoGripperSpeed = 350

# Gripper Angles
GRIPCLOSE = 150
GRIPOPEN = 240

# Unique IDs for Each Servo

servoIDArm = [6, 7, 16, 11, 9, 8]  # in ascending order from the bottom most Servo

# servoIdGripper =

# Standard Position ARM angles
standardArmAngle = [0, 0, 0, 0, 0, 0]  # in ascending order from the bottom most Servo
