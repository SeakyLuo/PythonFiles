from wxpy import *

limits = {
    '1': 8,
    '2': 8,
    '3': 8,
    '4': 8,
    '5': 8,
    '6': 8,
    '7': 9,
    '8': 9,
    '9': 9,
    '10': 9,
    '11': 9,
    '12': 9
}
d, ids = {}, []
def setup():
    global d, ids
    d = { k: [] for k in limits }
    ids = []

if __name__ == '__main__':
    setup()
    bot = Bot(cache_path = True)
    bot.enable_puid()
    group = next(g for g in bot.groups() if g.name == '测试用')
    @bot.register(group, msg_types = TEXT, except_self = False)
    def Main(msg):
        text = msg.text
        if text not in d: return
        puid = msg.member.puid
        if puid in ids: return
        if len(d[text]) < limits[text]:
            d[text].append(msg.member.name)
            ids.append(puid)
            reply = '\n'.join(f'{k}：{v}（{ f"剩{diff}" if (diff := limits[k] - len(v)) else "满"}）' for k, v in d.items())
            msg.reply(reply)
    # 进入 Python 命令行、让程序保持运行
    embed()
