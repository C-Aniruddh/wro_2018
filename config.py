import numpy as np

# Video
FPS = 30
CAMERA_ID = 0

# Serial
ARDUINO_SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

# 3x3
"""
cameraMatrix = np.array([[807.436816003674, 0., 0.],
                         [2.03900754532943, 807.610112298853, 0.],
                         [302.651456007652, 263.724593595848, 1.]])
"""

cameraMatrix = np.array([[403.206093743095, 0., 0.],
                         [-0.386960119299221, 400.466365169370, 0.],
                         [173.417201658237, 121.310110904374, 1.]])

# 5 values
distortionCoeffs = np.array([1.87840399e-01, -1.34123291e+00, 1.21747252e-03, -2.00202920e-03, 2.23674740e+00])

# 3 values
rvct = np.array([-0.10056308, 0.00848036, 1.59080042])

# 3 values
tvct = np.array([37.47226676, -68.12233158, 256.68262234])

# whatever unit is chosen here, the coordinates will be in the same unit
distance_cam = 24.4

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
