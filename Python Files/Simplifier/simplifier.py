from tkinter import *
from tkinter import messagebox
from eztk import *
import ez

root=Tk()
root['bg']='MintCream'
root.title('Simplifier')
try:
    t1txt='t1.txt'
    btxt='button.txt'
    open(t1txt, 'x').close()
    open(btxt, 'x').close()
except FileExistsError: pass

t1=Text(root)

history = ['']
pointer = 0
ctrlCounter = yzCounter = 0
wrappers = ez.fread(btxt, False)

def monitor(event):
    global history, pointer, ctrlCounter, yzCounter
    t=gettxt(t1)
    if not t or t == history[-1]:
        return
    ez.fwrite(t1txt,t)
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

w0=Label(root,text='Input:↑')
def linecount(event):
    count=lambda t:t.count('\n')+(t[-1]!='\n') if t else 0
    up=count(gettxt(t1))
    down=count(gettxt(t2))
    w1['text']=f'LineCount:↑{up}↓{down}'
root.bind('<KeyRelease>', linecount)
w1=Label(root,text='LineCount')
def clear():
    deltxt(t1)
    deltxt(t2)
w2=Button(root,text='Clear',command=clear)

def wrapper():
    global wrappers, wd
    string=gettxt(t1)
    funcs = wrappers.split('\n')
    wrappers = ''
    for func in wd:
        if func not in funcs: continue
        if func == 'newline': string = newline_remover(string)
        elif func == 'brackets': string = brackets_remover(string)
        elif func == 'numbers': string = numbers_remover(string)
        wd[func]['relief'] = GROOVE
        wrappers += func + '\n'
    inst2(string)
def switchButtonState(button, name):
    global wrappers
    name += '\n'
    if button['relief'] == GROOVE: # turn off
        button['relief'] = FLAT
        wrappers = wrappers.replace(name, '')
    else: # turn on
        button['relief'] = GROOVE
        wrappers += name

def remove_newline():
    global w3
    switchButtonState(w3, 'newline')
    wrapper()
def newline_remover(string):
    new=''
    for i,ch in enumerate(string):
        new += ' ' if ch=='\n' and string[i+1:i+3]!='- ' else ch
    return new
w3 = Button(root,text="\\n",command=remove_newline)

def remove_brackets():
    global w4
    switchButtonState(w4, 'brackets')
    wrapper()
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
w4 = Button(root,text='([{}])',command=remove_brackets)

def remove_numbers():
    global w5
    switchButtonState(w5, 'numbers')
    wrapper()
def numbers_remover(string):
    new=''
    for ch in string:
        new += '' if ch.isnumeric() else ch
    return new
w5 = Button(root,text='1',command=remove_numbers)    

ws = [w0, w1, w2, w3, w4, w5]
wd = {'newline': w3, 'brackets': w4, 'numbers': w5}
t1.grid(row=0,column=0,columnspan=len(ws))
for i,w in enumerate(ws):
    w.configure(relief=FLAT,bg='SeaGreen1')
    w.grid(row=1,column=i,sticky=NS)
t2=Text(root)
t2.grid(row=2,column=0,columnspan=len(ws))

def inst2(text):
    global wrappers
    ez.fwrite(btxt, wrappers)
    deltxt(t2)
    instxt(t2, text)
    linecount('<KeyRelease>')
    try: ez.cpc(text)
    except UnicodeError: messagebox.showerror('Error','You need to copy it to your clipboard manually.')

if wrappers: wrapper()
root.mainloop()
