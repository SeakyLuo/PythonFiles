from tkinter import *
from tkinter import filedialog
import ez
import os

LAST_DIR = 'LastDirectory'

class Exporter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.settings = ez.Settings(__file__)
        self.exportButton = Button(self, text = 'Export', command = self.export)
        self.exportButton.grid(row = 0, column = 0, sticky = NSEW)
        self.copyButton = Button(self, text = 'Copy Path', command = lambda: ez.copyToClipboard(self.settings[LAST_DIR]))
        self.copyButton.grid(row = 0, column = 1, sticky = NSEW)
        self.lastDirLabel = Label(self)
        self.setLastDirLabel(self.settings.setdefault(LAST_DIR, '/'))
        self.lastDirLabel.grid(row = 1, column = 0, sticky = NSEW, columnspan = 2)
        self.export()

    def setLastDirLabel(self, text):
        self.lastDirLabel['text'] = 'Last Used Directory:\n' + text

    def export(self):
        file = filedialog.askopenfile(initialdir = self.settings[LAST_DIR], \
                                      title = 'Select a Python File', \
                                      filetypes = [('Python files','*.py')])
        if file == None:
            return
        filename = file.name
        path = os.path.dirname(filename)
        self.settings[LAST_DIR] = path
        self.setLastDirLabel(path)
        ez.exportpy(filename)

root = Tk()
root.title('Py Exporter')
app = Exporter(root)
app.pack()
root.mainloop()