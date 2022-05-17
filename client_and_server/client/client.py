import socket, uuid

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect(("localhost", 8181))
    
    def handle_send(self):
        header = {"name"}

    def handle_recv(self):
        pass
