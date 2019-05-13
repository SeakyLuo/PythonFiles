import re
import random

RAND = r'random[ ]*([1-9][0-9]*)[ ]*to([ ]*[1-9][0-9]*)'
def rand(msg, match: re.Match, recv: list, sent: list) -> str:
    return str(random.randint(int(match[1]), int(match[2])))
REPEAT = 'r'
def repeat(msg, match: re.Match, recv: list, sent: list) -> str:
    return sent[-1] if sent else '傻逼'

regex = {
    RAND: rand,
    REPEAT: repeat
}