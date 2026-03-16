# PACMAN MODE CODE
'''function that runs the pacman mode
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





add this elif under the police lights if statement and above the rainbow elif. 
elif 6.5 <= press_length < 8.5:   # ~7s window 
            print("Starting Pacman")
            rapid_press_count = 0
            pacman_mode()
'''