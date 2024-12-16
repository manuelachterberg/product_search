from gpiozero import RGBLED
from time import sleep

# Initialize RGBLED
led = RGBLED(red=22, green=23, blue=24, active_high=False)  # Set active_high based on LED type

try:
    while True:
        print("Red")
        led.color = (1, 0, 0)  # Red
        sleep(1)
        
        print("Green")
        led.color = (0, 1, 0)  # Green
        sleep(1)
        
        print("Blue")
        led.color = (0, 0, 1)  # Blue
        sleep(1)
        
        print("White")
        led.color = (1, 1, 1)  # White
        sleep(1)
        
        print("Off")
        led.off()  # Turn off the LED
        sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    led.off()  # Ensure LED is off on exit