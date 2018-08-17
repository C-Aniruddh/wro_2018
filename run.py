from block_recognition import BlockRecognition
from actuators.arduino_serial import ArduinoSerial
from actuators.servos.normal_pca9685 import PWMServo
from inverse import perform_inverse
from img2world import undistort
import config
import threading

"""
    * Create objects of the required actuators / sensors 
    * Centralize all config parameters to config.py for easy changes
    * Extend classes based on more components (modular structure)
"""

br = BlockRecognition(camera_id=config.CAMERA_ID, optimal_fps=config.FPS)
# arduino_actuator = ArduinoSerial(portname=config.ARDUINO_SERIAL_PORT, baud_rate=config.BAUD_RATE)

br.run()


# Select a point and perform inverse based on arm design
