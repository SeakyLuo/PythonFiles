from wxpy import *
from rules import *
import time, os

def sendText(msg, allowChat = True):
    info: Info = infoDict.setdefault(msg.sender.nick_name, Info())
    if info.inProcess:
        return
    info.inProcess = True
    message = Message()
    info.recv.append(Message(msg.text))
    if info.mode != Mode.standard:
        message = info.action(msg)
    else:
        for rule, reply in regex.items():
            match = re.search(rule, msg.text.strip(), re.IGNORECASE)
            if match and len(match.groups()):
                try:
                    message: Message = reply(msg, match)
                    if message.mode == Mode.memo:
                        memo.save()
                except ResponseError as e:
                    info.error.append(Message(e.err_msg, e.err_code))
                    message.text = [e.err_msg]
                    print(e.err_msg)
                except Exception as e:
                    message.text = [f'Error: {e.with_traceback()}']
                    print(e)
                finally:
                    break
    if not allowChat or not message.isDefault():
        for text, latency in message.text:
            time.sleep(latency)
            msg.sender.send_msg(text)
    info.appendReply(message)
    info.inProcess = False

def sendFile(msg):
    info = infoDict.get(msg.sender.nick_name, Info())
    match = re.search(r'file\((.*)\)', msg.text.strip(), re.IGNORECASE)
    if not match:
        return
    path = match[1].replace('/', '\\')
    if 'desktop' in path.lower() and not path.startswith(ez.desktop):
        path = ez.desktop + re.search(r'desktop\\([\s\S]*)', path, re.IGNORECASE)[1]
    if '.lnk' in path:
        finder = ez.find(path)
        shortcut = finder.before('.lnk') + '.lnk'
        path = ez.getlnk(shortcut) + finder.after('.lnk')
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    if basename in os.listdir(dirname):
        msg.sender.send_file(path)
    else:
        msg.sender.send_msg('文件没找到呜呜呜')

def balloonGame(msg):
    info: Info = infoDict.setdefault(msg.sender.nick_name, Info())
    if info.inProcess:
        return
    info.inProcess = True
    message = Message()
    info.recv.append(Message(msg.text))
    if info.mode != Mode.standard:
        message = info.action(msg)
    else:
        try:
            match = re.search(BALLOON, msg.text.strip(), re.IGNORECASE)
            if match:
                message: Message = balloon(msg, match)
        except ResponseError as e:
            info.error.append(Message(e.err_msg, e.err_code))
            message.text = [e.err_msg]
            print(e.err_msg)
    if not message.isDefault():
        for text, latency in message.text:
            time.sleep(latency)
            msg.sender.send_msg(text)
    info.appendReply(message)
    info.inProcess = False

if __name__ == '__main__':
    bot = Bot(cache_path = True)
    me = ensure_one(bot.friends().search('头像我老婆'))
    # @bot.register([me], msg_types = TEXT)
    # def test(msg):
    #     sendText(msg, True)

    # friends = [ensure_one(bot.friends().search(remark_name = name)) for name in ['Me', '耿沈琪Cathy', '陈格', '刘恒宇', '林天承', '王旖旎', '张子豪Dennis']]
    # @bot.register(friends, msg_types = TEXT)
    @bot.register()
    def playGalloonGame(msg):
        balloonGame(msg)

    # @bot.register([ensure_one(bot.friends().search(remark_name = 'Me'))])
    # def fetchFile(msg):
    #     sendFile(msg)

    # 进入 Python 命令行、让程序保持运行
    embed()
