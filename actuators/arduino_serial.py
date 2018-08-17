# This file is for actuating the bot using an Arduino connected serially.

import serial


class ArduinoSerial:
    arduino_serial_instance = None

    def __init__(self, portname, baud_rate):
        self.arduino_serial_instance = serial.Serial(portname, baud_rate, timeout=0.1)

    def write_data(self, data_string):
        data = str(data_string)
        self.arduino_serial_instance.write(bytes(data))
