from enum import Enum
import re
import ez

class Mode(Enum):
    standard = 0 # default
    reply = 1 # needs reply
    sleep = 2
    memo = 10
    chess = 11
    horse_race = 12

class Message:
    defaultMessage = '我有点笨，能不能迁就下我，我们说点别的？'
    def __init__(self, text = '', mode: Mode = Mode.standard, action = None, latency = 0):
        '''Action is the followup reply to user message, which should be a function that at least accepts a wechat msg as an argument.'''
        text = text or Message.defaultMessage
        self.text = []
        if isinstance(text, str):
            self.appendText(text)
        else:
            self.appendTextList(text)
        self.mode = mode
        self.action = action
    def appendText(self, text):
        if isinstance(text, str):
            self.text.append((text, 0))
        else:
            self.text.append(text)
    def appendTextList(self, lst: list):
        for text in lst:
            self.appendText(text)
    def __str__(self):
        return f'Message(text={self.text}, mode={self.mode}, action={self.action})'
    def __repr__(self):
        return str(self)
    def isDefault(self):
        return any(Message.defaultMessage in text for text in self.text)

class Info:
    def __init__(self):
        self.recv = []
        self.sent = []
        self.error = []
        self.mode = Mode.standard
        self.action = None
        self.replies = []

    def appendReply(self, message: Message):
        self.replies.append(message)
        self.mode = message.mode
        self.action = message.action
        for text in message.text:
            self.sent.append(text[0])

infoDict = {}
memo = ez.Settings(__file__, 'memo')