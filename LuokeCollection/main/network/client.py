import pickle
import socket
from .package import Pack, Pets

class Client:
    def __init__(self, pets):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.4.56'
        self.port = 5555
        self.opponent_pets = None

        if self.connect():
            self.send(Pets(pets))
                

    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            print(self.client.recv(2048).decode())
            return True
        except:
            print("Fail")
            return False

    def receive(self, bits):
        return pickle.loads(self.client.recv(bits))

    def send(self, obj):
        try:
            self.client.sendall(pickle.dumps(obj))
            return True
        except:
            return False

    def reply(self, ready, accept, choice, oppo):
        p = Pack()
        p.ready = ready
        p.accept = accept
        p.choice = choice
        p.opponent = oppo
        try:
            self.client.sendall(pickle.dumps(p))
            return True
        except:
            return False
