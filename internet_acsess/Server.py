import pickle
import socket
from _thread import *
# from asyncio import get_event_loop
from asyncio import AbstractEventLoop
import asyncio
import random
from  OnServer import Game
import  time
import logging
import json
logging.basicConfig(filename="server.log", level=logging.DEBUG)



games_open = {}
ta = 0 # game id count


def create_game(players_amount, size):
    global ta
    game_id = ta
    ta += 1

    seed = random.randint(0,4000)
    game= Game(game_id, seed, players_amount, size)
    p = game.add_player()
    games_open[game_id] = game
    return p




async def main():

    server =  "localhost" #"192.168.1.9"
    port = 5555
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # disable Nagle algorithm
    main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    main_socket.setblocking(False)
    try:
        main_socket.bind((server, port))
    except socket.error as e:
        str(e)

# main_socket.setblocking(False)

    main_socket.listen(5)
    print("Waiting for a connection, Server Started")
    await listening_for_connection(main_socket, asyncio.get_event_loop())

connected = set()
games_open = {}
idCount = 0

async def get_client_move(p: int, gameID: int, conn: socket.socket, loop: AbstractEventLoop,):

    global idCount
    game = games_open[gameID]
    run = True
    while run:
        client_connect = await loop.sock_recv(conn, 4096)
        client_connect = client_connect.decode()
        if client_connect == "join game":
            data_to_client = {"player_number": p, "game_info": game.get_dict_for_client()}
            conn.send(str.encode(json.dumps(data_to_client)))
            run = False
    print("send starting data ")
    while True:
        try:
            data=  await asyncio.wait_for(loop.sock_recv(conn,4096), 1)
            # print(data =="")
            # print(type(data))
            data = data.decode()

        except asyncio.exceptions.TimeoutError:
            conn.close()
            game.remove_player(p)
            print("Timeout")
            games_open.pop(gameID)

        if gameID in games_open:
            game = games_open[gameID]
            if not data:
                print("Lost connection")
                conn.close()
                game.remove_player(p)
                games_open.pop(gameID)
                break
            else:
                if data != "no_moves":
                    for key in game.comands:
                        if key != p:
                            game.comands[key] += data

                comands_to_send = game.comands[p]
                if comands_to_send == "":
                    comands_to_send = "empty"
                # print(comands_to_send)
                await loop.sock_sendall(conn, str.encode(comands_to_send))
                game.comands[p] = ""

    print("stop  a loop", data)

async def client_room_selection(conn: socket.socket, loop: AbstractEventLoop, player_id: int):

    conn.send(str.encode(str(player_id)))

    run = True
    while run:
        data_from_client = await loop.sock_recv(conn, 4096)

        data_from_client = data_from_client.decode()
        data_from_client = json.loads(data_from_client)

        print("recieving ", data_from_client)
        action = list(data_from_client.keys())[0]
        print("this is action")
        data_from_client = data_from_client[action]
        if  action == "get_open_games":
            print("In get open games ")

            games_created  = {game_id : games_open[game_id].get_dict_for_room_selection() for game_id in games_open}
            print(games_created)
            await loop.sock_sendall(conn, str.encode(json.dumps(games_created)))

        if action == "enter_room":
            print("get in join game")

            game_id = int(data_from_client["game_id"])
            game = games_open[game_id]

            await loop.sock_sendall(conn, str.encode("ok"))

            player_id = game.add_player()
            run = False
            asyncio.create_task(get_client_move(player_id, game_id, conn, loop))

        if action == "create_room":
            players_amount = data_from_client["players_amount"]
            map_size = data_from_client["map_size"]

            player_id = create_game(players_amount = players_amount, size= map_size)
            await loop.sock_sendall(conn, str.encode(str(ta-1)))
            run = False
            asyncio.create_task(get_client_move(player_id, ta-1, conn, loop))



async def listening_for_connection(main_socket, loop: AbstractEventLoop):

    global game_with

    idCount = 0

    while True:
        conn, addr = await loop.sock_accept(main_socket)
        conn.setblocking(False)
        print("Connected to: " + addr[0] + ":" + str(addr[1]))
        idCount +=1

        # asyncio.create_task(get_client_move(p, gameIDCount, conn, loop, open_games))
        p = idCount
        asyncio.create_task(client_room_selection(conn, loop, p))



asyncio.run(main(), debug = True)