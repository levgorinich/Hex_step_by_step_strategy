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
                print(list(filter(lambda x: len(x[0]) == 2, player.game_map.hexes.hexes_dict.key_to_value.items())))
                # if click_handler.pos is not None:
                #     renderer.cells(click_handler.pos, game_map.hexes.hexes_dict)
                # print("yeagsdf")

        clock.tick(60)

    pygame.quit()




def choose_game(testing:bool = False):
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
        network.send(json.dumps({"enter_room": {"game_id": game_id}}))
        online_game( network)


    # def create_room(network: Network):
    #     print("tried to create room")
    #     game_id = network.send("create_room")
    #     print("not here")
    #     game_id = int(game_id)
    #     print("create room")
    #     online_game(game_id, network)


    button_size = (200, 50)
    backwards_button = MenuButton("Back", 100, 600, button_dimensions=button_size,  color=(0, 0, 255), font_size=24,)
    create_room_button = MenuButton("Create Room", 300, 600, button_dimensions=button_size, action=game_settings,action_args =  [network],  color=(0, 0, 255), font_size=24, )
    enter_room_button = MenuButton("Enter Room", 500, 600, button_dimensions=button_size,  action = enter_room, action_args = [game_list, network],color=(0, 0, 255), font_size=24,)
    backwards_button.draw(screen)
    create_room_button.draw(screen)
    enter_room_button.draw(screen)

    screen.blit(game_list.upper_surf, (0, 0))
    sleep(1)
    while is_run:
    #
    #     if testing == True:
    #         test_event =(yield)
    #         pygame.event.post(test_event)



        # print("before bliting")
        events_list = pygame.event.get()
        for event in events_list:
            if event.type == QUIT:
                is_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.dict["pos"]
                game_list.check_selection(mouse_pos)
                create_room_button.check_click(mouse_pos)
                enter_room_button.check_click(mouse_pos)

                if backwards_button.check_click(mouse_pos):
                    is_run = False



        pygame.display.flip()
    game_menu()



def game_menu(testing):
    global running
    def stop_menue():
        global running
        running = False

    screen.fill((255, 255, 255))
    button_dimensions = (200, 50)
    offline_game_button = MenuButton("Offline Game", 100, 100, button_dimensions=button_dimensions,
                                     action=offline_game, color=(0, 0, 255),font_size=24, font_name="Arial")
    online_game_button = MenuButton("Online Game", 300, 400, button_dimensions=button_dimensions,
                                    action=choose_game, color=(0, 0, 255), font_size=24,font_name="Arial")
    exit_button = MenuButton("Exit", 100, 400, button_dimensions= button_dimensions,
                             action=stop_menue, color=(0, 0, 255), font_size=24,font_name="Arial")

    buttons = [offline_game_button, online_game_button, exit_button]
    # [button.reset_clickability() for button in buttons]
    for button in buttons:
        button.draw(screen)
    while running:
        # if testing == True:
        #     test_event =(yield)
        #     pygame.event.post(test_event)
        if running:
            events_list = pygame.event.get()

            pygame.display.flip()
            for event in events_list:


                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    print("here")
                    pos = event.dict["pos"]
                    [button.check_click(pos) for button in buttons]

                # elif event.type == MOUSEBUTTONUP:
                #     [button.reset_clickability() for button in buttons]

            if not running:
                print("quitting")
                pygame.quit()
                sys.exit()


game_menu(testing=False)
