from header import *
from HorseRace import *
from Balloon import *

THANK = r'.*(谢).*'
def thank(msg, match: re.Match):
    return Message('不客气~')
RAND = r'random[ ]*([1-9][0-9]*)[ ]*to([ ]*[1-9][0-9]*)'
def rand(msg, match: re.Match):
    return Message(str(random.randint(int(match[1]), int(match[2]))))
REPEAT = r'r'
def repeat(msg, match: re.Match):
    info = infoDict.get(msg.sender.name, Info())
    return Message(info.sent[-1] if info.sent else '傻逼')
TGTDZHYWSY = '舔狗舔到最后一无所有'
def tgtdzhywsy(msg, match: re.Match):
    return Message(u'\U0001f445\U0001f436\U0001f445\U0001f52a\U0001f444\U0001f435\U0001f595\U0001f21a\U0001f512\U0001f236')
TGTDZHYYJY = '舔狗舔到最后应有尽有'
def tgtdzhyyjy(msg, match: re.Match):
    return Message(u'\U0001f445\U0001f436\U0001f445\U0001f52a\U0001f444\U0001f435\U0001f338\U0001f236\U0001f232\U0001f236')
CHESS = r'(象棋)'
def chess(msg, match: re.Match):
    text = '''車馬象士将士象馬車

    砲                    砲
卒    卒    卒    卒    卒


兵    兵    兵    兵    兵
    炮                    炮

车马相仕帅仕相马车'''
    return Message(text, Mode.chess)
REMEMBER = r'记住(.*)[ -:：](.*)'
def remember(msg, match: re.Match):
    name = match[1]
    target = match[2]
    memo.setdefault(name, [])
    memo[name].append(target)
    return Message([f'(๑‾ ꇴ ‾๑)好哒，这是你现在的{name}~', str(memo[name])], Mode.memo)
FORGET = r'忘记(.*)[ -:：]?(.*)?'
def forget(msg, match: re.Match):
    name = match[1]
    target = match[2]
    message = ''
    if target:
        if target in memo[name]:
            memo[name].remove(target)
            message = [f'(๑‾ ꇴ ‾๑)好哒，这是你现在的{name}~', str(memo[name])]
        else:
            message = '要忘记的东西不存在哦'
    else:
        message = '列表忘记啦' if memo.pop(name) else '列表不存在哦'
    return Message(message, Mode.memo)
LOOKAT = r'瞅瞅(.*)'
def lookat(msg, match: re.Match):
    name = match[1]
    if name in ['全部', '所有']:
        message = ['这是你所有的备忘列表~'] + [f'{name}: {lst}' for name, lst in memo.settings.items()]
    else:
        lst = memo.get(name, [])
        message = [f'(๑‾ ꇴ ‾๑)好哒，这是你现在的{name}~', str(memo[name])] if lst else '列表不存在哦'
    return Message(message, Mode.memo)
DIRTY = r'.*(操|傻逼|傻屌|脑残|靠|滚|有病).*'
def dirty(msg, match: re.Match):
    return Message(random.choice(['不可以说脏话嘤嘤嘤', '你骂我呜呜呜', '你不可以欺负我']))
VOMIT = r'.*(呕|D区|口区).*'
def vomit(msg, match: re.Match):
    return Message(random.choice(['我很可爱的嘤嘤嘤', '你欺负我呜呜呜']))

regex = {
    THANK: thank,
    RAND: rand,
    REPEAT: repeat,
    TGTDZHYWSY: tgtdzhywsy,
    TGTDZHYYJY: tgtdzhyyjy,
    CHESS: chess,
    REMEMBER: remember,
    FORGET: forget,
    LOOKAT: lookat,
    DIRTY: dirty,
    VOMIT: vomit,
    HORSE_RACE: horse_race,
    BALLOON: balloon
}
