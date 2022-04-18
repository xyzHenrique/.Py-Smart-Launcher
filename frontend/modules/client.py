import struct, json, socket, threading, time

class ApplicationClient:
    def __init__(self):
        """SOCKET"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("localhost", 8182)
        
        """FUNCTIONS"""
        self.connect()

    def connect(self):
        self.socket.connect(self.address)

        thread = threading.Thread(target=self.on_connected, args=(), daemon=True)
        thread.start()

    def on_connected(self):
        #x = 1
        while True:
            #x += 1
            
            #msg = f"{x}".encode()
            #msg = struct.pack(">I", len(msg)) + msg

            self.socket.sendall("aaa".encode())
             
            data = self.socket.recv(1024)

            print(data)

client = ApplicationClient()
        
        


