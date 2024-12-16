from gpiozero import RGBLED
from time import sleep

# Remap Pins to Match Observed Colors
led = RGBLED(red=23, green=22, blue=24, active_high=False)  # Adjust active_high for common anode/cathode

try:
    while True:
        print("Red")
        led.color = (1, 0, 0)  # Red (now mapped to GPIO 23)
        sleep(1)

        print("Green")
        led.color = (0, 1, 0)  # Green (now mapped to GPIO 22)
        sleep(1)

        print("Blue")
        led.color = (0, 0, 1)  # Blue (still GPIO 24)
        sleep(1)

        print("White")
        led.color = (1, 1, 1)  # White (all segments on)
        sleep(1)

        print("Off")
        led.off()
        sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    led.off()