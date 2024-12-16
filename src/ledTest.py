import RPi.GPIO as GPIO
from time import sleep

# Pin Definitions
RED_PIN = 22  # Replace if necessary
GREEN_PIN = 23  # Replace if necessary
BLUE_PIN = 24  # Replace if necessary

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

try:
    print("Testing Red")
    GPIO.output(RED_PIN, GPIO.LOW)  # LOW for common anode, HIGH for common cathode
    sleep(2)
    GPIO.output(RED_PIN, GPIO.HIGH)
    
    print("Testing Green")
    GPIO.output(GREEN_PIN, GPIO.LOW)
    sleep(2)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    
    print("Testing Blue")
    GPIO.output(BLUE_PIN, GPIO.LOW)
    sleep(2)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")
finally:
    GPIO.cleanup()