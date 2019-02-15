from tkinter import *
from eztk import setEntry
import os
import ez

PATH_OPTION = 'PathOption'
PATH_OPTIONS = ['\\\\', '/']
AUTO_COPY = 'AutoCopy'

class Converter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.settings = ez.Settings(__file__)

        self.autoCopyVar = BooleanVar(self, value = self.settings.setdefault(AUTO_COPY, True))
        self.autoCopy = Checkbutton(self, text = AUTO_COPY, variable = self.autoCopyVar, \
                                          command = lambda: self.settings.setdefault(AUTO_COPY, self.autoCopyVar.get()))
        self.autoCopy.grid(row = 0, column = 0)
        self.pathOptionVar = StringVar(self)
        for i, option in enumerate(PATH_OPTIONS):
            Radiobutton(self, text = option, variable = self.pathOptionVar, value = option, \
                              command = self.onRadioChange).grid(row = 0, column = i + 1)
        self.pathOptionVar.set(self.settings.setdefault(PATH_OPTION, PATH_OPTIONS[0]))
        self.inputLabel = Label(self, text = 'Input:')
        self.outputLabel = Label(self, text = 'Output:')
        self.inputVar = StringVar(self)
        self.inputEntry = Entry(self, textvariable = self.inputVar)
        self.outputVar = StringVar(self)
        self.outputEntry = Entry(self, textvariable = self.outputVar)
        for i, (label, entry, var) in enumerate(zip([self.inputLabel, self.outputLabel], [self.inputEntry, self.outputEntry], [self.inputVar, self.outputVar])):
            label.grid(row = i + 1, column = 0)
            entry.grid(row = i + 1, column = 1, columnspan = 2)
            var.trace('w', lambda *args: self.onChange())
        self.inputEntry.focus()

    def onRadioChange(self):
        self.settings[PATH_OPTION] = self.pathOptionVar.get()
        self.onChange()

    def onChange(self):
        text = self.inputEntry.get().replace('\\', self.settings[PATH_OPTION])
        if not text:
            return
        setEntry(self.outputEntry, text)
        if self.settings[AUTO_COPY]:
            ez.copyToClipboard(text)

root = Tk()
app = Converter(root)
app.pack()
root.title('Path Converter')
ez.py2pyw(__file__)
root.mainloop()
