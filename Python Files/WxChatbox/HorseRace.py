from header import *

HORSE_RACE = r'赛马'
__zhende = {}
__user = {}
__horse = u'\U0001F40E'
__dash = u'\U0001F4A8'
__die = u'\U0001F480'
__goodbye = r'.*(再见|退出|不玩|88|拜拜).*'

def __noGoodbye():
    return [random.choice(['这个游戏一旦开始就不能退出的哦嘻嘻', '你不可以离开我呜呜呜']), (info.sent[-1], 1)]
def horse_race(msg, match: re.Match):
    return horse_race1(msg.sender.nick_name)
def horse_race1(sender):
    text = [
        '紧张激烈的赛马比赛马上就要开始啦~',
        '\n'.join([str(i) + ' ' * 20 + __horse for i in range(1, 7)]),
        '请选择一位你觉得会赢的选手~'
    ]
    global __zhende, __user
    __zhende[sender] = 1
    __user[sender] = 0
    return Message(text, Mode.horse_race, horse_race_action1)
def horse_race_action1(msg):
    if re.match(__goodbye, msg.text):
        return Message(__noGoodbye(), Mode.horse_race, horse_race_action1)
    elif EXIT_CODE in msg.text:
        return Message('被你知道这个可爱的小咒语了哈哈，游戏退出~', Mode.standard)
    number = re.search(r'([1-6])', msg.text)
    if number:
        global __user
        __user[msg.sender.name] = int(number[0])
        text = [
            '比赛正式开始啦~',
            '\n'.join([str(i) + (' ' * 12 + __horse + __dash if i != __user[msg.sender.name] else ' ' * 18 + __horse) + ' ' * 4 for i in range(1, 7)]),
            '大家的马儿齐头并进', '只有你的马儿落在了后面', '你要使用外挂吗？']
        return Message(text, Mode.horse_race, horse_race_action2)
    else:
        text = '请输入一个1到6的数字~'
        return Message(text, Mode.horse_race, horse_race_action1)
def horse_race_action2(msg):
    if re.match(__goodbye, msg.text):
        return Message(__noGoodbye(), Mode.horse_race, horse_race_action2)
    elif msg.text == __niubi:
        return Message('被你知道这个可爱的小咒语了哈哈，游戏退出~', Mode.standard)
    no = re.search(r'(否|n|no|不)', msg.text)
    yes = no or re.search(r'(是|y|yes|要|好|可|行|用)', msg.text)
    global __zhende
    if not yes:
        return Message('回答“是”或者“否”啦！', Mode.horse_race, horse_race_action2)
    elif no:
        text = '真的' * __zhende[msg.sender.name] + '不要吗，外挂是免费哒'
        __zhende[msg.sender.name] += 1
        return Message(text, Mode.horse_race, horse_race_action2)
    else:
        text = [
            '你的马获得了外挂！', '你的马冲到了最前面！',
            '\n'.join([str(i) + (' ' * 8 + __horse + __dash if i != __user[msg.sender.name] else ' ' * 4 + __horse + __dash * 3) for i in range(1, 7)]),
            ('等一下', 2), '！', '系统检测到你的马作弊了！', '系统对你的马做出了处罚！',
            '\n'.join([str(i) + (' ' * 8 + __horse + __dash if i != __user[msg.sender.name] else ' ' * 4 + __die) + ' ' * 8 for i in range(1, 7)]),
            '你马死了！',
        ]
        __zhende[msg.sender.name] = 1
        return Message(text, Mode.standard, None)