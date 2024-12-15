import RPi.GPIO as GPIO
import time

# Pin Definitions
RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 27

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

try:
    # Test red
    print("Testing RED")
    GPIO.output(RED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RED_PIN, GPIO.LOW)
    
    # Test green
    print("Testing GREEN")
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    
    # Test blue
    print("Testing BLUE")
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(BLUE_PIN, GPIO.LOW)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()