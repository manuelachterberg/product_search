from evdev import InputDevice, categorize, ecodes

# Replace with your device's event file
device_path = '/dev/input/by-id/usb-040b_6543-if01-event-kbd'

try:
    device = InputDevice(device_path)
    print(f"Listening for input from {device.name} at {device_path}...")

    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:  # Keyboard event
            key_event = categorize(event)
            if key_event.keystate == 1:  # Key down
                print(f"Scanned: {key_event.keycode}")
except Exception as e:
    print(f"Error: {e}")
