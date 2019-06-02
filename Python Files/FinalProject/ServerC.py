# TCP server
from helper import *

class server:
    def __init__(self, name, config: dict):
        self.name = name
        self.config = config
        self.host = config[self.name][IP]
        self.port = config[self.name][PORT]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.pid = pid[self.name]
        log = self.readLog()
        self.setup(log)
        print(f'Server {self.name} started!')
        self.ballot_pool = []
        self.sendSocket = {}
        self.replySocket = {}
        if log:
            message = Message(RECONNECT, log = len(self.blockChain))
            self.broadcast(message)
            print('RECONNECT message has been sent to other servers.')
            self.receiveLog = False
        # listen for connection request from client and other 4 servers
        while True:
            conn, address = self.socket.accept()
            message = conn.recv(1024).decode()
            if message == self.name:
                self.clientConn = conn
                threading.Thread(target = self.client).start()
                print(f'Connected to Client')
            else:
                threading.Thread(target = self.server, args = [conn, message]).start()

    def setup(self, log):
        if log:
            self.trans = log['trans']
            self.money = log['money']
            self.leaders = log['leaders']
            self.ballotNum = log['ballotNum']
            self.acceptNum = log['acceptNum']
            self.acceptVal = log['acceptVal']
            self.block = log['block']
            self.blockChain = log['blockChain']
        else:
            self.trans = []
            self.money = { name: 100 for name in names }
            self.leaders = { name: False for name in names }
            self.ballotNum = Ballot(0, self.pid, 0)
            self.acceptNum = Ballot(0, self.pid, 0)
            self.acceptVal = None
            self.block = None
            self.blockChain = []

    def client(self):
        while True:
            recv = self.clientConn.recv(1024)
            command = recv.decode()
            if command == PB:
                print('Print Balance Command Received')
                message = '\n'.join([f'{name}: {balance}' for name, balance in money.items()])
            elif command == PBC:
                print('Print Block Chain Command Received')
                message = '↑\n'.join([block.toString() for block in self.blockChain])
            elif command == PS:
                print('Print Set Received')
                if self.trans:
                    message = '\n'.join([transaction.toString() for transaction in self.trans])
                else:
                    message = 'No Transactions.'
            else:
                print(f'Transaction received from {self.name}')
                transaction: Transaction = eval(command)
                if self.money[transaction.fromServer] < transaction.amount:
                    message = 'Transaction failed.'
                    print(message)
                else:
                    message = 'Transaction successful!'
                    print(message)
                    self.trans.append(transaction)
                    if len(self.trans) > 1:
                        print('A block created.')
                        self.prepare()
                    self.writeLog()
            self.clientConn.send(message.encode())

    def server(self, conn: socket, msg: str):
        while True:
            if msg:
                message = eval(msg)
            else:
                recv = conn.recv(1024).decode()
                message = eval(recv)
            msg = None
            sender = message.sender
            ballot = message.ballot
            if message.mtype == PREPARE:
                print('PREPARE message received.')
                if ballot >= self.ballotNum:
                    self.ballotNum = ballot
                    reply = Message(ACK, self.name, (ballot, self.acceptNum), self.acceptVal)
                    self.sendMessage(sender, reply)
                    print('ACK has been sent.')
                else:
                    print('Reject PREPARE message.')
            elif message.mtype == ACK:
                print('ACK message is received.')
                ballotNum, b = ballot
                self.ballot_pool.append(message)
                majority = len(self.leaders) // 2 + 1
                if len(self.ballot_pool) == majority:
                    myVal = self.block if all(not msg.acceptVal for msg in self.ballot_pool) else self.highestB()
                    self.ballot_pool.clear()
                    self.acceptVal = myVal
                    self.acceptNum = ballotNum
                    self.leaders[self.name] = True
                    reply = Message(ACCEPT, self.name, ballotNum, myVal)
                    self.broadcast(reply)
                    print('ACCEPT message has been sent to other servers.')
            elif message.mtype == ACCEPT:
                if self.leaders[self.name]:
                    print('ACCEPT message is received from the Acceptor.')
                    self.ballot_pool.append(message)
                    majority = len(self.leaders) // 2 + 1
                    if len(self.ballot_pool) == majority:
                        self.ballot_pool.clear()
                        reply = Message(DECISION, self.name, ballot, self.block)
                        self.broadcast(reply)
                        print('DECISION message has been sent to other servers.')
                        self.appendBlock(self.block)
                        self.block = None
                        self.leaders[self.name] = False
                        self.trans = self.trans[2:]
                else:
                    print('ACCEPT message is received from the Leader.')
                    if ballot >= self.ballotNum:
                        self.leaders[sender] = True
                        self.acceptNum = ballot
                        self.acceptVal = message.acceptVal
                        reply = message
                        self.sendMessage(sender, reply)
                    else:
                        print('ACCEPT message is rejected.')
            elif message.mtype == DECISION:
                self.leaders[sender] = False
                block = self.acceptVal
                self.appendBlock(block)
                # concurrent leader
                if self.block:
                    self.prepare()
            elif message.mtype == RECONNECT:
                reply = Message(LOG, self.name, log = self.getLog(message.log))
                self.sendMessage(sender, reply)
                print(f'Log has been sent to Server{sender}.')
            elif message.mtype == LOG:
                # update log only once?
                if not self.receiveLog:
                    print(f'Log is received from Server{sender}.')
                    for block in message.log:
                        # verify block?
                        self.appendBlock(block)
                    self.receiveLog = True
            self.writeLog()

    def prepare(self):
        txA, txB = self.trans[:2]
        if self.blockChain:
            prev = self.blockChain[-1]
            self.block = Block(txA, txB, prev.depth + 1, prev.hashString(), hash(prev))
        else:
            self.block = Block(txA, txB)
        ballot = self.getBallot(self.block)
        message = Message(PREPARE, self.name, ballot, self.block)
        self.broadcast(message)
        print('PREPARE message has been sent.')

    def sendMessage(self, toServer, message):
        if toServer not in self.replySocket:
            soc = socket(AF_INET, SOCK_STREAM)
            try:
                soc.connect((config[toServer][IP], config[toServer][PORT]))
            except:
                pass
            self.replySocket[toServer] = soc
        self.replySocket[toServer].sendall(str(message).encode())

    def broadcast(self, message: Message) -> bool:
        msg = str(message).encode()
        for name, info in self.config.items():
            if name == self.name: continue
            try:
                if name in self.sendSocket:
                    soc = self.sendSocket[name]
                else:
                    soc = socket(AF_INET, SOCK_STREAM)
                    soc.connect((info[IP], info[PORT]))
                    self.sendSocket[name] = soc
                soc.sendall(msg)
            except:
                pass

    def getBallot(self, block: Block = None) -> Ballot:
        if block:
            self.ballotNum.increment(block.depth)
        return self.ballotNum

    def highestB(self) -> Block:
        msg = self.ballot_pool[0]
        block = msg.acceptVal
        b = msg.ballot
        for message in self.ballot_pool[1:]:
            if message.b >= b:
                block = message.block
        return block

    def appendBlock(self, block):
        if not self.blockChain or block.prev == hash(self.blockChain[-1]):
            for transaction in [block.txA, block.txB]:
                if self.money[transaction.fromServer] < transaction.amount:
                    print('Block Rejected.')
                    break
                self.money[transaction.fromServer] -= transaction.amount
                self.money[transaction.toServer] += transaction.amount
            else:
                self.appendBlock(block)
                print('Block appended.')
                while self.trans:
                    transaction = self.trans[0]
                    if self.money[transaction.fromServer] < transaction.amount:
                        self.trans.pop(0)
                    else:
                        break
        else:
            print('Invalid block.')

    def tryAppendBlock(self, block):
        return

    def readLog(self):
        try:
            return eval(fread(f'Log{self.name}.txt'))
        except:
            return ''

    def getLog(self, depth = 0) -> dict:
        return {
            'trans': self.trans,
            'money': self.money,
            'leaders': self.leaders,
            'ballotNum': self.ballotNum,
            'acceptNum': self.acceptNum,
            'acceptVal': self.acceptVal,
            'block': self.block,
            'blockChain': self.blockChain[depth:],
        }

    def writeLog(self):
        fwrite(f'Log{self.name}.txt', str(self.getLog()))

if __name__ == '__main__':
    name = C
    config = readConfig()
    server = server(name, config)