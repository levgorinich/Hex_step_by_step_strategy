import sys

import pygame
from pygame.locals import *
from math import *
# from some_russian_gay_m.Groups import CameraGroup
from some_russian_gay_m.Map import Map
from some_russian_gay_m.MouseClickHandler import MouseClickHandler
from some_russian_gay_m.Render import Render
from mapMovement import MapMovementTracker
pygame.init()
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
# pygame.event.set_grab(True)
pygame.display.set_caption("Drawing Polygons on a Sprite")
clock = pygame.time.Clock()
internal_surface = pygame.Surface((2500, 2500),pygame.SRCALPHA)

# diagonal size of hexagon = 2a , where a is the radius of hexagon, or it's side length

game_map = Map(25,25)
tracker = MapMovementTracker(internal_surface.get_size(), pygame.display.get_surface().get_size())
renderer = Render(map_movement_tracker=tracker, internal_surface=internal_surface)
click_handler = MouseClickHandler(game_map, tracker)

unit_mover=False
running = True
while running:

    events_list = pygame.event.get()

    game_map.hexes.update()
    # screen.fill('#71deee')
    renderer.pre_display(events_list)
    renderer.display_objects(game_map.hexes)
    renderer.display_units(game_map.units, game_map.hexes.hexes_dict)
    renderer.display()

    # renderer.display_objects(game_map.hexes)
    pygame.display.flip()

    for event in events_list:
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
this is test
            click_handler.handle_click(event)

    clock.tick(60)

pygame.quit()