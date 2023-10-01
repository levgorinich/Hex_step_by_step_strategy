import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.setblocking(False)
        self.server = "5.42.78.110"
        self.port = 5555
        self.addr = (self.server, self.port)
        # print("timeout==",self.client.gettimeout())
        self.client.settimeout(3)
        self.p = self.connect()


    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("trying to connect")
            return self.client.recv(2048).decode()
        except Exception as e:
            print("!!!!!Connect error::",e)
            pass

    def send(self, data):
        try:
            # print("tried to send from network")
            self.client.send(str.encode(data))
            # print("i recieved")
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
    def get_changes(self):
        try:
            return self.client.recv(2048).decode()
        except:
            pass
