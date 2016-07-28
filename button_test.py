import RPi.GPIO as GPIO
import time

#True inverts the button state. My button is always on, and dpresses to false.
def_state = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.OUT, initial=GPIO.HIGH)

while True:
	state = (GPIO.input(18) != def_state)
	if not state:
		print('POW!')
		GPIO.output(21, (GPIO.HIGH))
		time.sleep(1)
	GPIO.output(21, GPIO.LOW)
