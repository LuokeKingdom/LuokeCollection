import pickle
import socket
from .package import Pack, Pets
from LuokeCollection.settings.dev import IP, PORT

class Client:
    def __init__(self, pets):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = IP
        self.port = PORT
        self.opponent_pets = None
        self.id = self.connect()

        if self.id is not None:
            self.send(Pets(pets))
                

    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            return(int(self.client.recv(2048).decode()))
        except:
            print("Fail")
            return None

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
