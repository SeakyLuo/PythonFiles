from wxpy import *
from rules import *

if __name__ == '__main__':
    bot = Bot(cache_path=True)  # 生成机器人实例，启动缓存避免重复登录

    found = bot.friends().search('头像我老婆', sex = 1)  # 在好友列表中搜索名字是'头像我老婆'性别为1(男)的一项
    boyfriend = ensure_one(found)  # 确保只有一个结果

    recv = []
    sent = []

    @bot.register([boyfriend, bot.self], msg_types = TEXT, except_self = True)
    def send(msg):
        recv.append(msg)
        message = '我有点笨，能不能迁就下我，我们说点别的？'
        for rule, reply in regex.items():
            match = re.search(rule, msg.text, re.IGNORECASE)
            if match:
                try:
                    message = reply(msg, match, recv, sent)
                except ResponseError as e:
                    message = e.err_msg
                    print(e.err_code, e.err_msg)  # 查看错误号和错误消息
                finally:
                    break
        msg.sender.send_msg(message)
        sent.append(message)

    # 进入 Python 命令行、让程序保持运行
    embed()
