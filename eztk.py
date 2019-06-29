from tkinter import *
import time, threading

def getText(text):
    return text.get(1.0, END).strip()

def clearText(text):
    text.delete(1.0, END)

def setText(text, content):
    text.insert(1.0, content)

def setEntry(entry, text):
    entry.delete(0, END)
    entry.insert(0, text)

def clearEntry(entry):
    entry.delete(0, END)

def setEntryHint(entry, hint, hintTextColor = 'grey39'):
    def focusIn(event):
        clearEntry(entry)
        entry['fg'] = color
    def focusOut(event):
        if not entry.get():
            setEntry(entry, hint)
            entry['fg'] = hintTextColor
    color = entry['fg']
    entry.bind('<FocusIn>', focusIn)
    entry.bind('<FocusOut>', focusOut)
    setEntry(entry, hint)
    entry['fg'] = hintTextColor

class LoadDialog(Toplevel):
    def __init__(self, master, message = 'Loading', maxDots = 5):
        Toplevel.__init__(self, master)
        self.transient(master)
        self.grab_set()
        self.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        self.title('Load Dialog')
        self.message = message
        self.maxDots = maxDots
        self.label = Label(self, text = message, width = 20)
        self.label.pack()
        self.protocol('WM_DELETE_WINDOW', self.dontClose)
        self.isClose = False
        threading.Thread(target = self.update).start()

    def setCloseEvent(self, target, args = ()):
        threading.Thread(target = self.__task, args = (target, args)).start()

    def __task(self, target, args):
        target(*args)
        self.close()

    def dontClose(self):
        pass

    def update(self):
        dots = 0
        while not self.isClose:
            dots = (dots + 1) % self.maxDots
            time.sleep(0.5)
            self.label['text'] = self.message + dots * '.'
        self.destroy()

    def close(self):
        self.isClose = True