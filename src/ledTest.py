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
        # Test Red
        print("Red ON")
        GPIO.output(RED_PIN, GPIO.LOW)  # LOW = ON for common anode
        sleep(2)
        print("Red OFF")
        GPIO.output(RED_PIN, GPIO.HIGH)  # HIGH = OFF
        sleep(1)

        # Test Green
        print("Green ON")
        GPIO.output(GREEN_PIN, GPIO.LOW)
        sleep(2)
        print("Green OFF")
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        sleep(1)

        # Test Blue
        print("Blue ON")
        GPIO.output(BLUE_PIN, GPIO.LOW)
        sleep(2)
        print("Blue OFF")
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        sleep(1)

        # Test White (All Colors ON)
        print("White ON")
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        sleep(2)
        print("White OFF")
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()