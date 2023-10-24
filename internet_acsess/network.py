import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.setblocking(False)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.server_id = self.connect()

        self.p =None
        self.seed = None
        self.players_amount = None

    def get_server_id(self):
        return self.server_id

    def getP(self):
        return self.p
    def getSeed(self):
        return self.seed

    def getPlayersAmount(self):
        return self.players_amount

    def connect(self):
        try:
            print("i tried ot connect")
            self.client.connect(self.addr)
            print("i connected")
            first_result = self.client.recv(2048).decode()

            server_id= int(first_result)
            return server_id

        except:
            pass

    def connect_to_game(self):
        data = self.send("join game")
        self.p, self.seed, self.players_amount = map(int, data.split(" "))

    def send(self, data):
        print("this is data to send", data)
        try:
            # print("tried to send from network")

            self.client.send(str.encode(data))

            # print("i recieved")
            resp =self.client.recv(2048).decode()

            return resp
        except socket.error as e:
            print("I stoped here ")
            print(e)
    def close(self):
        self.client.close()
    def get_changes(self):
        try:
            return self.client.recv(2048).decode()
        except:
            pass
