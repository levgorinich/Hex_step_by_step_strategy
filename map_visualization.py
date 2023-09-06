import sys
import pygame
from pygame.locals import *
from Map import Map
from MouseClickHandler import MouseClickHandler
from Render import Render
from mapMovement import MapMovementTracker
from User_interface import UI
from Buttons import MenuButton

#
pygame.init()
clock = pygame.time.Clock()

# creating window
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)

internal_surface_size = (2500, 2500)

# creating main game classes
game_map = Map(25, 25)
user_interface = UI(window_size, game_map)
tracker = MapMovementTracker(internal_surface_size, window_size, )
renderer = Render(internal_surface_size, map_movement_tracker=tracker, user_interface=user_interface)
click_handler = MouseClickHandler(game_map, user_interface, tracker)


# main loop
def offline_game():
    running = True
    while running:

        events_list = pygame.event.get()
        game_map.hexes.update()

        renderer.display(events_list, game_map)
        pygame.display.flip()

        for event in events_list:
            if event.type == QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handler.handle_click(event)

        clock.tick(60)

    pygame.quit()





def game_menu():
    running = True

    def stop_menue():

        running = False

    while running:
        screen.fill((255, 255, 255))
        offline_game_button = MenuButton("Offline Game", 100, 100, 200, 50, offline_game, color=(0, 0, 255),
                                         font_size=24, font_name="Arial")
        online_game_button = MenuButton("Online Game", 300, 400, 200, 50, offline_game, color=(0, 0, 255), font_size=24,
                                        font_name="Arial")
        exit_button = MenuButton("Exit", 100, 400, 200, 50, stop_menue, color=(0, 0, 255), font_size=24,
                                 font_name="Arial")

        buttons = [offline_game_button, online_game_button, exit_button]

        for button in buttons:
            button.draw(screen)
            running = not button.check_click(offline_game)
            print(running)
            if not running:
                print("i break here")
                break
        print(running, "after breacking ")

        events_list = pygame.event.get()

        pygame.display.flip()
        for event in events_list:
            if event.type == QUIT:
                running = False

        if not running:
            pygame.quit()
            run = False
            #
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     running = False
    # offline_game()



game_menu()
