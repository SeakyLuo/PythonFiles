from tkinter import *

class Generator(Frame):
    def __init__(self, master):
        ## init variables
        Frame.__init__(self, master)
        self.entries = {}

        ## Generate Widgets
        self.rowLabel = Label(self, text = 'Rows:')
        self.rowEntry = Entry(self)
        self.colLabel = Label(self, text = 'Columns:')
        self.colEntry = Entry(self)
        self.rowEntry.focus()
        for entry in [self.rowEntry, self.colEntry]:
            var = StringVar(self)
            # var.trace('w', lambda *args: self.generateEntries(self.getRow(), self.getCol()))
            var.trace('w', lambda *args: print("Debug1"))
            entry['textvariable'] = var

        ## Place Widgets
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)

    def getRow(self):
        try: return int(self.rowEntry.get())
        except ValueError: return 0

    def getCol(self):
        try: return int(self.colEntry.get())
        except ValueError: return 0

    def generateEntries(self, row, col):
        if not row or not col:
            return
        for i in range(row):
            for j in range(col):
                if (i, j) in self.entries:
                    continue
                var = StringVar(self)
                var.trace('w', lambda *args: print('Debug2'))
                entry = Entry(self, textvariable = var)
                entry.grid(row = 1 + i, column = j, sticky = NSEW)
                self.entries[(i, j)] = entry
        for i, j in self.entries.copy():
            if i not in range(row) or j not in range(col):
                self.entries[(i, j)].grid_forget()
                del self.entries[(i, j)]

root = Tk()
app = Generator(root)
app.pack()
root.title('Matrix Generator')
root.mainloop()
