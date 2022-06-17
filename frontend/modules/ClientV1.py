import socket, traceback

class Client:
    def __init__(self):
        self.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.address = ("", "8086")

    def connect(self):
        try:
            self.client.connect(self.address)
        except:
            print(traceback.format_exc())
    
    def connection(self):

data = "abc"

client.sendall(data.encode('utf-8'))
client.close()