from dataclasses import dataclass
import time, threading, json
from socket import *
from hashlib import sha256

names = 'ABCDE'
A, B, C, D, E = names
IP = 'IP'
PORT = 'Port'
pid = { name: i + 1 for i, name in enumerate(names) }

PREPARE, ACK, ACCEPT, DECISION, RECONNECT, LOG = range(6)

PB = 'pb'
PBC = 'pbc'
PS = 'ps'

@dataclass
class Transaction:
    fromServer: str
    toServer: str
    amount: float
    def toString(self):
        return f'{self.fromServer} {self.toServer} {self.amount}'

@dataclass
class Block:
    txA: Transaction
    txB: Transaction
    depth: int = 1
    nonce: str = 'NULL'
    prev:  str = 'NULL'
    def hashString(self):
        return str(self.depth) + self.prev + self.nonce + self.txA.toString() + self.txB.toString()

    def hash(self):
        return sha256(self.hashString().encode()).hexdigest()

    def toString(self):
        return f'Depth: {self.depth}\nH(B-1): {self.prev}\nNonce: {self.nonce}\ntxA: {self.txA.toString()}\ntxB: {self.txB.toString()}\n'

@dataclass
class Ballot:
    bal: int
    pid: int
    depth: int

    def increment(self, depth):
        self.bal += 1
        self.depth = depth

    def __ge__(self, obj):
        return self.depth > obj.depth or (self.depth == obj.depth and self.bal >= obj.bal)

@dataclass
class Message:
    mtype: int
    sender: str
    ballot: Ballot = None # a Ballot object or a tuple of two Ballots
    acceptVal: Block = None
    log: str = ''

def readConfig() -> dict:
    return json.loads(fread('config.txt'))

def updateConfig():
    config = readConfig()
    for name, info in config.items():
        info[IP] = gethostbyname(gethostname())
        config[name] = info
    fwrite('config.txt', json.dumps(config))

def saveClients():
    content = fread('client.py')
    for name in names:
        fwrite(f'Client{name}.py', content.replace('saveClients()', name))
    return ''

def saveServers():
    content = fread('server.py')
    for name in names:
        fwrite(f'Server{name}.py', content.replace('saveServers()', name))
    return ''

def clearLogs():
    for name in names:
        fwrite(f'Log{name}.txt', '')

def fread(filename):
    with open(filename) as file:
        content = file.read()
        return content

def fwrite(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    saveClients()
    saveServers()
    updateConfig()
    clearLogs()
