import serial
ArduinoSerial = serial.Serial('/dev/ttyACM1', 9600, timeout=.1)

while True:
    input_data = str(input('Enter your command : '))
    input_data = input_data.encode('utf-8')
    ArduinoSerial.write(bytes(input_data))
