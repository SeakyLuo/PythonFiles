from tkinter import *
from tkinter import messagebox
from eztk import *
import ez

root=Tk()
root['bg']='MintCream'
root.title('Simplifier')
btxt='button.txt'
try: open(btxt, 'x').close()
except FileExistsError: pass

t1=Text(root)

history = ['']
pointer = 0
ctrlCounter = yzCounter = 0
wrappers = ez.fread(btxt, True)
if wrappers == '':
    wrappers = {'newline': 0, 'brackets': 0, 'numbers': 0, 'smartnl': 1,'space': 1, 'autocopy': 1, 'translate': 0}

def monitor(event):
    global history, pointer, ctrlCounter, yzCounter
    t=gettxt(t1)
    if not t or t == history[-1]:
        return
    if ctrlCounter and 'Control' in event.keysym:
        ctrlCounter -= 1
    elif yzCounter and event.keysym in ['y', 'z']:
        yzCounter -= 1
    else:
        history = history[:pointer + 1] + [t]
        pointer = len(history) - 1
    wrapper()
t1.bind('<KeyRelease>',monitor)

def undo(event):
    global history, pointer, ctrlCounter, yzCounter
    if not pointer: return
    pointer -= 1
    deltxt(t1)
    instxt(t1, history[pointer])
    ctrlCounter = yzCounter = 1
t1.bind('<Control-z>', undo)
def redo(event):
    global history, pointer, ctrlCounter, yzCounter
    if pointer == len(history) - 1: return
    pointer += 1
    deltxt(t1)
    instxt(t1, history[pointer])
    ctrlCounter = yzCounter = 1
t1.bind('<Control-y>', redo)

w0=Label(root,text='In↑Out↓')
def lineCount(event):
    count = lambda t:t.count('\n')+(t[-1] != '\n') if t else 0
    up = count(gettxt(t1))
    down = count(gettxt(t2))
    w1['text']=f'Lines↑{up}↓{down}'
root.bind('<KeyRelease>', lineCount)
w1 = Label(root,text='lineCount')
def clear():
    deltxt(t1)
    deltxt(t2)
w2 = Button(root,text='Clear',command=clear)
def autocopy():
    switchButtonState(w3, 'autocopy')
    ez.fwrite(btxt, wrappers)
    ez.cpc(gettxt(t2))
w3 = Button(root,text = 'AutoCopy', command = autocopy, relief = FLAT)
def charCount(event):
    w4['text']='Chars↓' + str(len(gettxt(t2)))
root.bind('<KeyRelease>', charCount)
w4 = Label(root,text='Chars:↓0')

def wrapper():
    global wrappers, wd
    string=gettxt(t1)
    for func in wd:
        if wrappers.get(func, 0):
            if func == 'newline': string = newline_remover(string)
            elif func == 'brackets': string = brackets_remover(string)
            elif func == 'numbers': string = numbers_remover(string)
            elif func == 'smartnl': string = smart_newline_remover(string)
            wd[func]['relief'] = GROOVE
            
    if wrappers['space']: string = space_remover(string)
    if wrappers['translate']: string = translate(string)
    ez.fwrite(btxt, wrappers)
    deltxt(t2)
    instxt(t2, string)
    lineCount('<KeyRelease>')
    if wrappers['autocopy']:
        try:
            ez.cpc(string)
        except UnicodeError:
            messagebox.showerror('Error','You need to copy it to your clipboard manually.')
def switchButtonState(button, name):
    global wrappers
    if button['relief'] == GROOVE: # turn off
        button['relief'] = FLAT
        wrappers[name] = 0
    else: # turn on
        button['relief'] = GROOVE
        wrappers[name] = 1
def remover(name):
    global wd
    switchButtonState(wd[name], name)
    wrapper()
    
def newline_remover(string):
    new=''
    length = len(string)
    for i,ch in enumerate(string):
        new += ' ' if ch == '\n' else ch  
    return new.strip()
b0 = Button(root,text="\\n",command=lambda: remover('newline'))
def brackets_remover(string):
    new=''
    stop=0
    d={'[':']','(':')','{':'}','（':'）',\
       '【':'】','<':'>','《':'》',\
       '『':'』','「':'」',0:None}
    for ch in string:
        if ch in d and not stop and string.count(ch)==string.count(d[ch]):
            stop=ch
        elif ch==d[stop]:
            stop=0
        elif not stop:
            new+=ch
    return new
b1 = Button(root,text='([{}])',command=lambda: remover('brackets'))
def numbers_remover(string):
    new=''
    for ch in string:
        new += '' if ch.isnumeric() else ch
    return new
b2 = Button(root,text='1',command=lambda: remover('numbers'))
def smart_newline_remover(string):
    new = ''
    length = len(string)
    notEnd = [',', '-','，' ,'–','—',']',')','}','）','】','>','》','』','」']
    for i, ch in enumerate(string):
        if ch == '\n' and \
           (i + 1 < length and string[i + 1] not in ['•','-' ,'–','—']) and \
           (i > 1 and (string[i - 1].isalnum() or string[i - 1] in notEnd)):
            new += ' '
        else:
            new += ch
    return new.strip()
b3 = Button(root,text='smartnl',command=lambda: remover('smartnl'))
def space_remover(string):
    return ez.sub(string, ' ,',',','  ',' ',' .','.',' 。','。',' ，','，')
b4 = Button(root,text='space',command=lambda: remover('space'))
def translate(string):
    return ez.translate(string)
b5 = Button(root,text='translate',command=lambda: remover('translate'))

buttons = [b0, b1, b2, b3, b4, b5]
widgets = [w0, w1, w2, w3, w4]
wd = {'newline': b0, 'brackets': b1, 'numbers': b2, 'smartnl': b3, 'autocopy': w3, 'space': b4, 'translate': b5}
columnspanLength = max(len(widgets),len(buttons))
for i,w in enumerate(buttons):
    w.configure(relief=FLAT,bg='SeaGreen1')
    w.grid(row=0,column=i,sticky=NS)
t1.grid(row = 1,column = 0,columnspan = columnspanLength, sticky = EW)
for i,w in enumerate(widgets):
    w.configure(relief=FLAT,bg='thistle1')
    w.grid(row=2,column=i,sticky=NS)
t2=Text(root)
t2.grid(row = 3,column = 0,columnspan = columnspanLength, sticky = EW)
for col in range(columnspanLength): root.columnconfigure(col, weight = 1)
for row in range(4): root.rowconfigure(row, weight = 1)

wrapper()
root.mainloop()

ez.py2pyw('simplifier.py')
