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
logging.basicConfig(filename="server.log", level=logging.DEBUG)



games = {}


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
    main_socket.listen()
    print("Waiting for a connection, Server Started")
    await listening_for_connection(main_socket, asyncio.get_event_loop())

connected = set()
games = {}
idCount = 0

async def get_client_move(p: int, gameID: int, conn: socket.socket, loop: AbstractEventLoop, open_games = None):

    global idCount
    game = games[gameID]
    conn.send(str.encode(str(p)+ " "+ str(game.seed) + " " + str(game.max_players)))
    print("send starting data ")
    reply = ""
    while True:
        try:
            data=  await asyncio.wait_for(loop.sock_recv(conn,4096), 1)
            # print(data =="")
            # print(type(data))
            data = data.decode()

        except asyncio.exceptions.TimeoutError:
            conn.close()
            game.remove_player(p)
            games.pop(gameID)
            if game == open_games[0]:
                open_games.pop()
            # print("Timeout")


        # print(data)
        if gameID in games:
            game = games[gameID]
            if not data:
                print("Lost connection")
                conn.close()
                game.remove_player(p)
                games.pop(gameID)
                if game == open_games[0]:
                    open_games.pop()
                break

            else:
                # print(comands)
                if data != "no_moves":
                    # print(data)

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



async def listening_for_connection(main_socket, loop: AbstractEventLoop):

    global game_with
    connected = set()
    open_games = []
    idCount = 0
    gameIDCount = 0
    while True:
        conn, addr = await loop.sock_accept(main_socket)
        conn.setblocking(False)
        print("Connected to: " + addr[0] + ":" + str(addr[1]))
        idCount +=1




        print(open_games)
        if not open_games:
            print("createing player 0")
            p= 0
            gameIDCount+=1

            gameID = gameIDCount
            seed = random.randint(0,4000)
            game= Game(gameID, seed, 3)
            game.add_player(p)
            games[gameID] = game
            open_games.append(games[gameID])
            print("Created Game ID: ", gameID)
        else :

            p= len(open_games[0].players)
            print("Created player 1", p)
            open_games[0].add_player(p)
            if p == open_games[0].max_players -1:
                open_games.pop()
        print(open_games)


        asyncio.create_task(get_client_move(p, gameIDCount, conn, loop, open_games))



asyncio.run(main(), debug = True)