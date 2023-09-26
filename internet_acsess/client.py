import pygame
from pygame import QUIT


from Map import Map

from MouseClickHandler import MouseClickHandler
from Render import Render
from User_interface import UI
from mapMovement import MapMovementTracker
from mover import Mover

from network import Network
from Spawner import Spawner
from MoveParser import Parser


pygame.font.init()
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


# creating window
window_size = (width, height)
screen = pygame.display.set_mode(window_size)

internal_surface_size = (2500, 2500)

# creating main game classes




def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()

    player_id = int(n.getP())
    print("You are player", player_id)

    game_map = Map(25, 25, player_id)
    mover = Mover(game_map)
    spawner = Spawner(game_map)
    move_parser = Parser(mover, spawner)
    user_interface = UI(window_size, game_map)
    tracker = MapMovementTracker(internal_surface_size, window_size, )
    renderer = Render(internal_surface_size, map_movement_tracker=tracker, user_interface=user_interface)
    click_handler = MouseClickHandler(game_map, user_interface, tracker, mover)

    while run:
        clock.tick(60)


        try:

            moves =""
            update = None
            print(game_map.actions)
            for move in game_map.actions:
                moves += move
            if moves!="":
                update = n.send(moves)

            # else:
            #     update = n.send("no_moves")

            game_map.actions = set()

            if update:
                print(update)
                start, end = 0, 0
                for idx, symbol in enumerate(update):


                    if symbol == "<":
                        start = idx
                    if symbol == ">":
                        end = idx

                        move_parser.parse_moves(update[start+1:end])
                        start, end = 0, 0


        except Exception as e :
            print(e)
            run = False
            print("Couldn't get game")
            break

        events_list = pygame.event.get()
        game_map.hexes.update()


        renderer.display(events_list, game_map,click_handler.pos,click_handler.clear,click_handler.check_on_activate)

        pygame.display.flip()

        for event in events_list:
            if event.type == QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handler.handle_click(event)

        clock.tick(60)

    pygame.quit()


main()

