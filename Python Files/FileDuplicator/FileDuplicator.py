from tkinter import *
from tkinter import filedialog, messagebox
import ez, os
from eztk import setEntryHint

DIRECTORY = 'Directory'
PATTERN = 'Pattern'
NUMBER = 'NumbersOnly'

class Duplicator(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.settings = ez.Settings(__file__)
        self.frames = [Frame(self) for _ in range(3)]
        self.selectButton = Button(self.frames[0], text = 'Select File', command = self.select)
        self.dupButton = Button(self.frames[0], text = 'Duplicate', command = self.duplicate)
        self.fileLabel = Label(self.frames[1], text = 'File: ')
        self.filenameLabel = Label(self.frames[1])
        self.copiesLabel = Label(self.frames[1], text = 'Copies: ')
        self.copiesEntry = Entry(self.frames[1])
        self.copiesEntry.focus()
        self.patternLabel = Label(self.frames[1], text = 'Pattern: ')
        self.patternEntry = Entry(self.frames[1], text = self.settings.setdefault(PATTERN, ''), width = 40)
        self.patternHint = 'Example: " (?)" -> "filename (1)"'
        setEntryHint(self.patternEntry, self.patternHint)
        self.numbersOnlyLabel = Label(self.frames[1], text = 'Numbers Only: ')
        self.numbersOnlyVar = BooleanVar(self, value = self.settings.setdefault(NUMBER, False))
        self.numbersOnlyButton = Checkbutton(self.frames[1], variable = self.numbersOnlyVar, \
                                            command = lambda: self.settings.set(NUMBER, self.numbersOnlyVar.get()))
        self.startLabel = Label(self.frames[1], text = 'Start Number: ')
        self.startEntry = Entry(self.frames[1], textvariable = IntVar(self, value = 1))
        for i, w in enumerate(self.frames):
            w.grid(row = i, column = 0, sticky = NSEW)
        for i, w in enumerate([self.selectButton, self.dupButton]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, widgets in enumerate(zip([self.fileLabel, self.filenameLabel],
                                        [self.copiesLabel, self.copiesEntry],
                                        [self.patternLabel, self.patternEntry],
                                        [self.numbersOnlyLabel, self.numbersOnlyButton],
                                        [self.startLabel, self.startEntry])):
            for j, w in enumerate(widgets):
                w.grid(row = j, column = i, sticky = NSEW if j else None)
        self.entries = [self.copiesEntry, self.patternEntry, self.startEntry]
        for e in self.entries:
            e.bind('<Up>', self.switch)
            e.bind('<Down>', self.switch)

    def select(self):
        filename = filedialog.askopenfilename(initialdir = self.settings.setdefault(DIRECTORY, ''), \
                                              title = 'Select a File')
        if not filename: return
        self.settings[DIRECTORY] = os.path.dirname(filename)
        self.filenameLabel['text'] = filename

    def duplicate(self):
        filename = self.filenameLabel['text']
        if not filename:
            messagebox.showerror(title = 'Error', message = 'No File Selected')
            return
        copies = self.copiesEntry.get()
        if not copies.isnumeric():
            messagebox.showerror(title = 'Error', message = 'Please Input Numerical Value for Copies!')
            return
        copies = int(copies)
        pattern = self.patternEntry.get().strip()
        if pattern == self.patternHint or pattern == '':
            pattern = ''
        elif '?' not in pattern:
            messagebox.showerror(title = 'Error', message = 'No "?" Found in Pattern!')
            return
        self.settings[PATTERN] = pattern
        numbersOnly = self.numbersOnlyVar.get()
        start = int(self.startEntry.get())
        ez.dupFile(filename, copies, pattern, numbersOnly, start)
        messagebox.showinfo(title = 'Finished', message = 'Done!')

    def switch(self, event):
        self.entries[(self.entries.index(self.master.focus_get()) + (-1) ** (event.keysym == 'Up')) % len(self.entries)].focus()

root = Tk()
app = Duplicator(root)
app.pack()
root.title('File Duplicator')
ez.py2pyw(__file__)
root.mainloop()
