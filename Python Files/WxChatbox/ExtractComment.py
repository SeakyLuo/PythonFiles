from wxpy import *
from docx import Document
import os

user = '黄懒懒-o-'
# user = '头像我老婆'

# 备注 --- 真名
name_map = {
    '王也钦': '王也钦',
    '陈芊伊': '陈芊伊',
    '朱泽亮': '朱泽亮',
    '倪佳纯': '倪佳纯',
    user: '黄滢',
    '陈菲': '陈菲',
    '韩雨露': '韩雨露',
    '李泳霖': '李泳霖',
    '陈倚天': '陈倚天',
    '孙颖': '孙颖',
    '申嘉': '申嘉',
    '咏絮': '咏絮',
    '丁一': '丁一',
    '庄楠': '庄楠',
    '叶龙荣': '叶龙荣',
    '唐雯琳': '唐雯琳'
}

classmates = []

comments_map = {}

def setup(msg):
    global classmates, comments_map
    classmates.extend(msg.split(' '))
    for classmate in classmates:
        comments_map[classmate] = { name: '' for name in name_map }
    print('开始记录')

def save(filename, content):
    with open(filename + '.txt', 'w') as f:
        f.write(content)
    # document = Document()
    # paragraph = document.add_paragraph(content)
    # document.save(filename + '.docx')
    print('文件已保存')

if __name__ == '__main__':
    bot = Bot(cache_path = True)
    bot.enable_puid()
    @bot.register(msg_types = TEXT, except_self = False)
    def Main(msg):
        message = msg.text
        sender = msg.sender.name
        if sender == user:
            if classmates == []:
                setup(message)
                return
            if message == '好了':
                desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
                filename = os.path.join(desktop, '关于' + ''.join(classmates) + '同学的会议记录')
                seperator = '\n' + '=' * 10 + '分割线' + '=' * 10 + '\n'
                content = seperator.join("\n".join(f'{name_map[name]}：{comment}' for name, comment in comments.items()) for classmate, comments in comments_map.items())
                save(filename, content)
                return
        for text in message.split('\n'):
            for classmate in classmates:
                if classmate in text:
                    print(f'收到来自于{sender}对{classmate}的评价')
                    comments_map[classmate][sender] = text
                    if sender not in name_map:
                        name_map[sender] = sender
    # 进入 Python 命令行、让程序保持运行
    embed()