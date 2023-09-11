import pygame
from pygame import QUIT

from Map import Map
from MouseClickHandler import MouseClickHandler
from Render import Render
from User_interface import UI
from mapMovement import MapMovementTracker
from mover import Mover
from network import Network
pygame.font.init()
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


# creating window
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)

internal_surface_size = (2500, 2500)

# creating main game classes
game_map = Map(25, 25)
mover = Mover(game_map)
user_interface = UI(window_size, game_map)
tracker = MapMovementTracker(internal_surface_size, window_size, )
renderer = Render(internal_surface_size, map_movement_tracker=tracker, user_interface=user_interface)
click_handler = MouseClickHandler(game_map, user_interface, tracker, mover)


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)


        try:
            # print("i have sended")
            update = n.send(str(click_handler.actions))
            click_handler.actions = set()
            if update != "empty":
                print(update)
                print(update[9], update[12], update[17], update[20])
                start = int(update[9]), int(update[12])
                end = int(update[17]), int(update[20])
                mover.move(start, end)
            # print(update, "get form server")

            # game = n.send("get")
            # print(game)
        except Exception as e :
            print(e)
            run = False
            print("Couldn't get game")
            break

        events_list = pygame.event.get()
        game_map.hexes.update()

        renderer.display(events_list, game_map)
        pygame.display.flip()

        for event in events_list:
            if event.type == QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handler.handle_click(event)

        clock.tick(60)

    pygame.quit()












main()
