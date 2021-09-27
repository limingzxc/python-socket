import socket


class Tcp:
    def __init__(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.bind(('127.0.0.1', 9090))
        sk.listen()

    def lianjie(self):
        pass

