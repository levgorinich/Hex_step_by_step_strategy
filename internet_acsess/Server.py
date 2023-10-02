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

async def get_client_move(p: int, gameID: int, conn: socket.socket, loop: AbstractEventLoop):

    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while data :=  await loop.sock_recv(conn,4096):

        data = data.decode()
        # print(data)
        if gameID in games:
            game = games[gameID]
            if not data:
                print("Lost connection")
                break
            else:
                # print(comands)
                if data != "no_moves":
                    # print(data)

                    for key in comands:
                        if key != p:
                            comands[key] += data

                comands_to_send = comands[p]
                if comands_to_send == "":
                    comands_to_send = "empty"
                # print(comands_to_send)
                await loop.sock_sendall(conn, str.encode(comands_to_send))
                comands[p] = ""


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


asyncio.run(main(), debug = True)