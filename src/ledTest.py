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
    print("Testing RED")
    GPIO.output(RED_PIN, GPIO.LOW)  # LOW = ON for common anode
    sleep(1)
    GPIO.output(RED_PIN, GPIO.HIGH)  # HIGH = OFF
    sleep(1)

    print("Testing GREEN")
    GPIO.output(GREEN_PIN, GPIO.LOW)
    sleep(1)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    sleep(1)

    print("Testing BLUE")
    GPIO.output(BLUE_PIN, GPIO.LOW)
    sleep(1)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    sleep(1)

    print("WHITE (All Colors ON)")
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    sleep(2)

    print("OFF")
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()