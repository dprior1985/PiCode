import RPi.GPIO as GPIO
import time

#led = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.OUT)


while True:
        GPIO.output(40,GPIO.HIGH)
	print("high")
        time.sleep(1)
        GPIO.output(40,GPIO.LOW)
	print("low")
        time.sleep(1)

