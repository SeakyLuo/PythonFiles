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
        self.serverSockets = {}
        self.ballot_pool = []
        # if log:
        #     message = Message(RECONNECT, log = len(self.blockChain))
        #     self.broadcast(message)
        #     print('RECONNECT message has been sent to other servers.')
        #     self.receiveLog = False
        #listen for connection request from client and other 4 servers
        while True:
            conn, address = self.socket.accept()
            message = conn.recv(1024).decode()
            if message == self.name:
                self.clientConn = conn
                threading.Thread(target = self.client).start()
                print(f'Connected to Client')
            else:
                print(message)
                threading.Thread(target = self.server, args = (address, conn, message)).start()

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

    def server(self, name, socket: socket, firstMessage):
        while True:
            if firstMessage:
                message: Message = eval(firstMessage)
                firstMessage = None
            else:
                recv = socket.recv(1024).decode()
                print(recv)
                if not recv:
                    continue
                message: Message = eval(recv)
            ballot = message.ballot
            if message.mtype == PREPARE:
                print('PREPARE message received.')
                if ballot >= self.ballotNum:
                    self.ballotNum = ballot.bal
                    reply = Message(ACK, (ballot, self.acceptNum), self.acceptVal)
                    self.sendMessage(socket, reply)
                    print('ACK has been sent.')
                else:
                    print('Reject PREPARE message.')
            elif message.mtype == ACK:
                print('ACK message is received.')
                ballotNum, b = ballot
                self.ballot_pool.append(message)
                majority = len(self.leaders) // 2 + 1
                if len(self.ballot_pool) >= majority:
                    myVal = self.block if all(not msg.acceptVal for msg in self.ballot_pool) else self.highestB()
                    reply = Message(ACCEPT, ballotNum, myVal)
                    self.leaders[self.name] = True
                    self.broadcast(reply)
                    print('ACCEPT message has been sent to other servers.')
                    self.acceptVal = myVal
                    self.acceptNum = ballotNum
                    self.ballot_pool.clear()
            elif message.mtype == ACCEPT:
                if self.leaders[self.name]:
                    print('ACCEPT message is received from the Acceptor.')
                    self.ballot_pool.append(message)
                    majority = len(self.leaders) // 2 + 1
                    if len(self.ballot_pool) >= majority:
                        reply = Message(DECISION, ballot, self.block)
                        self.blockChain.append(self.block)
                        self.broadcast(reply)
                        print('DECISION message has been sent to other servers.')
                        self.block = None
                        self.leaders[self.name] = False
                        self.ballot_pool.clear()
                        for i in range(2):
                            self.trans.pop(i)
                else:
                    print('ACCEPT message is received from the Leader.')
                    if ballot >= self.ballotNum:
                        self.leaders[name] = True
                        self.acceptNum = ballot
                        self.acceptVal = message.acceptVal
                        reply = message
                        self.sendMessage(socket, reply)
                    else:
                        print('ACCEPT message is rejected.')
            elif message.mtype == DECISION:
                self.leaders[name] = False
                block = self.acceptVal
                if block.prev == hash(self.blockChain[-1]):
                    for transaction in [block.txA, block.txB]:
                        if self.money[transaction.fromServer] < transaction.amount:
                            print('Block Rejected.')
                            break
                        self.money[transaction.fromServer] -= transaction.amount
                        self.money[transaction.toServer] += transaction.amount
                    else:
                        print('Block appended.')
                        self.blockChain.append(block)
                        while True:
                            transaction = self.trans[0]
                            if self.money[transaction.fromServer] < transaction.amount:
                                self.trans.pop(0)
                            else:
                                break
                else:
                    print('Invalid block.')
                # concurrent leader
                if self.block:
                    self.prepare()
            elif message.mtype == RECONNECT:
                reply = Message(LOG, log = self.getLog(message.log))
                self.sendMessage(socket, reply)
                print(f'Log has been sent to Server{name}.')
            elif message.mtype == LOG:
                # update log only once?
                if not self.receiveLog:
                    print(f'Log is received from Server{name}.')
                    for block in message.log:
                        # verify block?
                        self.blockChain.append(block)
                    self.receiveLog = True
            self.writeLog()

    def prepare(self):
        txA, txB = self.trans[:2]
        self.block = Block(self.blockChain[-1] if self.blockChain else None, txA, txB)
        ballot = self.getBallot(self.block)
        message = Message(PREPARE, ballot)
        self.broadcast(message)
        print('PREPARE message has been sent.')

    def sendMessage(self, socket, message):
        socket.sendall(str(message).encode())

    def broadcast(self, message: Message) -> bool:
        msg = str(message).encode()
        for name, info in self.config.items():
            if name == self.name: continue
            try:
                soc = socket(AF_INET, SOCK_STREAM)
                soc = self.serverSockets.setdefault(name, soc)
                soc.connect((info[IP], info[PORT]))
                soc.sendall(msg)
            except:
                pass
            # finally:
            #     soc.close()

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
            'ballot_pool': self.ballot_pool,
            'block': self.block,
            'blockChain': self.blockChain[depth:],
        }

    def writeLog(self):
        fwrite(f'Log{self.name}.txt', str(self.getLog()))

if __name__ == '__main__':
    name = C
    config = readConfig()
    server = server(name, config)