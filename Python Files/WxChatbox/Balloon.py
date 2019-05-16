from header import *
from HorseRace import horse_race1

BALLOON = r'.*(打气球).*'
__bossAim = 0
__gameInfo = {}

class Voucher: #'\n'.join(['=' * 21, '|' + ' ' * 40 + '|',  ])
    content = \
'''====================
      ■■■■■■■■
      ■■■■■■■■
===================
'''
    levels = ['一', '二', '三', '四', '五']
    awards = [
        ['给老板发个红包', '今天晚上会好梦'],
        ['请老板吃一餐饭', '获得额外零张券'],
        ['谢谢惠顾再来玩', '背诵一天圆周率'],
        ['暗恋老板一辈子', '陪老板傻笑一天'],
        ['美国的新鲜空气', '拍老板一年马屁']
    ]
    def __init__(self, level):
        self.levelNum = level
        self.level = Voucher.levels[level] + '等奖'
        self.award = random.choice(Voucher.awards[level])
        self.string = Voucher.content
        self.guaTimes = 0
    def __str__(self):
        return self.string
    def gua(self):
        if self.guaTimes == 0:
            self.string = self.string.replace('■■■■■■■■', ' ' * 10 + self.level, 1)
        elif self.guaTimes == 1:
            self.string = self.string.replace('■■■■■■■■', self.award)
        self.guaTimes += 1
        return self.string

def guaVoucher(vouchers) -> list:
    text = []
    if vouchers:
        last = len(vouchers) - 1
        for i, voucher in enumerate(vouchers):
            if last:
                num = f'第{i + 1}' if i < last else '最后一'
                first = f'你拿起了{num}张奖券' + '~' * (i + 1)
            else:
                first = '你拿起了你唯一的一张奖券~'
            level = 5 - voucher.levelNum
            text += [first, str(voucher), '你刮开了它', f'你获得了{voucher.level}' + '！' * level, voucher.gua()]
            text += ['对应的奖励是' + '~' * level, voucher.gua(), voucher.award + '！' * level]
        text += ['这就是你所有的奖励啦~', '完结撒花~']
    else:
        text.append('再接再厉呀')
    return text

class BalloonGame:
    width = 3
    height = 3
    balloon = u'\U0001F388'
    boom = u'\U0001F4A5'
    pistol = u'\U0001F52B'
    boss = u'\U0001F468'
    balloonCode = 1
    boomCode = 2
    badShot = 3
    madeShot = 4
    aimBoss = (-1, -1)
    def __init__(self):
        self.shots = 3
        self.balloons = [[BalloonGame.balloonCode] * BalloonGame.width for _ in range(BalloonGame.height)]
        self.bossAimed = 0
        self.boomCount = 0
    def getEmoji(self, i, j) -> str:
        if self.balloons[i][j] == BalloonGame.balloonCode:
            return BalloonGame.balloon
        elif self.balloons[i][j] == BalloonGame.boomCode:
            return BalloonGame.boom
        return ' '
    def __str__(self):
        row = '   ' + '    '.join(list(map(str, range(1, BalloonGame.height + 1))))
        rows = '\n'.join([str(h + 1) + ''.join([self.getEmoji(w, h) for w in range(BalloonGame.width)]) for h in range(BalloonGame.height)])
        return row + '\n' + rows
    def __repr__(self):
        return f'GameInfo(Shots: {self.shots}; Balloons: {self.balloons}; BossAimed: {self.bossAimed})'
    def getNeighbors(self, i, j):
        return list(filter(lambda x: 0 <= x[0] < BalloonGame.width and 0 <= x[1] < BalloonGame.height and self.balloons[x[0]][x[1]] == BalloonGame.balloonCode, \
            [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]))
    def shoot(self, i, j) -> list:
        if not 0 <= i < BalloonGame.width or not 0 <= j < BalloonGame.height:
            return BalloonGame.badShot
        if self.balloons[i][j] != BalloonGame.balloonCode:
            return BalloonGame.madeShot
        self.shots -= 1
        if random.randint(0, 3) == 0: # if miss
            return []
        if random.randint(0, 10) == 0:
            return [BalloonGame.aimBoss]
        neighbors = self.getNeighbors(i, j)
        if random.randint(0, 2) == 0:
            i, j = random.choice(neighbors)
            neighbors = self.getNeighbors(i, j)
        explosion = [(i, j)]
        self.balloons[i][j] = BalloonGame.boomCode
        for x, y in neighbors:
            if random.randint(0, 2) == 0:
                self.balloons[x][y] = BalloonGame.boomCode
                explosion.append((x, y))
        self.boomCount += len(explosion)
        return explosion
    def getChanceLeft(self) -> str:
        if self.boomCount == BalloonGame.width * BalloonGame.height:
            return '恭喜呀，你已经打完了所有的气球~'
        guns = BalloonGame.pistol * self.shots
        chances = f'{self.shots}次机会'
        if self.shots == 0:
            return '游戏结束啦！~'
        elif self.shots == 1:
            return f'最后{chances}啦{guns}'
        elif self.shots == 2:
            return f'你现在还有{chances}哦{guns}'
        return f'你总共有{chances}哦{guns}'
    def askAim() -> str:
        return f'请问你要瞄准的是：\nA：{BalloonGame.Balloon()} （如果要瞄准第二行第三个气球直接回复23就好啦）\nB：老板{BalloonGame.boss}'
    def Balloon(bid = '') -> str:
        return f'气球{BalloonGame.balloon}{bid}'
    def getVoucherCount(self):
        return self.boomCount // 2
    def ends(self):
        return self.boomCount == BalloonGame.width * BalloonGame.height or self.shots == 0

def balloon(msg, match: re.Match):
    game = BalloonGame()
    __gameInfo[msg.sender.nick_name] = game
    text = ['打气球咯', str(game), '击中的气球越多获得的奖励也会更多~', game.getChanceLeft(), BalloonGame.askAim()]
    return Message(text, Mode.balloon, balloon_action1)
def balloon_action1(msg):
    if msg.text in ['A', 'a', '气球', BalloonGame.balloon]:
        return Message(f'请问你想瞄准哪个{BalloonGame.Balloon()}呢\n如果要瞄准第二行第三个回复23就好啦', Mode.balloon, balloon_action1)
    elif msg.text in ['B', 'b', '老板', BalloonGame.boss]:
        return balloon_aim_boss(msg.sender.nick_name)
    elif msg.text.isnumeric() and len(msg.text) == 2:
        return balloon_aim_balloon(msg.text, msg.sender.nick_name)
    elif EXIT_CODE in msg.text:
        return Message('被你知道这个可爱的小咒语了哈哈，游戏退出~', Mode.standard)
    return Message(['请回复A或者B或者一个合法的两位数啦', BalloonGame.askAim()], Mode.balloon, balloon_action1)
def balloon_aim_balloon(msgText, sender):
    col, row = divmod(int(msgText), 10)
    row -= 1
    col -= 1
    game: BalloonGame = __gameInfo[sender]
    print(game)
    result = game.shoot(row, col)
    typ = type(result)
    if typ == list and result and result[0] == BalloonGame.aimBoss:
        message: Message = balloon_aim_boss(sender)
        message.insertStart('你不知道为什么突然手一抖，枪口瞄准了老板！')
        return message
    elif typ == int:
        text = '这个气球已经被打爆啦，请再选一个' if result == BalloonGame.madeShot else '你不可以打那里啦'
        return Message([text, BalloonGame.askAim()], Mode.balloon, balloon_action1)
    text = [f'你瞄准了{BalloonGame.Balloon(msgText)}！', '砰！', str(game)]
    if result:
        r, c = result[0]
        balloon = BalloonGame.Balloon(f'{c + 1}{r + 1}')
        neighbors = len(result) - 1
        if row == r and col == c:
            text.append(f'漂亮！你成功打中了那个气球！')
            if neighbors:
                text.append(f'而且由于它和旁边的气球靠得比较近，它同时引爆了旁边的{neighbors}个气球！')
        else:
            text.append(f'啊，你打偏了！你打中了{balloon}！')
            if neighbors:
                text.append(f'不过因为它和旁边的气球靠得比较近，它同时引爆了旁边的{neighbors}个气球！')
            else:
                text.append('不过没事啦，打中哪个气球都一样')
            text += ['下次你一定会打准的！熟练了就好了！', '只要别打到我就行【超小声']
    else:
        text.append('啊，你打歪了！你什么都没打中！')
        text.append('别灰心啦，你下次一定可以的！' if game.shots else '哎哟，游戏而已啦，没什么的')
    text.append(game.getChanceLeft())
    print(result)
    if game.ends():
        return Message(text + balloon_award(sender))
    else:
        return Message(text + [BalloonGame.askAim()], Mode.balloon, balloon_action1)
def balloon_award(name):
    game = __gameInfo[name]
    count = game.getVoucherCount()
    level = list(range(5))
    vouchers = guaVoucher([Voucher(ez.random_pop(level)) for _ in range(count)])
    return ['登登登！', '激动人心的颁奖典礼开始啦', f'“{name}”小朋友可以获得的奖券总共有', (f'{count}张' + count * '！', 2)] + vouchers
def balloon_aim_boss(sender, plot1 = None):
    game: BalloonGame = __gameInfo[sender]
    game.bossAimed += 1
    global __bossAim
    __bossAim += 1
    print(__gameInfo)
    plot1 = plot1 if plot1 != None else random.randint(0, 3)
    print(plot1)
    if plot1 == 0:
        vouchers = [Voucher(i) for i in range(5)]
        random.shuffle(vouchers)
        vouchers = guaVoucher(vouchers)
        text = ['“喂喂喂你干嘛！”老板很紧张，', '“你不要突然把枪对准我啊！！！你瞄准气球啊！！！”', '砰！']
        if random.randint(0, 1):
            person = '老板' if random.randint(0, 2) else '路人'
            text += [f'你手一滑，人一紧张，把{person}打伤了！', f'{person}血流不止!', '你很慌张', '但你趁老板不注意偷走了老板所有的奖券！', '你获得了5张奖券！', \
                     '你逃跑了！', '你逍遥法外！', f'所幸因为抢救及时，{person}并没有死', '在一个夜深人静的晚上，你缩在被窝里']
            if random.randint(0, 1):
                text.append(f'你对{person}的伤感到很内疚，但你仍然刮开了老板的奖券')
            else:
                text.append(f'你对{person}的伤一点也不感到内疚，并且刮开了老板的奖券')
            text += vouchers
            if person == '老板':
                text += ['游戏结束了，老板的心也很受伤，再也不摆他那心爱的气球摊了']
            else:
                text += ['游戏结束了，老板因为危害社会安全被警察叔叔带走了', '老板再摆不了他心爱的气球摊了', '老板希望你早日自首，也好去陪陪他这个孤寡老人']
        else:
            text += ['你一枪打在了气球上！', '还好没有人受伤！', '但老板被你吓出了心脏病！', '老板昏过去了！', '你很慌张，你不知道该怎么做', '但你觉得奖券更重要！', '所以你决定偷走了老板所有的奖券！', '你获得了5张奖券！', \
                    '你逃跑了！', '在一个夜深人静的晚上，你缩在被窝里', '你对老板的事感到很内疚，但你仍然刮开了老板的奖券'] + vouchers + ['游戏结束了，老板的心很受伤，再也不摆他那心爱的气球摊了']
        return Message(text)
    elif plot1 == 1:
        text = ['“喂喂喂你干嘛！”，老板把你的枪口转向了气球', '“你瞄准气球啊！！！瞄准我干什么！！！”']
        if random.randint(0, 1):
            text += ['小朋友，下次不要再干这么危险的事情了啊！', '你认真地嗯了一声（但老板看起来被吓出了心脏病）']
            return Message(text + [game.getChanceLeft(), BalloonGame.askAim()], Mode.balloon, balloon_action1)
        else:
            text += ['老板很生气！']
            if random.randint(1, game.bossAimed):
                firstCommit = '初犯' if game.bossAimed == 1 else '新手'
                text += [f'但看在你是{firstCommit}的份上原谅了你！', '小朋友，下次不要再干这么危险的事情了啊！', '你认真地嗯了一声（但老板看起来被吓出了心脏病）']
                return Message(text + [game.getChanceLeft(), BalloonGame.askAim()], Mode.balloon, balloon_action1)
            else:
                text += ['“你们这群人，一天想着搞事情！”老板愤怒地说，', f'“我今天已经总共被瞄准{__bossAim}次了！”', '老板不开心了！']
                if random.randint(0, __bossAim):
                    text += ['老板收摊了！', '游戏结束！']
                    return Message(text)
                else:
                    text += ['老板邀请你玩了赛马游戏！']
                    hrMsg = horse_race1(sender)
                    hrMsg.insertStart(text)
                    return hrMsg
    elif plot1 == 2:
        plot2 = random.randint(0, 3)
        if plot2 == 0:
            text = ['老板默然而又冷静地看着你', '你觉得自讨没趣，于是放下了枪']
        elif plot2 == 1:
            text = ['老板递给了你一杯果汁', '你接过了果汁，喝了一口', '你觉得老板是个好人，于是放下了枪']
        elif plot2 == 2:
            text = ['老板冲你抛了个媚眼', '你觉得很心动，于是放下了枪']
        elif plot2 == 3:
            game.shots += 1
            text = ['老板以为你没子弹了，过来给你加了一颗子弹', '你获得了额外的一颗子弹！']
        return Message(text + [game.getChanceLeft(), BalloonGame.askAim()], Mode.balloon, balloon_action1)
    elif plot1 == 3:
        text = ['“喂喂喂你干嘛！”老板很紧张，', '“你不要突然把枪对准我啊！！！你瞄准气球啊！！！”', '只听你冷冷地说了一句：', '“劫色。”']
        if random.randint(0, 1):
            text += ['老板害羞地点了点头，哦不低下了头', '从此你和老板过上了没羞没臊的幸福生活', '你忘记了打气球这个游戏！', '游戏结束！']
            return Message(text)
        else:
            text += ['老板宁死不屈！', '你扣动了扳机！', '但是！', '枪里其实已经没有子弹了！', '你放了空枪！', '老板觉得这是个机会', '老板扑了过来！', \
                '你被老板推倒了！']
            if random.randint(1, __bossAim):
                text += ['老板觉得你很可爱', '你被老板劫色了！', '游戏结束！']
                return Message(text)
            else:
                text += ['老板坐在你身上，什么话也没说，就盯着你', '你看着老板的眼睛，对刚刚这个玩笑很过意不去，就赧着脸撇了句对不起',
                        f'老板看在这只是他今天第{__bossAim}次被人欺负的份上就原谅了你']
                if game.shots > 1:
                    game.shots = 1
                    text += ['但是老板只允许你最多再打一枪了']
                else:
                    game.shots = 3
                    text += ['但是老板看在你觉得他姿色不错的份上，多给了你两次机会！', game.getChanceLeft()]
                text += ['游戏继续！']
                return Message(text + [BalloonGame.askAim()], Mode.balloon, balloon_action1)
    return Message('游戏结束')

