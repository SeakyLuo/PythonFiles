from tkinter import *
from tkinter import filedialog, messagebox
import ez, os
from eztk import setEntry

LAST_DIR = 'LastDirectory'
LAST_FORMAT = 'LastFormat'

class Converter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.settings = ez.Settings(__file__)
        self.frames = [Frame(self) for _ in range(3)]
        self.selectButton = Button(self.frames[0], text = 'Select File', command = self.select)
        self.convertButton = Button(self.frames[0], text = 'Convert', command = self.convert)
        self.fileLabel = Label(self.frames[1], text = 'File: ')
        self.filenameLabel = Label(self.frames[1])
        self.toLabel = Label(self.frames[1], text = 'Format: ')
        self.toEntry = Entry(self.frames[1])
        self.toEntry.focus()
        entryText = self.settings.setdefault(LAST_FORMAT, '')
        if entryText:
            setEntry(self.toEntry, entryText)
            self.toEntry.select_range(0, END)
        for i, w in enumerate(self.frames):
            w.grid(row = i, column = 0, sticky = NSEW)
        for i, (w1, w2, w3) in enumerate(zip([self.selectButton, self.convertButton],
                                             [self.fileLabel, self.filenameLabel],
                                             [self.toLabel, self.toEntry])):
            w1.grid(row = 0, column = i, sticky = NSEW)
            w2.grid(row = 0, column = i)
            w3.grid(row = 1, column = i, sticky = NSEW)

    def select(self):
        filename = filedialog.askopenfilename(initialdir = self.settings.setdefault(LAST_DIR, ''), \
                                              title = 'Select a File')
        if not filename: return
        self.settings[LAST_DIR] = os.path.dirname(filename)
        self.filenameLabel['text'] = filename

    def convert(self):
        filename = self.filenameLabel['text']
        fileFormat = self.toEntry.get()
        if not filename or not fileFormat: return
        if fileFormat.startswith('.'):
            fileFormat = fileFormat[1:]
            if not fileFormat: return
        self.settings[LAST_FORMAT] = fileFormat
        os.rename(filename, filename[:filename.find('.') + 1] + fileFormat)
        messagebox.showinfo(title = 'Finished', message = 'Done!')

root = Tk()
app = Converter(root)
app.pack()
root.title('File Converter')
ez.py2pyw(__file__)
root.mainloop()
