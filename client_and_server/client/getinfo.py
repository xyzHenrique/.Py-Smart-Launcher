import uuid

class Getinfo:
    def __init__(self):
        pass

    def get__mac_address(self):
        mac = 
        print(":".join(("%012X" % uuid.getnode())[i:i+2] for i in range(0, 12, 2)))

x = Getinfo()
x.get__mac_address()
