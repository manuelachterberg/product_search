import RPi.GPIO as GPIO
import time

# GPIO setup
RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Set up PWM
red_pwm = GPIO.PWM(RED_PIN, 100)
green_pwm = GPIO.PWM(GREEN_PIN, 100)
blue_pwm = GPIO.PWM(BLUE_PIN, 100)

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

# Function to set RGB color (0-100 for each color)
def set_color(red, green, blue):
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

try:
    while True:
        for i in range(0, 101, 5):
            set_color(i, 100 - i, i)  # Smooth transition
            time.sleep(0.1)
except KeyboardInterrupt:
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()