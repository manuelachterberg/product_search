from gpiozero import RGBLED

class RGBLEDController:
    def __init__(self, red_pin, green_pin, blue_pin, active_high=True):
        """
        Initialize the RGB LED with the given GPIO pins.
        
        Args:
            red_pin (int): GPIO pin for the red LED.
            green_pin (int): GPIO pin for the green LED.
            blue_pin (int): GPIO pin for the blue LED.
            active_high (bool): Set to False for common anode LEDs.
        """
        self.led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin, active_high=active_high)

    def set_color(self, red, green, blue):
        """
        Set the color of the RGB LED.
        
        Args:
            red (float): Intensity of the red LED (0 to 1).
            green (float): Intensity of the green LED (0 to 1).
            blue (float): Intensity of the blue LED (0 to 1).
        """
        self.led.color = (red, green, blue)

    def off(self):
        """Turn off the RGB LED."""
        self.led.off()

    def cleanup(self):
        """Cleanup the GPIO resources."""
        self.led.close()