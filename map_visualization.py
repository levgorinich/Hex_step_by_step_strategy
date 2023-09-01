import sys
import pygame
from pygame.locals import *
from Map import Map
from MouseClickHandler import MouseClickHandler
from Render import Render
from mapMovement import MapMovementTracker
from User_interface import UI


#
pygame.init()
clock = pygame.time.Clock()

#creating window
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)

internal_surface_size = (2500,2500)

# creating main game classes
game_map = Map(25,25)
user_interface = UI(window_size, game_map)
tracker = MapMovementTracker(internal_surface_size, window_size, )
renderer = Render(internal_surface_size, map_movement_tracker=tracker, user_interface=user_interface)
click_handler = MouseClickHandler(game_map, user_interface, tracker)

# main loop
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