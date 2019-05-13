from header import *

HORSE_RACE = r'赛马'
__zhende = 1
__user = 0
__horse = u'\U0001F40E'
__dash = u'\U0001F4A8'
__die = u'\U0001F480'

def horse_race(msg, match: re.Match):
    text = [
        '紧张激烈的赛马比赛马上就要开始啦~',
        '\n'.join([str(i) + ' ' * 20 + __horse for i in range(1, 7)]),
        ('请选择一位你觉得会赢的选手~', 1)
    ]
    return Message(text, Mode.horse_race, horse_race_action1)
def horse_race_action1(msg):
    number = re.search(r'([1-6])', msg.text)
    if number:
        global __user
        __user = int(number[0])
        text = [
            '比赛正式开始啦~',
            ('\n'.join([str(i) + (' ' * 12 + __horse + __dash if i != __user else ' ' * 16 + __horse) + ' ' * 4 for i in range(1, 7)]), 1),
            '大家的马儿齐头并进', '只有你的马儿落在了后面', ('是否要充值外挂？', 1)]
        return Message(text, Mode.horse_race, horse_race_action2)
    else:
        text = '请输入一个1到6的数字~'
        return Message(text, Mode.horse_race, horse_race_action1)
def horse_race_action2(msg):
    no = re.search(r'(否|n|no|不)', msg.text)
    yes = no or re.search(r'(是|y|yes|要|好|可|行)', msg.text)
    global __zhende
    if not yes:
        return Message('请回答“是”或者“否”', Mode.horse_race, horse_race_action2)
    elif no:
        text = '真的' * __zhende + '不要吗，外挂是免费哒'
        __zhende += 1
        return Message(text, Mode.horse_race, horse_race_action2)
    else:
        text = [
            '你的马获得了外挂！', '你的马冲到了最前面！',
            '\n'.join([str(i) + (' ' * 8 + __horse + __dash if i != __user else ' ' * 4 + __horse + __dash * 3) for i in range(1, 7)]),
            ('等一下', 2), ('！', 1), ('系统检测到你的马作弊了！', 1), ('系统对你的马做出了处罚！', 1),
            '\n'.join([str(i) + (' ' * 8 + __horse + __dash if i != __user else ' ' * 4 + __die) + ' ' * 8 for i in range(1, 7)]),
            ('你马死了！', 1)
        ]
        __zhende = 1
        return Message(text, Mode.standard, None)