import sys
import pygame
from time import sleep
from pygame.locals import *
import logging
import json

from main_components.Offline_Player import OfflinePlayer
from internet_acsess.network import Network
from main_components.Map import Map
from main_components.MouseClickHandler import MouseClickHandler
from main_components.Render import Render
from main_components.User_interface import UI
from main_components.mapMovement import MapMovementTracker
from player_actions.Buttons import *
from player_actions.MoveParser import Parser
from player_actions.Spawner import Spawner
from player_actions.mover import Mover
from main_components.Player import Player
from collections import deque
from main_components.game import OnlineGame
#
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
pygame.init()
clock = pygame.time.Clock()

# creating window
# window_size = (1280, 720)
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)

internal_surface_size = (2500, 2500)

running = True
# creating main game classes


# main loop
def offline_game():
    players = deque()
    for id in range(3):
        players.append(OfflinePlayer(window_size, internal_surface_size,id))


    player = players.popleft()
    players.append(player)
    player.player.start_turn()
    commands = {i:[] for i in range(3)}

    run = True
    while run:

        if not player.player.cur_turn:

            for key in commands.keys():
                if key != player.player.id:
                    commands[key].append(player.game_map.actions)
            player.game_map.actions = []

            player = players.popleft()
            players.append(player)
            player.player.start_turn()
            update = str(commands[player.player.id])
            commands[player.player.id] = []
            print(update)
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
                run = False
                global running
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("detected click")
                player.click_handler.handle_click(event)
                # if click_handler.pos is not None:
                #     renderer.cells(click_handler.pos, game_map.hexes.hexes_dict)
                # print("yeagsdf")

        clock.tick(60)

    pygame.quit()


def online_game(game_id: int, network: Network):
    run = True
    clock = pygame.time.Clock()

    network.connect_to_game()
    player_id = int(network.getP())
    seed = network.getSeed()
    playrs_amount = int(network.getPlayersAmount())
    print("players amount in main ", playrs_amount)


    print("You are player", player_id)


    game_map = Map(20, 20, player_id, seed, playrs_amount)

    player = Player(player_id,game_map )

    if player.id == 0:
        player.start_turn()
    mover = Mover(game_map)
    spawner = Spawner(game_map,)
    move_parser = Parser(mover, spawner, player, playrs_amount)
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
                update = network.send(moves)

            else:
                # print("send no_moves")
                update = network.send("no_moves")
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
                network.close()
                run = False
                global running
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_handler.handle_click(event)

        clock.tick(60)

    pygame.quit()




def choose_game():
    print("choose game")

    network = Network()
    server_id = int(network.get_server_id())

    open_games=  network.send(json.dumps({"get_open_games": ""}))

    games = json.loads(open_games)

    game_list = ButtonList()
    for game_id in games:

        game = games[game_id]

        print(game)
        onlin_game = OnlineGame(game_id, game["players"], game["max_players"])
        text = str(game["id"]) +" "*10 + str(len(game["players"])) + "/ "+ str(game["max_players"])
        game_list.add_element(text, onlin_game)


    screen.fill((255, 255, 255))

    is_run = True

    def enter_room(game_list, network: Network):
        print("tried to enter room")
        game_id = game_list.selected_element.id
        network.send(json.dumps({"enter_room": game_id}))
        online_game(game_id, network)


    # def create_room(network: Network):
    #     print("tried to create room")
    #     game_id = network.send("create_room")
    #     print("not here")
    #     game_id = int(game_id)
    #     print("create room")
    #     online_game(game_id, network)



    backwards_button = MenuButton("Back", 100, 600, 200, 50,  color=(0, 0, 255), font_size=24,)
    create_room_button = MenuButton("Create Room", 300, 600, 200, 50, action=game_settings,action_args =  [network],  color=(0, 0, 255), font_size=24, )
    enter_room_button = MenuButton("Enter Room", 500, 600, 200, 50,  action = enter_room, action_args = [game_list, network],color=(0, 0, 255), font_size=24,)
    backwards_button.draw(screen)
    create_room_button.draw(screen)
    enter_room_button.draw(screen)

    screen.blit(game_list.surf, (0, 0))

    while is_run:

        create_room_button.check_click()
        enter_room_button.check_click()

        game_list.check_selection()

        # print("before bliting")
        events_list = pygame.event.get()
        for event in events_list:
            if event.type == QUIT:
                is_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_room_button.check_click()
                enter_room_button.check_click()

            if backwards_button.check_click():
                is_run = False



        pygame.display.flip()
    game_menu()


def game_settings(network: Network):
    screen.fill((255, 255, 255))

    def create_room(network: Network):
        print("tried to create room")
        game_dict = {"create_room": {"players_amount": players_amount_list.selected_element, "map_size": map_sizes_list.selected_element}}
        game_id = network.send(json.dumps(game_dict))
        print("not here")
        game_id = int(game_id)
        print("create room")
        online_game(game_id, network)
    start_game = MenuButton("Start Game", 400, 600, 200, 50,action=create_room, action_args = [network],  color=(0, 0, 255), font_size=24,)
    backwards_button = MenuButton("Back", 100, 600, 200, 50,  color=(0, 0, 255), font_size=24,)
    start_game.draw(screen)
    backwards_button.draw(screen)

    map_sizes_list = ButtonList()
    players_amount_list = ButtonList(x_offset=400)
    for amount in [2,3,4,5,6]:
        players_amount_list.add_element(str(amount), amount)
    for size in [(10,10), (20,20), (30,30), (40,40), (50,50)]:
        map_sizes_list.add_element(str(size), size)

    screen.blit(map_sizes_list.surf, (0, 0))
    screen.blit(players_amount_list.surf, (400, 0))


    is_run = True
    while is_run:

        # start_game.check_click()


        events_list = pygame.event.get()
        for event in events_list:
            print("event")
            if event.type == QUIT:
                is_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_game.check_click()
                map_sizes_list.check_selection()
                players_amount_list.check_selection()

                if backwards_button.check_click():
                    is_run = False
                    choose_game()
        pygame.display.flip()




def game_menu():
    global running
    def stop_menue():
        global running
        running = False

    screen.fill((255, 255, 255))
    offline_game_button = MenuButton("Offline Game", 100, 100, 200, 50, action=offline_game, color=(0, 0, 255),
                                     font_size=24, font_name="Arial")
    online_game_button = MenuButton("Online Game", 300, 400, 200, 50, action=choose_game, color=(0, 0, 255), font_size=24,
                                    font_name="Arial")
    exit_button = MenuButton("Exit", 100, 400, 200, 50, action=stop_menue, color=(0, 0, 255), font_size=24,
                             font_name="Arial")

    buttons = [offline_game_button, online_game_button, exit_button]
    # [button.reset_clickability() for button in buttons]
    for button in buttons:
        button.draw(screen)
    while running:




        if running:
            events_list = pygame.event.get()

            pygame.display.flip()
            for event in events_list:
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    [button.check_click() for button in buttons]

                # elif event.type == MOUSEBUTTONUP:
                #     [button.reset_clickability() for button in buttons]

            if not running:
                print("quitting")
                pygame.quit()
                sys.exit()


game_menu()
