import socket
from _thread import start_new_thread
import pickle
import random

from LuokeCollection.main.network.package import Pack, Pets
from LuokeCollection.settings.dev import PORT

server = "localhost"
port = PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()
print("Server started")
games = {}
count = 0


class Game:
    def __init__(self, seed):
        self.pets = [None, None]
        self.status = [Pack(), Pack()]
        self.sent = [False, False]
        self.seed = seed
        self.started = False


def threaded_client(conn: socket.socket, count):
    game = None
    index = 0
    countId = count
    for k, v in games.items():
        if not v.started:
            v.started = True
            game = v
            index = 1
            countId = k
    if index == 0:
        game_rng_seed = random.choice(range(1, 10000000))
        game = Game(game_rng_seed)
        games[count] = game

    def receive(bits):
        data = conn.recv(bits)
        if not data:
            return False
        return pickle.loads(data)

    conn.send(str.encode(str(index) + "," + str(game.seed)))

    while 1:
        try:
            if games.get(countId) is None:
                break
            reply = Pack()
            data = receive(1024)
            if all(game.sent):
                game.sent[0] = False
                game.sent[1] = False
                game.status[0].choice = -1
                game.status[1].choice = -1
            if not data:
                break
            if data.id == 1:
                game.pets[index] = data.data
                game.status[index].accept = True
            else:
                if game.pets[1 - index] is not None:
                    reply.opponent = 1 - index
                    if data.ready is False and data.accept is True:
                        reply = Pets(game.pets[1 - index])
                    elif data.ready and data.accept:
                        game.status[index].ready = True
                        reply.ready = game.status[1 - index].ready
                    elif data.ready is True and data.accept is False:
                        game.status[index].choice = data.choice
                    if (
                        game.status[index].choice > -1
                        and game.status[1 - index].choice > -1
                        and not game.sent[index]
                    ):
                        reply.ready = True
                        reply.accept = False
                        reply.choice = game.status[1 - index].choice
                        conn.sendall(pickle.dumps(reply))
                        game.sent[index] = True
                        continue
                else:
                    pass
            reply.accept = game.status[index].accept
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break
    if games.get(countId) is not None:
        del games[countId]
        print(f"ID <{countId}>: connection lost")
    else:
        print(f"ID <{countId}>: opponent disconnected")

    conn.close()


while 1:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn, count))
    count += 1
    print(f"Client <{addr}> connected")
