from tkinter import *
from tkinter import filedialog
import ez
import os

LAST_DIR = 'LastDirectory'
WITH_CONSOLE = 'WithConsole'
ZIP_FILE = 'ZipFile'

class Exporter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.settings = ez.Settings(__file__)
        self.exportButton = Button(self, text = 'Export', command = self.export)
        self.copyButton = Button(self, text = 'Copy Path', command = lambda: ez.copyToClipboard(self.settings[LAST_DIR]))
        self.consoleVar = BooleanVar(self, value = self.settings.setdefault(WITH_CONSOLE, True))
        self.consoleButton = Checkbutton(self, text = 'With Console', variable = self.consoleVar, \
                                               command = lambda: self.settings.setitem(WITH_CONSOLE, self.consoleVar.get()))
        self.zipVar = BooleanVar(self, value = self.settings.setdefault(ZIP_FILE, True))
        self.zipButton = Checkbutton(self, text = 'Zip File', variable = self.zipVar, \
                                           command = lambda: self.settings.setitem(ZIP_FILE, self.zipVar.get()))
        row0 = [self.exportButton, self.copyButton, self.consoleButton, self.zipButton]
        for i, w in enumerate(row0):
            w.grid(row = 0, column = i, sticky = NSEW)
        self.lastDirLabel = Label(self)
        self.setLastDirLabel(self.settings.setdefault(LAST_DIR, '/'))
        self.lastDirLabel.grid(row = 1, column = 0, sticky = NSEW, columnspan = len(row0))

    def setLastDirLabel(self, text):
        self.lastDirLabel['text'] = 'Last Used Directory:\n' + text

    def export(self):
        filename = filedialog.askopenfilename(initialdir = self.settings[LAST_DIR], \
                                              title = 'Select a Python File', \
                                              filetypes = [('Python files','*.py')])
        if not filename:
            return
        path = os.path.dirname(filename)
        self.settings[LAST_DIR] = path
        self.setLastDirLabel(path)
        ez.exportpy(filename, self.settings[WITH_CONSOLE], self.settings[ZIP_FILE])

root = Tk()
root.title('Py Exporter')
app = Exporter(root)
app.pack()
root.mainloop()
