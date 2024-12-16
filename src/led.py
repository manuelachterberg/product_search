from gpiozero import RGBLED
from time import sleep

# Pin Definitions (adjust as per your setup)
led = RGBLED(red=22, green=23, blue=8, active_high=False)  # active_high=False for common cathode

try:
    while True:
        # Red ON
        print("Red ON")
        led.color = (1, 0, 0)  # Red
        sleep(2)

        # Green ON
        print("Green ON")
        led.color = (0, 1, 0)  # Green
        sleep(2)

        # Blue ON
        print("Blue ON")
        led.color = (0, 0, 1)  # Blue
        sleep(2)

        # White (All Colors ON)
        print("White ON")
        led.color = (1, 1, 1)  # White (all ON)
        sleep(2)

        # All OFF
        print("All OFF")
        led.off()
        sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
    led.off()  # Turn off the LED on exit