import RPi.GPIO as GPIO
from time import sleep

# Pin Definitions
RED_PIN = 23   # GPIO for Red (update as per your wiring)
GREEN_PIN = 22 # GPIO for Green (update as per your wiring)
BLUE_PIN = 8   # GPIO for Blue (working configuration)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)    # LOW = OFF for common cathode
GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)  # LOW = OFF for common cathode
GPIO.setup(BLUE_PIN, GPIO.OUT, initial=GPIO.LOW)   # LOW = OFF for common cathode

try:
    while True:
        # Red ON
        print("Red ON")
        GPIO.output(RED_PIN, GPIO.HIGH)  # HIGH = ON for common cathode
        GPIO.output(GREEN_PIN, GPIO.LOW) # Ensure other colors are OFF
        GPIO.output(BLUE_PIN, GPIO.LOW)
        sleep(2)

        # Green ON
        print("Green ON")
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)  # HIGH = ON for common cathode
        GPIO.output(BLUE_PIN, GPIO.LOW)
        sleep(2)

        # Blue ON
        print("Blue ON")
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)  # HIGH = ON for common cathode
        sleep(2)

        # White (All Colors ON)
        print("White ON")
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)  # All ON
        sleep(2)

        # All OFF
        print("All OFF")
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()