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
        self.revertButton = Button(self.frames[0], text = 'Revert', command = self.revert)
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
        for i, w in enumerate([self.selectButton, self.convertButton, self.revertButton]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, (w1, w2) in enumerate(zip([self.fileLabel, self.filenameLabel],
                                         [self.toLabel, self.toEntry])):
            w1.grid(row = 0, column = i)
            w2.grid(row = 1, column = i, sticky = NSEW)
        self.lastConversion = ()

    def select(self):
        filename = filedialog.askopenfilename(initialdir = self.settings.setdefault(LAST_DIR, ''), \
                                              title = 'Select a File')
        if not filename: return
        self.settings[LAST_DIR] = os.path.dirname(filename)
        self.filenameLabel['text'] = filename
        self.lastConversion = ()

    def convert(self):
        filename = self.filenameLabel['text']
        fileFormat = self.toEntry.get()
        if fileFormat.startswith('.'):
            fileFormat = fileFormat[1:]
        if not filename or not fileFormat:
            messagebox.showerror(title = 'Error', message = 'Nothing to Convert!')
            return
        self.settings[LAST_FORMAT] = fileFormat
        dot = filename.find('.')
        newFileName = filename + '.' + fileFormat if dot == -1 else filename[:dot + 1] + fileFormat
        self.__rename(filename, newFileName, 'Renaming Done!')

    def revert(self):
        if not self.lastConversion:
            messagebox.showerror(title = 'Error', message = 'Nothing to Revert!')
            return
        fromFile, toFile = self.lastConversion
        self.__rename(toFile, fromFile, 'Reversion Done!')

    def __rename(self, fromFile, toFile, doneMessage):
        try:
            os.rename(fromFile, toFile)
        except:
            messagebox.showerror(title = 'Error', message = 'File not found!')
            return False
        self.filenameLabel['text'] = toFile
        self.lastConversion = (fromFile, toFile)
        messagebox.showinfo(title = 'Finished', message = doneMessage)
        return True

root = Tk()
app = Converter(root)
app.pack()
root.title('File Converter')
ez.py2pyw(__file__)
root.mainloop()
