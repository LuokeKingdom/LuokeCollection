import socket

server = '192.168.4.56'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
