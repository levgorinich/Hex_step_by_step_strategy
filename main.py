import sys
import pygame
from pygame.locals import *

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
#
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
    game_map = Map(25, 25, 0)
    mover = Mover(game_map)
    user_interface = UI(window_size, game_map)
    tracker = MapMovementTracker(internal_surface_size, window_size, )
    renderer = Render(internal_surface_size, map_movement_tracker=tracker, user_interface=user_interface)
    click_handler = MouseClickHandler(game_map, user_interface, tracker, mover)
    running = True
    while running:

        events_list = pygame.event.get()
        game_map.hexes.update()

        renderer.display(events_list, game_map, click_handler.pos, click_handler.clear, click_handler.check_on_activate)
        pygame.display.flip()

        for event in events_list:
            if event.type == QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handler.handle_click(event)
                # if click_handler.pos is not None:
                #     renderer.cells(click_handler.pos, game_map.hexes.hexes_dict)
                # print("yeag")

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
    while run:
        clock.tick(60)

        try:

            moves = ""
            update = None
            # print(game_map.actions)
            for move in game_map.actions:
                moves += move
            if moves != "":
                update = n.send(moves)

            else:
                update = n.send("no_moves")
            game_map.actions = set()

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

        renderer.display(events_list, game_map, click_handler.hexes_available_move_selected_unit,
                         click_handler.clear, click_handler.check_on_activate)

        pygame.display.flip()

        for event in events_list:
            if event.type == QUIT:
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
