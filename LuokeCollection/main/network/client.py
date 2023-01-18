import pickle
import socket
from LuokeCollection.main.network.package import Pack, Pets
from assets.IP import address


class Client:
    def __init__(self, pets):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ngrok forwarding
        self.opponent_pets = None
        self.id, self.seed = self.connect()

        if self.id is not None:
            self.send(Pets(pets))

    def connect(self):
        try:
            self.client.connect(address)
            str_id, str_seed = self.client.recv(1024).decode().split(",")
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
