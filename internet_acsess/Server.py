import socket
from _thread import *
import  sys

server = ""

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(string):
    stritng = string.split(",")
    return int(stritng[0]), int(stritng[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0),(100,100)]
def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data



            if not data:
                print("Disconected")
                break
            else:
                if player == 0:
                    reply = pos[1]
                else:
                    reply = pos[0]
                #
                # print("Received: ", data)
                # print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Connected to: " + addr[0] + ":" + str(addr[1]))
    start_new_thread(threaded_client, (conn,current_player))
    current_player +=1