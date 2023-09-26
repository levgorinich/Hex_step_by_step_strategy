import pickle
import socket
from _thread import *
# from asyncio import get_event_loop
from asyncio import AbstractEventLoop
import asyncio
from  OnServer import Game
import  time


comands = {0: "", 1: "",}
games = {}

async def main():

    server =  "localhost" #"192.168.1.9"
    port = 5555
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # disable Nagle algorithm
    main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
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

async def get_client_move(p: int, gameID: int, conn: socket.socket, loop: AbstractEventLoop):

    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while data :=  await loop.sock_recv(conn,4096):
        print("got data from client")
        data = data.decode()
        print(data)
        if gameID in games:
            print("Game Exists")
            game = games[gameID]
            if not data:
                print("Lost connection")
                break
            else:
                print("I am in else")
                print(comands)
                if data != "no_moves":
                    print(data)
                    for key in comands:
                        if key != p:
                            comands[key] += data

                comands_to_send = comands[p]
                if comands_to_send == "":
                    comands_to_send = "empty"
                print(comands_to_send)
                await loop.sock_sendall(conn, str.encode(comands_to_send))
                comands[p] = ""

    #     else:
    #         break
    # except socket.error as e:
    # pass

async def listening_for_connection(main_socket, loop: AbstractEventLoop):

    connected = set()

    idCount = 0
    while True:
        conn, addr = await loop.sock_accept(main_socket)
        conn.setblocking(False)
        print("Connected to: " + addr[0] + ":" + str(addr[1]))
        idCount +=1
        p=0
        gameID = (idCount-1)//2

        if idCount %2 ==1:
            games[gameID] = Game(gameID)
            print("Created Game ID: ", gameID)
        else :
            p=1
        asyncio.create_task(get_client_move(p, gameID, conn, loop))

asyncio.run(main())
# def threaded_client(conn, p, gameID):
#     global idCount
#     conn.send(str.encode(str(p)))
#
#
#     reply = ""
#     while True:
#         time.sleep(0.1)
#         try:
#             data = conn.recv(4096).decode()
#             if gameID in games:
#                 game = games[gameID]
#                 if not data:
#                     print("Lost connection")
#                     break
#                 else:
#                     print(comands)
#                     if data != "no_moves":
#                         print(data)
#                         for key in comands:
#                             if key != p:
#                                 comands[key] += data
#
#                     comands_to_send = comands[p]
#                     if comands_to_send == "":
#                         comands_to_send = "empty"
#
#                     conn.send(str.encode(comands_to_send))
#                     comands[p] = ""
#
#             else:
#                 break
#         except socket.error as e:
#             pass
#
#     print("Lost connection")
#
#     try:
#         del games[gameID]
#
#         print("closing game", gameID)
#         print(games)
#     except:
#         pass
#
#     idCount -=1
#
#
#
# current_player = 0
# while True:
#
#     # conn - new socket where newly connected client is redirected from main_socket
#     conn, addr = main_socket.accept()
#     conn.setblocking(False)
#     print("Connected to: " + addr[0] + ":" + str(addr[1]))
#     idCount +=1
#     p=0
#     gameID = (idCount-1)//2
#
#     if idCount %2 ==1:
#         games[gameID] = Game(gameID)
#         print("Created Game ID: ", gameID)
#     else :
#         p=1
#     # else:
#     #     p=2
#     start_new_thread(threaded_client, (conn, p, gameID))
