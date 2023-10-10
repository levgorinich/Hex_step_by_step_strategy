import sys
import pygame
from time import sleep
from pygame.locals import *
import logging

from Offline_Player import OfflinePlayer
from internet_acsess.network import Network
from main_components.Map import Map
from main_components.MouseClickHandler import MouseClickHandler
from main_components.Render import Render
from main_components.User_interface import UI
from main_components.mapMovement import MapMovementTracker
from player_actions.Buttons import MenuButton
from player_actions.MoveParser import Parser
from player_actions.Spawner import Spawner
from player_actions.mover import Mover
from main_components.Player import Player
from collections import deque
#
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
pygame.init()
clock = pygame.time.Clock()

# creating window
# window_size = (1280, 720)
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)

internal_surface_size = (2500, 2500)


# creating main game classes


# main loop
def offline_game():
    players = deque()
    for id in range(2):
        players.append(OfflinePlayer(window_size, internal_surface_size,id))


    player = players.popleft()
    players.append(player)
    player.player.start_turn()

    running = True
    while running:
        if not player.player.cur_turn:

            update = str(player.game_map.actions)
            player.game_map.actions = []
            print(update)

            player = players.popleft()
            players.append(player)
            player.player.start_turn()
            if update:

                start, end = 0, 0
                for idx, symbol in enumerate(update):

                    if symbol == "<":
                        start = idx
                    if symbol == ">":
                        end = idx

                        player.move_parser.parse_moves(update[start + 1:end])
                        # print("parsed moves")
                        start, end = 0, 0




        events_list = pygame.event.get()
        player.game_map.hexes.update()

        player.renderer.display(events_list, player.game_map)
        pygame.display.flip()

        for event in events_list:
            if event.type == QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("detected click")
                player.click_handler.handle_click(event)
                # if click_handler.pos is not None:
                #     renderer.cells(click_handler.pos, game_map.hexes.hexes_dict)
                # print("yeagsdf")

        clock.tick(60)

    pygame.quit()


def online_game():
    run = True
    clock = pygame.time.Clock()
    n = Network()

    player_id = int(n.getP())
    seed = n.getSeed()


    print("You are player", player_id)


    game_map = Map(25, 25, player_id, seed)

    player = Player(player_id,game_map )

    if player.id == 0:
        player.start_turn()
    mover = Mover(game_map)
    spawner = Spawner(game_map,)
    move_parser = Parser(mover, spawner, player)
    user_interface = UI(window_size, game_map,player, spawner)
    tracker = MapMovementTracker(internal_surface_size, window_size, )
    renderer = Render(internal_surface_size, map_movement_tracker=tracker, user_interface=user_interface)
    click_handler = MouseClickHandler(game_map, user_interface, tracker, mover)
    counter = 0
    while run:
        clock.tick(60)

        try:

            moves = ""
            update = None
            # print(game_map.actions)
            for move in game_map.actions:
                moves += move
            if moves != "":
                print("sending", moves)
                update = n.send(moves)

            else:
                # print("send no_moves")
                update = n.send("no_moves")
            counter+=1
            # if counter == 10:
                # sleep(2)
            # print("update", update)
            # print("game_map.actions", game_map.actions)
            game_map.actions = []

            if update:

                start, end = 0, 0
                for idx, symbol in enumerate(update):

                    if symbol == "<":
                        start = idx
                    if symbol == ">":
                        end = idx

                        move_parser.parse_moves(update[start + 1:end])
                        # print("parsed moves")
                        start, end = 0, 0


        except Exception as e:
            print("this is my exception")
            print(e)
            run = False
            # print("Couldn't get game")
            break

        events_list = pygame.event.get()
        game_map.hexes.update()

        renderer.display(events_list, game_map,)

        pygame.display.flip()

        for event in events_list:
            if event.type == QUIT:
                print("Quitting")
                n.close()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handler.handle_click(event)

        clock.tick(60)

    pygame.quit()


def game_menu():
    running = True

    def stop_menue():
        nonlocal running
        running = False

    while running:
        screen.fill((255, 255, 255))
        offline_game_button = MenuButton("Offline Game", 100, 100, 200, 50, offline_game, color=(0, 0, 255),
                                         font_size=24, font_name="Arial")
        online_game_button = MenuButton("Online Game", 300, 400, 200, 50, online_game, color=(0, 0, 255), font_size=24,
                                        font_name="Arial")
        exit_button = MenuButton("Exit", 100, 400, 200, 50, stop_menue, color=(0, 0, 255), font_size=24,
                                 font_name="Arial")

        buttons = [offline_game_button, online_game_button, exit_button]

        for button in buttons:
            button.draw(screen)
            button.check_click()

        events_list = pygame.event.get()

        pygame.display.flip()
        for event in events_list:
            if event.type == QUIT:
                running = False

        if not running:
            pygame.quit()


game_menu()
