from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from ez import find, fread, fwrite
from eztk import *
import lyrics, os
import atexit

root = Tk()
root.title("Search&Set Lyrics")
bgcolor = 'MintCream'
root['bg'] = bgcolor
global sc, st
sc = st = 0
defaultPath = lyrics.defaultPath
if 'previous.txt' not in os.listdir():
    fwrite('previous.txt', defaultPath)
else:
    info = fread('previous.txt')
    if info:
        info = info.replace('\ufeff', '')
        defaultPath = os.path.normpath(info)

def search():
    global sc
    title = getText(titleText)
    if title == '':
        messagebox.showerror('错误', '没有歌名怎么让人家帮你搜啦')
        return
    sc = lyrics.Searcher(title = title, artist = getArtist())

def Set():
    global st
    st = lyrics.Setter(path = os.path.join(getPath(), getText(titleText)), artist = getArtist())
    response = getText(commandText)
    if response in ['ow', 'overwrite']:
        st.add(source = '', overwrite = True)
    else:
        for flag in ['ow = ', 'overwrite = ', 'ow=', 'overwrite=']:
            if response.startswith(flag):
                st.add(source = '', overwrite = eval(find(response).after(flag)))
                break
        else:
            st.add(source = '', overwrite = False)

def read():
    global sc, st
    title = getText(titleText)
    if title:
        try:
            st = lyrics.Setter(path = os.path.join(getPath(), title), artist = getArtist())
        except FileNotFoundError:
            pass
    if st:
        st.read()
    elif sc:
        All = getText(commandText)
        if All in ['True', 'False']:
            All = eval(All)
        else:
            All = 1
        sc.read(All)
    else:
        st = lyrics.Setter(path = getPath(), artist = getArtist())
        st.read()

def execute():
    instruction = '''Command Arguments:
save   --- save
       --- saveAs
       --- saveAs = lrc
       --- save("lrc", "True")
       --- save(saveAs = "lrc", ALL = "True")
next   --- next
       --- next(2)
delete --- del
       --- del("告白气球")
reset  --- reset
       --- reset("告白气球")
help   --- help
'''
    response = getText(commandText)
    if response == 'help' or response == '':
        print(instruction)
        return
    global sc, st
    fd = find(response)
    try:
        if response.startswith('save'):
            if not sc:
                return
            if response == 'save':
                sc.save()
            elif response.startswith('saveAs'):
                sc.save(fd.after('saveAs = '))
            else:
                 eval(response)
        elif response.startswith('next'):
            number = fd.after('next').strip()
            if number:
                number = eval(number)
            else:
                number = -1
            if st:
                st.next(number)
            elif sc:
                sc.next(number)
        elif response.startswith('del'):
            if not st:
                path = fd.between('(', ')')
                if not path:
                    path = pathText.get()
                st = lyrics.Setter(path)
            if response == 'del':
                st.delete()
            else:
                eval(response)
        elif response.startswith('reset'):
            arg = fd.between('(', ')')
            response = input('请输入想要重设的歌词~\n>>>')
            if not response:
                return
            st.reset(response, arg)
    except:
        print(instruction)

def switch(event):
    key = event.keysym
    widget = event.widget
    index = textList.index(widget)
    if key == 'Up':
        textList[index-1].focus()
    elif key == 'Down':
        textList[(index+1)%len(textList)].focus()

def getPath():
    global defaultPath
    defaultPath = getText(pathText)## os.path.normcase(getText(pathText))
    if os.path.isdir(defaultPath):
        fwrite('previous.txt', defaultPath)
    return defaultPath

def getArtist():
    return getText(artistText)

titleLabel = Label(root, text = 'Title: ')
titleText = Text(root)
titleText.focus()

artistLabel = Label(root, text = 'Artist: ')
artistText = Text(root)

def askdirectory():
    if (path := os.path.normpath(filedialog.Directory().show())) == '':
        return
    defaultPath = path
    setText(pathText, defaultPath)
    fwrite('previous.txt', defaultPath)
pathLabel = Button(root, text = 'Path: ', command = askdirectory)
pathText = Text(root)
pathText.insert(1.0, defaultPath)

commandLabel = Label(root, text = 'Command: ')
commandText = Text(root)

labelList = [titleLabel, artistLabel, pathLabel, commandLabel]
textList = [titleText, artistText, pathText, commandText]
for i, (label, text) in enumerate(zip(labelList, textList)):
    label.configure(width = 10, height = 1, bg = bgcolor, relief = FLAT)
    label.grid(row = i, column = 0)
    text.configure(width = 60, height = 1, bg = 'MistyRose', font = 'TkDefaultFont', relief = FLAT)
    text.grid(row = i, column = 1, columnspan = 3)
    text.bind('<KeyRelease>', switch)

b1 = Button(root, text = "Search", command = search)
b2 = Button(root, text = "Set", command = Set)
b3 = Button(root, text = "Read", command = read)
b4 = Button(root, text = "Execute", command = execute)
for i, b in enumerate([b1, b2, b3, b4]):
    b.grid(row = 4 + i // 2, column = 1 + i % 2, sticky = NSEW)
    b.configure(relief = FLAT, bg = 'lavender')

root.mainloop()
