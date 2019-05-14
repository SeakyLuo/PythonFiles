from header import *

__balloon = u'\U0001F388'
__width = 10
__height = 10

BALLOON = r'打气球'
def balloon(msg, match: re.Match):
    return Message(['打气球咯', '\n'.join([__balloon * __width] * __height)])