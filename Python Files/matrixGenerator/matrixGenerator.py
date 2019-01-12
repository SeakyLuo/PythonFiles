from tkinter import *
from tkinter import messagebox
from json import dumps, loads
from atexit import register
import ez, ezs, eztk, os

MATRIX = 'Matrix'
DETERMINANT = 'Determinant'
VECTOR = 'Vector'
IDENTITY_MATRIX = 'Identity Matrix'
LATEX = 'LaTeX'
WOLFRAM = 'Wolfram'
LEFT = 'Left'
RIGHT = 'Right'
UP = 'Up'
DOWN = 'Down'

class Generator(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        ## init variables
        self.minRows = self.maxRows = 2
        self.minCols = self.maxCols = 4
        self.maxSize = 20
        self.entries = {}
        
        ## generate widgets
        self.settingsFileName = 'settings.json'
        self.settings = loads(ez.fread(self.settingsFileName)) if os.path.exists(self.settingsFileName) else {}
        self.resultTypeOptions = [MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX]
        self.RESULT_TYPE = 'ResultType'
        self.resultType = StringVar(self)
        self.resultTypeDropdown = OptionMenu(self, self.resultType, *self.resultTypeOptions, command = lambda event: self.onResultTypeChange())
        self.resultFormatOptions = [LATEX, WOLFRAM]
        self.RESULT_FORMAT = "ResultFormat"
        self.resultFormat = StringVar(self)
        self.resultFormatDropdown = OptionMenu(self, self.resultFormat, *self.resultFormatOptions, command = lambda event: self.onResultFormatChange())
        self.generateButton = Button(self, text = 'Generate', command = self.generate)
        self.showDialogButton = Button(self, text = 'ShowDialog', command = self.showDialog)
        self.SHOW_DIALOG = "ShowDialog"
        self.clearButton = Button(self, text = 'Clear', command = self.clear)
        
        self.rowLabel = Label(self, text = 'Rows: ')
        self.rowEntry = Entry(self)
        self.rowEntry.focus()
        self.colLabel = Label(self, text = 'Columns: ')
        self.colEntry = Entry(self)
        for entry in [self.rowEntry, self.colEntry]:
            entry.bind('<KeyPress>', self.moveFocus)
            entry.bind('<KeyRelease>', self.onRowColChange)

        ## place widgets
        for i, w in enumerate([self.resultTypeDropdown, self.resultFormatDropdown, self.generateButton, self.showDialogButton, self.clearButton]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)

        ## set values
        self.setResultType(self.settings.get(self.RESULT_TYPE, MATRIX))
        self.setResultFormat(self.settings.get(self.RESULT_FORMAT, LATEX))
        self.switchButtonState(self.showDialogButton, self.settings.get(self.SHOW_DIALOG, True))

        register(self.saveSettings)

    def saveSettings(self):
        ez.fwrite(self.settingsFileName, dumps(self.settings))

    def setResultType(self, resultType):
        self.resultType.set(resultType)
        self.onResultTypeChange()

    def onResultTypeChange(self):
        resultType = self.resultType.get()
        self.settings[self.RESULT_TYPE] = resultType
        row = self.getRow()
        col = self.getCol()
        if resultType == MATRIX:
            self.colEntry['state'] = NORMAL
        elif resultType == DETERMINANT:
            self.colEntry['state'] = NORMAL
            size = max(row, col)
            if size:                
                row = col = size
                self.syncRowCol(size)
        elif resultType == VECTOR:
            eztk.setEntry(self.colEntry, 1)
            self.colEntry['state'] = DISABLED
            if row:
                self.generateEntries(row, 1)
        elif resultType == IDENTITY_MATRIX:
            self.colEntry['state'] = NORMAL
            size = max(row, col)
            if size:                
                row = col = size
                self.syncRowCol(size)
                self.fillIdentityMatrix()

    def setResultFormat(self, resultFormat):
        self.resultFormat.set(resultFormat)
        self.onResultFormatChange()

    def onResultFormatChange(self):
        self.settings[self.RESULT_FORMAT] = self.resultFormat.get()

    def getRow(self):
        return int(self.rowEntry.get() or 0)

    def getCol(self):
        return int(self.colEntry.get() or 0)

    def onRowColChange(self, event):
        text = event.widget.get()
        if not text:
            return
        if not text.isnumeric():
            text = text[:-1]
            eztk.setEntry(event.widget, text)
        elif eval(text) > self.maxSize:
            text = str(self.maxSize)
            eztk.setEntry(event.widget, text)
        resultType = self.resultType.get()
        r = self.getRow()
        c = self.getCol()
        if resultType in [DETERMINANT, IDENTITY_MATRIX]:
            size = r if text == str(r) else c
            r = c = size
            self.syncRowCol(size)
        self.maxRows = r + self.minRows
        self.maxCols = max(c, self.maxCols)
        self.generateEntries(r, c)
        if resultType == IDENTITY_MATRIX:
            self.fillIdentityMatrix()

    def generateEntries(self, row, column):
        for i in range(row):
            for j in range(column):
                if (i, j) in self.entries:
                    continue
                e = Entry(self)
                e.bind('<KeyRelease>', self.onEntryChange)
                e.bind('<KeyPress>', self.moveFocus)
                e.bind('<Return>', lambda event: self.generate())
                e.grid(row = i + self.minRows, column = j, sticky = NSEW)
                self.entries[(i, j)] = e
        for i, j in self.entries.copy():
            if i not in range(row) or j not in range(column):
                self.entries[(i, j)].grid_forget()
                del self.entries[(i, j)]

    def onEntryChange(self, event):
        resultType = self.resultType.get()
        if resultType == IDENTITY_MATRIX:
            for r, c in self.entries:
                entry = self.entries[(r, c)]
                text = entry.get()
                if text and (r == c and text != '1') or (r != c and text != '0'):
                    self.setResultType(MATRIX)
                    break

    def moveFocus(self, event):
        key = event.keysym
        move = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
        if type(event.widget) != Entry or key not in move or (key == LEFT and event.widget.index(INSERT) > 0) or (key == RIGHT and event.widget.index(INSERT) == len(event.widget.get()) - 1):
            return
        x, y = move[key]
        info = event.widget.grid_info()
        r = info['row']
        c = info['column']
        while True:
            r += x
            c += y
            if r == self.maxRows:
                r = 0
                if self.entries:
                    c = (c + 1) % self.maxCols
            elif r == -1:
                r = self.maxRows - 1
                if self.entries:
                    c = (c - 1) % self.maxCols
            elif c == self.maxCols:
                c = 0
            elif c == -1:
                c = self.maxCols - 1
            w = self.findByGrid(r, c)
            if type(w) == Entry:
                w.focus()
                break

    def findByGrid(self, row, column):
        for child in self.children.values():
            info = child.grid_info()
            if info and info['row'] == row and info['column'] == column:
                return child
        return None

    def syncRowCol(self, size):
        eztk.setEntry(self.rowEntry, size)
        eztk.setEntry(self.colEntry, size)
        self.generateEntries(size, size)

    def fillIdentityMatrix(self):
        for i, j in self.entries:
            eztk.setEntry(self.entries[(i, j)], 1 if i == j else 0)

    def isOn(self, switchButton):
        return switchButton['relief'] == GROOVE

    def switchButtonState(self, switchButton, on = None):
        switchButton['relief'] = FLAT if self.isOn(switchButton) else GROOVE \
                                 if on == None else \
                                 GROOVE if on else FLAT

    def showDialog(self):
        self.switchButtonState(self.showDialogButton)
        self.settings[self.SHOW_DIALOG] = self.isOn(self.showDialogButton)

    def clear(self): 
        if self.resultType.get() != IDENTITY_MATRIX:
            for entry in self.entries.values():
                eztk.clearEntry(entry)
        
    def generate(self):
        for entry in self.entries.values():
            if not entry.get():
                messagebox.showerror(title = "Error!", message = "Not All Entries are Filled")
                return
        text = ''
        r = self.getRow()
        c = self.getCol()
        # resultType = self.resultType.get()
        resultFormat = self.resultFormat.get()
        if resultFormat == LATEX:
            text = ezs.ml(r, c, ' '.join(self.entries[(i, j)].get() for i in range(r) for j in range(c)), False)
        elif resultFormat == WOLFRAM:
            text = ezs.mw(r, c, ' '.join(self.entries[(i, j)].get() for i in range(r) for j in range(c)), False)
        ez.copyToClipboard(text)
        if self.settings[self.SHOW_DIALOG]:
            messagebox.showinfo(title = "Result", message = text + "\nis Copied to the Clipboard!")

root = Tk()
gui = Generator(root)
gui.pack()
root.title('Generator')
root.mainloop()

ez.py2pyw(__file__)
