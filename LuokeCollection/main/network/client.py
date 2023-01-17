import pickle
import socket
from LuokeCollection.main.network.package import Pack, Pets


class Client:
    def __init__(self, pets):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ngrok forwarding
        self.server = "0.tcp.ngrok.io"
        self.port = 19173
        self.opponent_pets = None
        self.id, self.seed = self.connect()

        if self.id is not None:
            self.send(Pets(pets))

    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            str_id, str_seed = self.client.recv(2048).decode().split(",")
            return int(str_id), int(str_seed)
        except Exception as e:
            print("Connect Fail")
            print(e)
            return None

    def receive(self, bits):
        return pickle.loads(self.client.recv(bits))

    def send(self, obj):
        try:
            self.client.sendall(pickle.dumps(obj))
            return True
        except Exception as e:
            print("Send Fail")
            print(e)
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
        except Exception as e:
            print("Reply Fail")
            print(e)
            return False
