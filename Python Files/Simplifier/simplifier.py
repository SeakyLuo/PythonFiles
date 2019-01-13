from tkinter import *
from tkinter import messagebox
from eztk import *
import ez
from win32 import win32clipboard

class Simplifier(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Simplifier')
        self.btxt = 'button.txt'
        try: open(self.btxt, 'x').close()
        except FileExistsError: pass
        self.wrappers = ez.fread(self.btxt, True)
        if self.wrappers == '':
            self.wrappers = {'newline': 0, 'brackets': 0, 'numbers': 0, 'smartnl': 1,'space': 1, 'autocopy': 1,\
                             'punc': 'en', 'translate': 0, 'lines': 1, 'chars': 0, 'fontsize': 10}
        self.history = ['']
        self.pointer = 0
        self.ctrlCounter = self.yzCounter = 0
        self.brackets = {'[': ']', '(': ')', '{': '}', '（': '）',\
        '【': '】', '<': '>', '《': '》', '『': '』', '「': '」'}
        self.rbrackets = { self.brackets[key]: key for key in self.brackets }
        
        self.buttonbar = Frame(self)
        self.input = Frame(self)
        self.widgetbar = Frame(self)
        self.output = Frame(self, width = 600, height = 450)
        self.output.grid_propagate(False)
        frames = [self.buttonbar, self.input, self.widgetbar, self.output]
        self.t1 = Text(self.input)
        self.scrollb1 = Scrollbar(self.input, command = self.t1.yview)
        self.t1.bind('<KeyRelease>', self.monitor)
        self.t1.bind('<Control-z>', lambda event: self.undo())
        self.t1.bind('<Control-y>', lambda event: self.redo())
        self.t2 = Text(self.output)
        self.scrollb2 = Scrollbar(self.output, command = self.t2.yview)
        self.w0 = Label(self.widgetbar, text = 'In↑Out↓')
        self.w1 = Button(self.widgetbar, command = self.lineCount)
        self.w2 = Button(self.widgetbar, command = self.charCount)
        self.w3 = Button(self.widgetbar, text = 'Clear',command = self.clear)
        self.w4 = Button(self.widgetbar, text = 'AutoCopy', command = self.autocopy)
        self.w5 = Button(self.widgetbar, text = 'Paste', command = self.paste)
        self.w6 = Button(self.widgetbar, text = 'Undo', command = self.Undo)
        self.w7 = Button(self.widgetbar,text = 'Redo', command = self.Redo)
        self.w8 = Scale(self.widgetbar, from_ = 5, to = 50, orient = HORIZONTAL,\
                        showvalue = 0, command = lambda event: self.fontSize())
        self.b0 = Button(self.buttonbar, text = "\\n", command = lambda: self.remover('newline'))
        self.b1 = Button(self.buttonbar, text = '([{}])', command = lambda: self.remover('brackets'))
        self.b2 = Button(self.buttonbar, text = '1', command = lambda: self.remover('numbers'))
        self.b3 = Button(self.buttonbar, text = 'smartnl', command = lambda: self.remover('smartnl'))
        self.b4 = Button(self.buttonbar, text = 'space', command = lambda: self.remover('space'))
        self.b5 = Button(self.buttonbar, text = 'translate', command = lambda: self.remover('translate'))
        self.b6 = Button(self.buttonbar, text = self.wrappers['punc'] if self.wrappers['punc'] else 'Punctuation', command = self.switch_punc)
        buttons = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6]
        widgets = [self.w0, self.w1, self.w2, self.w3, self.w4, self.w5, self.w6, self.w7, self.w8]
        self.wd = {'newline': self.b0, 'brackets': self.b1, 'numbers': self.b2, 'smartnl': self.b3, \
        'autocopy': self.w4, 'space': self.b4, 'translate': self.b5, 'punc': self.b6}
        columnspanLength = max(len(widgets),len(buttons))
        for sb, t in zip([self.scrollb1, self.scrollb2], [self.t1, self.t2]):
            t.grid(row = 0, column = 0, sticky = NSEW)
            t['yscrollcommand'] = sb.set
            sb.configure(relief = FLAT, borderwidth = 0)
            sb.grid(row = 0, column = 1, sticky = NS)
        for f in frames:
            f['bg'] = 'MintCream'
            f.pack(fill = BOTH, expand = 1)
            f.rowconfigure(0, weight = 1)
            f.columnconfigure(0, weight = 1)
        for w in buttons:
            w.configure(relief = FLAT, bg = 'SeaGreen1')
            w.pack(side = LEFT, fill = Y, expand = 1)
        for w in widgets:
            w.configure(relief = FLAT, bg = 'thistle1')
            w.pack(side = LEFT, fill = Y, expand = 1)
        self.wrapper()
        self.w8.set(self.wrappers['fontsize'])
        self.fontSize()

    def monitor(self, event):
        t = gettxt(self.t1)
        if not t or t == self.history[-1]:
            return
        if self.ctrlCounter and 'Control' in event.keysym:
            self.ctrlCounter -= 1
        elif self.yzCounter and event.keysym in ['y', 'z']:
            self.yzCounter -= 1
        else:
            self.history = self.history[:self.pointer + 1] + [t]
            self.pointer = len(self.history) - 1
        self.wrapper()
        self.countLines()
        self.countChars()
    def countLines(self):
        if self.wrappers['lines']: 
            count = lambda t: t.count('\n')+(t[-1] != '\n') if t else 0
            up = count(gettxt(self.t1))
            down = count(gettxt(self.t2))
            self.w1['text'] = f'Lines↑{up}↓{down}'
        else:
            self.w1['text'] = 'LineCount'
    def lineCount(self):
        self.wrappers['lines'] = int(not self.wrappers['lines'])
        self.countLines()
    def countChars(self):
        if self.wrappers['chars']:
            up = len(gettxt(self.t1))
            down = len(gettxt(self.t2))
            self.w2['text'] = f'Chars↑{up}↓{down}'
        else:
            self.w2['text'] = 'CharCount'
    def charCount(self):
        self.wrappers['chars'] = int(not self.wrappers['chars'])
        self.countChars()
    def clear(self):
        deltxt(self.t1)
        deltxt(self.t2)
    def autocopy(self):
        self.switchButtonState(self.w4, 'autocopy')
        ez.fwrite(self.btxt, self.wrappers)
        ez.cpc(gettxt(self.t2))
    def paste(self):
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        instxt(self.t1, data)
        self.wrapper()
    def undo(self):
        if not self.pointer:
            return
        self.pointer -= 1
        deltxt(self.t1)
        instxt(self.t1, self.history[self.pointer])
        self.ctrlCounter = self.yzCounter = 1
    def Undo(self):
        self.undo()
        self.wrapper()
    def redo(self):
        if self.pointer == len(self.history) - 1:
            return
        self.pointer += 1
        deltxt(self.t1)
        instxt(self.t1, self.history[self.pointer])
        self.ctrlCounter = self.yzCounter = 1
    def Redo(self):
        self.redo()
        self.wrapper()
    def fontSize(self):
        value = int(self.w8.get())
        self.wrappers['fontsize'] = value
        self.w8['label'] = 'FontSize: ' + str(value)
        self.t2['font'] = ('TkFixedFont', value)
    def wrapper(self):
        string = gettxt(self.t1)
        for func in self.wd:
            if not self.wrappers[func]: continue
            if func == 'newline': string = self.newline_remover(string)
            elif func == 'brackets': string = self.brackets_remover(string)
            elif func == 'numbers': string = self.numbers_remover(string)
            elif func == 'smartnl': string = self.smart_newline_remover(string)
            elif func == 'punc': string = self.punc_switch(string)
            self.wd[func]['relief'] = GROOVE
        
        if self.wrappers['space']: string = self.space_remover(string)
        if self.wrappers['translate']: string = self.translate(string)
        ez.fwrite(self.btxt, self.wrappers)
        deltxt(self.t2)
        instxt(self.t2, string)
        self.countLines()
        self.countChars()
        if self.wrappers['autocopy']:
            try:
                ez.cpc(string)
            except UnicodeError:
                messagebox.showerror('Error','You need to copy it to your clipboard manually.')
    def switchButtonState(self, button, name):
        if button['relief'] == GROOVE: # turn off
            button['relief'] = FLAT
            self.wrappers[name] = 0
        else: # turn on
            button['relief'] = GROOVE
            self.wrappers[name] = 1
    def remover(self, name):
        self.switchButtonState(self.wd[name], name)
        self.wrapper()
    def newline_remover(self, string):
        new = ''
        for i,ch in enumerate(string):
            new += ' ' if ch == '\n' else ch  
        return new.strip()
    def brackets_remover(self, string):
        new = ''
        left = { key: 0 for key in self.brackets }
        right = []
        for ch in string:
            if ch in self.brackets:
                left[ch] += 1
                right.append(self.brackets[ch])
            elif ch in right:
                left[self.rbrackets[ch]] -= 1
                right.remove(ch)
            elif all(left[b] == 0 for b in left):
                new += ch
        return new
    def numbers_remover(self, string):
        new = ''
        for ch in string:
            new += '' if ch.isnumeric() else ch
        return new
    def smart_newline_remover(self, string):
        new = ''
        length = len(string)
        notEnd = [',', '，', ';', ':', \
                '[', ']','(', ')','{', '}','（', '）',\
                '【', '】','<', '>','《', '》',\
                '『', '』','「', '」']
        noSpace = ['•', '-', '–', '—']
        for i, ch in enumerate(string):
            if ch == '\n' and i and i + 1 < length:
                if string[i + 1] not in noSpace and \
                (string[i - 1].isalnum() or string[i - 1] in notEnd):
                    new += ' '
                elif string[i - 1] in noSpace:
                    new += ''
                else:
                    new += ch
            else:
                new += ch
        return new.strip()
    def space_remover(self, string):
        return ez.sub(string, ' ,',',','  ',' ',' .','.',' 。','。',' ，','，')
    def switch_punc(self):
        texts = ['Punctuation', 'en', 'zh']
        states = [0] + texts[1:]
        next_index = (states.index(self.wrappers['punc']) + 1) % len(states) 
        self.wrappers['punc'] = states[next_index]
        self.b6['text'] = texts[next_index]
        if next_index == 0: self.b6['relief'] = FLAT
        self.wrapper()
    def punc_switch(self, string):
        zh2en = ['‘', '\'','“','"', '’', '\'', '”', '"', '，', ',', '。', '.', '：', ':', '；', ';', '【', '[', '】', ']',\
                 '—', '-', '、', '\\']
        if self.wrappers['punc'] == 'en':
            string = ez.sub(string, *zh2en)
        elif self.wrappers['punc'] == 'zh':
            en2zh = []
            for i in range(0, len(zh2en), 2): en2zh += [zh2en[i + 1], zh2en[i]]
            string = ez.sub(string, *en2zh)
        return string
    def translate(self, string):
        try:
            if len(string) > 5000:
                messagebox.showwarning('Warning', 'String length can\'t exceeds 5000!')
            return ez.translate(string)
        except Exception as e:
            if e is UnicodeError:
                messagebox.showerror('Error', 'Can\'t translate!')
            else:
                messagebox.showerror('Error', 'No Network!')
            self.remover('translate')
            return string
        
app = Simplifier()
app.mainloop()
ez.py2pyw(__file__)
