import socket

ADDRESS = "localhost", 1234

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(ADDRESS)

    def close(self):
        self.socket.close()
