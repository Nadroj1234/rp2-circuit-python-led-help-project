# BASIC COLOR MOOD CODE

''' import board
import digitalio
import neopixel
import time

NUM_PIXELS = 24
pixels = neopixel.NeoPixel(board.GP4, NUM_PIXELS, brightness=0.02, auto_write=False, pixel_order=neopixel.GRB)

button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

last_state = button.value

# Define colors / states
OFF = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

colors = [OFF, GREEN, YELLOW, RED, "FLASH_RED"]  # last state is flashing

count = 0

# Start with all off
pixels.fill(OFF)
pixels.show()

while True:
    current_state = button.value

    # Detect button press (True → False)
    if last_state and not current_state:
        count = (count + 1) % len(colors)
        state = colors[count]

        print("Button pressed, new state:", state)

        if state == "FLASH_RED":
            while True:
                pixels.fill(OFF)
                pixels.show()
                time.sleep(0.2)
                pixels.fill(RED)
                pixels.show()
                time.sleep(0.2)
                current_state = button.value
                if last_state and not current_state:
                    print("stopped")
                    pixels.fill(OFF)
                    pixels.show()
                    break
                



        else:
            # Normal color
            pixels.fill(state)
            pixels.show()

        time.sleep(0.1)  # debounce

    last_state = current_state
    time.sleep(0.01) '''