import RPi.GPIO as GPIO
from time import sleep

# Pin Definitions
RED_PIN = 23
GREEN_PIN = 22
BLUE_PIN = 24

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

try:
    while True:
        # Test Red Only
        print("Testing Red")
        GPIO.output(RED_PIN, GPIO.LOW)  # LOW for common anode, HIGH for common cathode
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        sleep(2)

        # Test Green Only
        print("Testing Green")
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        sleep(2)

        # Test Blue Only
        print("Testing Blue")
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        sleep(2)

        # Turn Everything OFF
        print("All Off")
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()