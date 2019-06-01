# TCP server
from helper import *

class server:
    def __init__(self, name, config: dict):
        self.name = name
        self.config = config
        self.host = gethostbyname(gethostname())
        self.port = config[name][PORT]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.pid = pid[name]
        log = self.readLog()
        self.setup(log)
        print(f'Server {self.name} started!')
        self.clientConn, address = self.socket.accept()
        print(f'Connected to Client')
        threading.Thread(target = self.client).start()
        self.serverSockets = {}
        for name in names:
            if name == self.name: continue
            soc = socket(AF_INET, SOCK_STREAM)
            soc.connect((config[name][IP], config[name][PORT]))
            self.serverSockets[name] = soc
            threading.Thread(target = self.server, args = (name, soc)).start()
        if log:
            message = Message(RECONNECT, log = len(self.blockChain))
            for name in names:
                if name != self.name:
                    self.sendMessage(name, message)
            print('RECONNECT message has been sent to the other servers.')
            self.receiveLog = False
        # for reconnection
        while True:
            conn, address = self.socket.accept()
            name = self.findServerName(address[0])
            print(f'{name} is reconnected.')
            self.serverSockets[name] = conn
            threading.Thread(target = self.server, args = (name, conn)).start()

    def setup(self, log):
        if log:
            self.trans = log['trans']
            self.money = log['money']
            self.leaders = log['leaders']
            self.ballotNum = log['ballotNum']
            self.acceptNum = log['acceptNum']
            self.acceptVal = log['acceptVal']
            self.ballot_pool = log['ballot_pool']
            self.block = log['block']
            self.blockChain = log['blockChain']
        else:
            self.trans = []
            self.money = { name: 100 for name in names }
            self.leaders = { name: False for name in names }
            self.ballotNum = Ballot(0, self.pid, 0)
            self.acceptNum = Ballot(0, self.pid, 0)
            self.acceptVal = None
            self.ballot_pool = []
            self.block = None
            self.blockChain = []

    def getBallot(self, block: Block = None) -> Ballot:
        if block:
            self.ballotNum.increment(block.depth)
        return self.ballotNum

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
            self.clientConn.sendall(message.encode())

    def server(self, name, socket: socket):
        while True:
            recv = socket.recv(1024)
            message: Message = eval(recv.decode())
            ballot = message.ballot
            if message.mtype == PREPARE:
                print('PREPARE message received.')
                if ballot >= self.ballotNum:
                    self.ballotNum = ballot.bal
                    reply = Message(ACK, (ballot, self.acceptNum), self.acceptVal)
                    socket.sendall(reply)
                    print('ACK has been sent.')
                else:
                    print('Reject PREPARE message.')
            elif message.mtype == ACK:
                ballotNum, b = ballot
                self.ballot_pool.append(message)
                majority = len(self.leaders) // 2 + 1
                if len(self.ballot_pool) >= majority:
                    myVal = self.block if all(not msg.acceptVal for msg in self.ballot_pool) else self.highestB()
                    reply = Message(ACCEPT, ballotNum, myVal)
                    self.leaders[self.name] = True
                    for name in self.serverSockets:
                        self.sendMessage(name, reply)
                    print('ACCEPT message has been sent to the other servers.')
                    self.acceptVal = myVal
                    self.acceptNum = ballotNum
                    self.ballot_pool.clear()
            elif message.mtype == ACCEPT:
                if self.leaders[self.name]:
                    self.ballot_pool.append(message)
                    majority = len(self.leaders) // 2 + 1
                    if len(self.ballot_pool) >= majority:
                        reply = Message(DECISION, ballot, self.block)
                        self.blockChain.append(self.block)
                        for name in self.serverSockets:
                            self.sendMessage(name, reply)
                        print('DECISION message has been sent to the other servers.')
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
                        socket.sendall(reply)
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
                socket.sendall(reply)
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
        ballot = self.getBallot(block)
        message = Message(PREPARE, ballot)
        for name in self.serverSockets:
            self.sendMessage(name, message)
        print('PREPARE message has been sent.')

    def sendMessage(self, socket: str, message: Message) -> bool:
        try:
            self.serverSockets[name].sendall(str(message).encode())
            return True
        except Exception as e:
            return False

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
        # fwrite(f'Log{self.name}.txt', json.dumps(self.getLog()))
        fwrite(f'Log{self.name}.txt', str(self.getLog()))

    def findServerName(self, ip):
        for name, info in self.config.items():
            if info[IP] == ip:
                return name
        return ''

if __name__ == '__main__':
    name = E
    config = readConfig()
    server = server(name, config)