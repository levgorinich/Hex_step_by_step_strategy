import pygame
from pygame import QUIT

from Map import Map
from MouseClickHandler import MouseClickHandler
from Render import Render
from User_interface import UI
from mapMovement import MapMovementTracker
from mover import Mover
from internet_acsess.network import Network
from Spawner import Spawner
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
game_map = Map(25, 25)
mover = Mover(game_map)
Spawner = Spawner(game_map)
user_interface = UI(window_size, game_map)
tracker = MapMovementTracker(internal_surface_size, window_size, )
renderer = Render(internal_surface_size, map_movement_tracker=tracker, user_interface=user_interface)
click_handler = MouseClickHandler(game_map, user_interface, tracker, mover)

def parse_moves(move):
    if move.startswith("spawn"):
        move = move.replace("spawn", "")
        idx = move.find("(")
        type = move[:idx]
        coords = move[idx+1:-1]
        coords = coords.split(",")
        coords = tuple(map(int, coords))
        Spawner.spawn_unit(type, coords)
    elif move.startswith("move"):
        move = move.replace("move", "")
        move = move.replace("(", "")
        move = move.replace(")", "")

        coords = move.split(",")
        coords = list(map(int, coords))
        mover.move((coords[0], coords[1]), (coords[2], coords[3]))

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
            moves =""
            for move in click_handler.actions:
                # move = str(move)
                # move = move[1:-1]
                # move = "<" + move + ">"
                moves += move
            if moves!="":
                update = n.send(moves)
            else: update = n.send("no_moves")
            click_handler.actions = set()
            if update != "empty":
                for idx, symbol in enumerate(update):
                    start, end = 0, 0
                    if symbol == "<":
                        start = idx
                    if symbol == ">":
                        end = idx
                        parse_moves(update[start+1:end])
                #
                # print(update)
                # print(update[4], update[7], update[12], update[15])
                # start = int(update[4]), int(update[7])
                # end = int(update[12]), int(update[15])
                # mover.move(start, end)
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
