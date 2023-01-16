import socket
from _thread import *
import pickle
from .package import Pack, Pets

server = '192.168.4.56'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.listen(2)
print("Server started")



def handle_connection(conn):
    pass

while 1:
    conn, addr = s.accept()
    start_new_thread(handle_connection, (conn,))
    print(f"Client <{addr}> connected")



