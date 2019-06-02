# TCP client
from helper import *

class client:
    def __init__(self, name, serverIP, serverPort):
        self.name = name
        print(f'This is Client{self.name}')
        self.serverParams = (serverIP, serverPort)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(self.serverParams)
        self.socket.send(name.encode())
        while True:
            command = input("Type your command: \n1. fromClient toClient amount\n2. printBlockchain (pbc)\n3. printBalance (pb)\n4. printSet (ps)\n>>> ")
            if command in [PBC, PB, PS]:
                message = command
                print(f'Command has been sent to the server {self.name}.')
            else:
                fromServer, toServer, amount = command.split()
                message = str(Transaction(fromServer.upper(), toServer.upper(), float(amount)))
                print(f'Transaction request has been sent to the server {self.name}.')
            self.socket.send(message.encode())
            reply = self.socket.recv(1024).decode()
            print(reply)

if __name__ == '__main__':
    name = E
    config = readConfig()[name]
    serverIP = config[IP]
    serverPort = config[PORT]
    client = client(name, serverIP, serverPort)