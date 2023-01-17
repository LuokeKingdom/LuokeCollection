import socket
from _thread import *
import pickle

from LuokeCollection.main.network.package import Pack, Pets

server = '192.168.4.56'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(2)
print("Server started")
pets = [None, None]
status = [Pack(), Pack()]

count = 0


def threaded_client(conn: socket.socket, index):
    def receive(bits):
        data = conn.recv(bits) 
        if not data:
            return False
        return pickle.loads(data)
    conn.send(str.encode("Connected"))
    while 1:
        try:
            reply = Pack()
            data = receive(2048)
            if not data:
                break
            if data.id == 1:
                pets[index] = data.data
                status[index].accept = True
            else:
                if pets[1-index] is not None:
                    reply.opponent = 1-index
                    if data.ready is False and data.accept is True:
                        reply = Pets(pets[1-index]) 
                    elif data.ready and data.accept:
                        status[index].ready = True
                        reply.ready = not not status[1-index].ready
                else:
                    pass
            print(data)
            reply.accept = status[index].accept
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break
    conn.close()
    pets[index] = None
    global count
    count -= 1
    print("connection lost")

while 1:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn, count))
    count += 1
    print(f"Client <{addr}> connected")


