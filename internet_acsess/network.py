import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.setblocking(False)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p, self.seed = self.connect()

    def getP(self):
        return self.p
    def getSeed(self):
        return self.seed

    def connect(self):
        try:
            print("i tried ot connect")
            self.client.connect(self.addr)
            print("i connected")
            first_result = self.client.recv(2048).decode()
            print(first_result, " this I got ros")
            player_id, seed = map(int, first_result.split())
            print(player_id,seed, "first result")
            return player_id, seed

        except:
            pass

    def send(self, data):

        try:
            # print("tried to send from network")

            self.client.send(str.encode(data))

            # print("i recieved")
            resp =self.client.recv(2048).decode()

            return resp
        except socket.error as e:
            print("I stoped here ")
            print(e)
    def get_changes(self):
        try:
            return self.client.recv(2048).decode()
        except:
            pass
