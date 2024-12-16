from gpiozero import RGBLED
from time import sleep

# Updated Pin Mapping
led = RGBLED(red=24, green=22, blue=23, active_high=False)  # Adjust pins and active_high as needed

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
        led.off()
        sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    led.off()