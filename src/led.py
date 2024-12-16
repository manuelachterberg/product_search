from gpiozero import RGBLED
from time import sleep

# Pin Definitions (adjust if needed)
led = RGBLED(red=22, green=23, blue=8, active_high=True)  # Default active_high=True for common cathode

try:
    while True:
        print("Red")
        led.color = (1, 0, 0)  # Red
        sleep(2)

        print("Green")
        led.color = (0, 1, 0)  # Green
        sleep(2)

        print("Blue")
        led.color = (0, 0, 1)  # Blue
        sleep(2)

        print("Off")
        led.off()
        sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
    led.off()