import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23

try:
    while True:
         button_state = GPIO.input(23)
         if button_state == False:
             print('Button Pressed...')
             time.sleep(0.2)
except:
    GPIO.cleanup()
