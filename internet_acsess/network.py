import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.setblocking(False)
        self.server = "5.42.78.110"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            first_result = self.client.recv(2048).decode()
            print(first_result, "first result")
            return first_result

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
