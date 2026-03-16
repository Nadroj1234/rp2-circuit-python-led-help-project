import board
import digitalio
import neopixel
import time

# define the led strip
NUM_PIXELS = 24
pixels = neopixel.NeoPixel(board.GP4, NUM_PIXELS, brightness=0.02, auto_write=False, pixel_order=neopixel.GRB)

#define the button 
button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

last_state = button.value

# Define colors / states
OFF = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

colors = [OFF, GREEN, BLUE, RED, "FLASH_RED"]

count = 0
rainbow_running = False
press_start = None

# Theater chase tracking
rapid_press_count = 0
last_press_time = 0
RAPID_PRESS_WINDOW = 1.5   # seconds between presses to count as "rapid"
THEATER_CHASE_THRESHOLD = 15

pixels.fill(OFF)
pixels.show()


def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


def rainbow_mode():
    global rainbow_running
    rainbow_running = True

    while rainbow_running:
        for j in range(255):

            # stop rainbow if button pressed
            if not button.value:
                time.sleep(0.2)  # debounce
                pixels.fill(OFF)
                pixels.show()
                rainbow_running = False
                return

            for i in range(NUM_PIXELS):
                pixel_index = (i * 256 // NUM_PIXELS) + j
                pixels[i] = wheel(pixel_index & 255)

            pixels.show()
            time.sleep(0.01)


def police_mode():
    while True:

        # red left, blue right
        for i in range(NUM_PIXELS):
            if i < NUM_PIXELS // 2:
                pixels[i] = RED
            else:
                pixels[i] = BLUE
        pixels.show()
        time.sleep(0.15)

        if not button.value:
            pixels.fill(OFF)
            pixels.show()
            return

        # swap sides
        for i in range(NUM_PIXELS):
            if i < NUM_PIXELS // 2:
                pixels[i] = BLUE
            else:
                pixels[i] = RED
        pixels.show()
        time.sleep(0.15)

        if not button.value:
            pixels.fill(OFF)
            pixels.show()
            return


def theater_chase_mode():
    """Classic theater chase: every 3rd pixel lights up and shifts forward."""
    CHASE_COLOR = (255, 165, 0)  # Orange — change to any color you like
    CHASE_DELAY = 0.08

    print("Theater Chase started!")

    while True:
        for offset in range(3):
            # Turn all off
            pixels.fill(OFF)

            # Light every 3rd pixel starting at offset
            for i in range(offset, NUM_PIXELS, 3):
                pixels[i] = CHASE_COLOR

            pixels.show()
            time.sleep(CHASE_DELAY)

            # Exit if button pressed
            if not button.value:
                time.sleep(0.2)  # debounce
                pixels.fill(OFF)
                pixels.show()
                print("Theater Chase stopped.")
                return


def pacman_mode():
    PACMAN_YELLOW = (255, 255, 0)
    PELLET_COLOR = (255, 255, 255)
    pacman_pos = 0
    pellet_pos_1 = 2
    pellet_pos_2 = 4
    pellet_pos_3 = 6
    pellet_pos_4 = 8
    pellet_pos_5 = 10
    ghost_pos_1 = 12
    pellet_pos_6 = 14
    ghost_pos_2 = 16
    pellet_pos_7 = 18
    pellet_pos_8 = 20
    ghost_pos_3 = 22




    while True:
        pixels.fill(OFF)
        pixels[pacman_pos] = PACMAN_YELLOW
        pixels[pellet_pos_1] = PELLET_COLOR 
        pixels[pellet_pos_2] = PELLET_COLOR
        pixels[pellet_pos_3] = PELLET_COLOR
        pixels[pellet_pos_4] = PELLET_COLOR
        pixels[pellet_pos_5] = PELLET_COLOR
        pixels[pellet_pos_6] = PELLET_COLOR
        pixels[pellet_pos_7] = PELLET_COLOR
        pixels[pellet_pos_8] = PELLET_COLOR
        pixels[ghost_pos_1] = (255, 0, 0)
        pixels[ghost_pos_2] = (0, 0, 255)
        pixels[ghost_pos_3] = (0, 255, 0)
        pixels.show()
        time.sleep(0.05)


        if not button.value:
            while True:
                time.sleep(0.2)
                pixels[pacman_pos] = OFF
                pacman_pos += 1
                pixels[pacman_pos] = PACMAN_YELLOW
                pixels.show()
                if pacman_pos == 23:
                    pixels.fill(OFF)
                    pixels.show()
                    return



while True:

    current_state = button.value

    # BUTTON PRESSED
    if last_state and not current_state:
        press_start = time.monotonic()

    # BUTTON RELEASED
    if not last_state and current_state:
        press_length = time.monotonic() - press_start
        now = time.monotonic()

        if press_length >= 10:
            print("Starting Police Lights")
            rapid_press_count = 0
            police_mode()

        elif 6.5 <= press_length < 8.5:   # ~7s window 
            print("Starting Pacman")
            rapid_press_count = 0
            pacman_mode()

        elif 5 <= press_length < 10:      # Rainbow catches everything else in 5-10s
            print("Starting rainbow")
            rapid_press_count = 0
            rainbow_mode()

        else:
            # --- Rapid press counter for Theater Chase ---
            if now - last_press_time <= RAPID_PRESS_WINDOW:
                rapid_press_count += 1
            else:
                rapid_press_count = 1  # reset, this is the first press in a new window

            last_press_time = now

            if rapid_press_count >= THEATER_CHASE_THRESHOLD:
                rapid_press_count = 0  # reset after triggering
                count = 0             # reset color state too
                pixels.fill(OFF)
                pixels.show()
                theater_chase_mode()

            else:
                count = (count + 1) % len(colors)
                state = colors[count]

                print(f"Button pressed ({rapid_press_count}/{THEATER_CHASE_THRESHOLD}), new state:", state)

                # Skip FLASH_RED while building up rapid presses to avoid getting stuck
                if state == "FLASH_RED" and rapid_press_count > 1:
                    # Don't enter flash loop mid-sequence; just keep lights off
                    pixels.fill(OFF)
                    pixels.show()

                elif state == "FLASH_RED":
                    while True:
                        pixels.fill(OFF)
                        pixels.show()
                        time.sleep(0.2)

                        pixels.fill(RED)
                        pixels.show()
                        time.sleep(0.2)

                        if not button.value:
                            time.sleep(0.2)
                            pixels.fill(OFF)
                            pixels.show()
                            rapid_press_count = 0  # reset — sequence broken by hold
                            break

                else:
                    pixels.fill(state)
                    pixels.show()

    last_state = current_state
    time.sleep(0.01)