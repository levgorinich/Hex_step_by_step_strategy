import socket
from _thread import *
from game import Game
import sys

import pickle

server = ""

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

connected =  set()
games = {}
idCount =0




def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))


    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameID in games:
                game = games[gameID]
                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendal(pickle.dumps(reply))
            else:
                break
        except:
            break


    print("Lost connection")

    try:
        del games[gameID]

        print("closing game", gameID)
        print(games)
    except:
        pass

    idCount -=1



current_player = 0
while True:
    conn, addr = s.accept()
    print("Connected to: " + addr[0] + ":" + str(addr[1]))
    idCount +=1
    p=0
    gameID = (idCount-1)//2

    if idCount %2 ==1:
        games[gameID] = Game(gameID)
        print("Created Game ID: ", gameID)
    else:
        games[gameID].ready = True
        p=1
    start_new_thread(threaded_client, (conn, p, gameID))
