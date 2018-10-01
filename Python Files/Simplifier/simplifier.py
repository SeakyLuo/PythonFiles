from tkinter import *
from tkinter import messagebox
from eztk import *
import ez

root=Tk()
root['bg']='MintCream'
try:
    t1txt='t1.txt'
    btxt='button.txt'
    open(t1txt,'x').close()
    open(btxt,'x').close()
except FileExistsError: pass

t1=Text(root)
def monitor(event):
    t=gettxt(t1)
    if not t or t==ez.fread(t1txt):
        return
    ez.fwrite(t1txt,t)
    txt=ez.fread(btxt,0)
    if txt: eval(txt)
t1.bind('<KeyRelease>',monitor)

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
def newline():
    t=gettxt(t1)
    new=''
    for i,ch in enumerate(t):
        if ch=='\n' and t[i+1:i+3]!='- ':
            new+=' '
        else:
            new+=ch
    inst2(new,'newline()')
w3=Button(root,text="\\n",command=newline)
def brackets():
    t=gettxt(t1)
    new=''
    stop=0
    d={'[':']','(':')','{':'}','（':'）','【':'】',0:None}
    for ch in t:
        if ch in d and not stop and t.count(ch)==t.count(d[ch]):
            stop=ch
        elif ch==d[stop]:
            stop=0
        elif not stop:
            new+=ch
    inst2(new,'brackets()')
w4=Button(root,text='([{}])',command=brackets)
t2=Text(root)

ws=[w0,w1,w2,w3,w4]
t1.grid(row=0,column=0,columnspan=len(ws))
for i,w in enumerate(ws):
    w.configure(relief=FLAT,bg='SeaGreen1')
    w.grid(row=1,column=i,sticky=NS)
t2.grid(row=2,column=0,columnspan=len(ws))

def inst2(text,caller):
    ez.fwrite(btxt,caller)
    deltxt(t2)
    instxt(t2,text)
    linecount('<KeyRelease>')
    try: ez.cpc(text)
    except UnicodeError: messagebox.showerror('Error','You need to copy it to your clipboard manually.')
    
root.mainloop()
