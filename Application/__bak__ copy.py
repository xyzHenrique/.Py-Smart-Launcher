import socket, threading
# this is script is used to create a client socket

# this class is used to create a client socket
class ClientSocket:
    def __init__(self):
        """SOCKET"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("localhost", 8086)

        """FUNCTIONS"""
        self.connect()

    def connect(self):
        self.socket.connect(self.address)

        thread = threading.Thread(target=self.on_connected, args=(), daemon=True)
        thread.start()

    def on_connected(self):
