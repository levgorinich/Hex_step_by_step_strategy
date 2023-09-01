import socket
from _thread import *
import sys
from net_player import Player
import pickle

server = ""

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player(0, 0, 10, 10, (255, 0, 0)), Player(0, 0, 10, 10, (0, 255, 0))]


def threaded_client(conn, player):
    conn.send(pickle.dumps((players[player])))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconected")
                break
            else:
                if player == 0:
                    reply = players[1]
                else:
                    reply = players[0]
                #
                # print("Received: ", data)
                # print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Connected to: " + addr[0] + ":" + str(addr[1]))
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
