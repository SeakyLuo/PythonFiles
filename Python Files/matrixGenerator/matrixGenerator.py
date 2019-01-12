from tkinter import *
from tkinter import messagebox
from json import dumps, loads
from atexit import register
from eztk import setEntry, clearEntry
from random import randrange
import ez, ezs, eztk, os

MATRIX = 'Matrix'
DETERMINANT = 'Determinant'
VECTOR = 'Vector'
IDENTITY_MATRIX = 'Identity Matrix'
resultTypeOptions = [MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX]
LATEX = 'LaTeX'
WOLFRAM = 'Wolfram'
resultFormatOptions = [LATEX, WOLFRAM]
LEFT = 'Left'
RIGHT = 'Right'
UP = 'Up'
DOWN = 'Down'

class Generator(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        ## init variables
        self.master = master
        self.minRows = self.maxRows = 2
        self.minCols = self.maxCols = 4
        self.maxSize = 15
        self.entries = {}
        self.settingsFileName = 'settings.json'
        self.settings = loads(ez.fread(self.settingsFileName)) if os.path.exists(self.settingsFileName) else {}

        ## generate menu        
        self.menu = Menu(self)
        self.editMenu = Menu(self.menu, tearoff = 0)
        self.editMenu.add_command(label = 'Random', command = self.randomFill)
        self.editMenu.add_command(label = 'Unit Matrix', command = self.unitMatrix)
        self.editMenu.add_command(label = 'Generate', command = self.generate)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = 'Clear Size', command = lambda: self.clear(0))
        self.editMenu.add_command(label = 'Clear Entries', command = lambda: self.clear(1))
        self.editMenu.add_command(label = 'Clear All', command = lambda: self.clear(0, 1))
        self.matMenu = Menu(self.menu, tearoff = 0)
        self.matMenu.add_command(label = 'Transpose', command = self.transpose)
        self.matMenu.add_command(label = 'Lower Triangular', command = self.lowerTriangular)
        self.matMenu.add_command(label = 'Upper Triangular', command = self.upperTriangular)
        self.detMenu = Menu(self.menu, tearoff = 0)
        self.detMenu.add_command(label = 'Transpose', command = self.transpose)
        self.vecMenu = Menu(self.menu, tearoff = 0)
        self.vecMenu.add_command(label = 'Transpose', command = self.transpose)
        self.imatMenu = Menu(self.menu, tearoff = 0)
        self.imatMenu.add_command(label = 'Permutation Matrix', command = self.permutationMatrix)
        self.settingsMenu = Menu(self.menu, tearoff = 0)
        self.SHOW_DIALOG = 'ShowDialog'
        self.showDialogVar = BooleanVar(self, value = self.settings.get(self.SHOW_DIALOG, True))
        self.settingsMenu.add_checkbutton(label = 'Show Dialog', onvalue = 1, offvalue = 0, variable = self.showDialogVar, command = self.showDialog)
        for name, menu in zip(['Edit'] + resultTypeOptions + ['Settings'], [self.editMenu, self.matMenu, self.detMenu, self.vecMenu, self.imatMenu, self.settingsMenu]):            
            self.menu.add_cascade(label = name, menu = menu)
        
        ## generate widgets
        self.master.config(menu = self.menu)
        self.RESULT_TYPE = 'ResultType'
        self.resultType = StringVar(self)
        self.resultTypeDropdown = OptionMenu(self, self.resultType, *resultTypeOptions, command = lambda event: self.onResultTypeChange())
        self.RESULT_FORMAT = "ResultFormat"
        self.resultFormat = StringVar(self)
        self.resultFormatDropdown = OptionMenu(self, self.resultFormat, *resultFormatOptions, command = lambda event: self.onResultFormatChange())
        
        self.rowLabel = Label(self, text = 'Rows: ')
        self.rowEntry = Entry(self)
        self.rowEntry.focus()
        self.colLabel = Label(self, text = 'Columns: ')
        self.colEntry = Entry(self)
        for entry in [self.rowEntry, self.colEntry]:
            entry.bind('<KeyPress>', self.moveFocus)
            entry.bind('<KeyRelease>', self.onRowColChange)

        ## place widgets
        for i, w in enumerate([self.resultTypeDropdown, self.resultFormatDropdown]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)

        ## set values
        self.setResultType(self.settings.get(self.RESULT_TYPE, MATRIX))
        self.setResultFormat(self.settings.get(self.RESULT_FORMAT, LATEX))
        register(self.saveSettings)

    def saveSettings(self):
        ez.fwrite(self.settingsFileName, dumps(self.settings))

    def getRow(self):
        return int(self.rowEntry.get() or 0)

    def getCol(self):
        return int(self.colEntry.get() or 0)

    def setRow(self, num):
        setEntry(self.rowEntry, num)

    def setCol(self, num):
        setEntry(self.colEntry, num)

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
            self.setCol(1)
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

    def onRowColChange(self, event):
        text = event.widget.get()
        if not text:
            return
        if not text.isnumeric():
            text = text[:-1]
            setEntry(event.widget, text)
        elif eval(text) > self.maxSize:
            text = str(self.maxSize)
            setEntry(event.widget, text)
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
        self.setRow(size)
        self.setCol(size)
        self.generateEntries(size, size)

    def fillIdentityMatrix(self):
        for i, j in self.entries:
            setEntry(self.entries[(i, j)], 1 if i == j else 0)

    def transpose(self):
        resultType = self.resultType.get()
        if resultType not in [MATRIX, DETERMINANT, VECTOR]:
            return
        row = self.getRow()
        col = self.getCol()
        entries = { key: self.entries[key].get() for key in self.entries }
        if row != col:            
            if resultType == VECTOR:
                self.setResultType(MATRIX)
            self.generateEntries(col, row)
            self.setRow(col)
            self.setCol(row)
        for i in range(row):
            for j in range(col):
                setEntry(self.entries[(j, i)], entries[(i, j)])

    def randomFill(self):
        resultType = self.resultType.get()
        ## Use ezs random matrix instead
        row = self.getRow()
        col = self.getCol()
        isIdentity = resultType == IDENTITY_MATRIX
        if not row or not col or isIdentity:
            if resultType == MATRIX:
                if not row:
                    row = randrange(self.maxSize)
                if not col:
                    col = randrange(self.maxSize)
            elif resultType == DETERMINANT:
                row = col = randrange(self.maxSize)
            elif resultType == VECTOR:
                row = randrange(self.maxSize)
            elif resultType == IDENTITY_MATRIX:
                row = col = randrange(self.maxSize)
            self.setRow(row)
            self.setCol(col)
            self.generateEntries(row, col)
        if isIdentity:
            self.fillIdentityMatrix()
        else:
            for entry in self.entries.values():
                setEntry(entry, randrange(1, 10))

    def lowerTriangular(self):
        isIdentity = self.resultType.get() == IDENTITY_MATRIX
        for i, j in self.entries:
            if i < j:
                setEntry(self.entries[(i ,j)], 0)
            elif isIdentity:
                setEntry(self.entries[(i ,j)], 1)
        if isIdentity:
            self.setResultType(MATRIX)

    def upperTriangular(self):
        isIdentity = self.resultType.get() == IDENTITY_MATRIX
        for i, j in self.entries:
            if i > j:
                setEntry(self.entries[(i ,j)], 0)
            elif isIdentity:
                setEntry(self.entries[(i ,j)], 1)
        if isIdentity:
            self.setResultType(MATRIX)

    def unitMatrix(self):
        if self.resultType.get() == IDENTITY_MATRIX:
            self.fillIdentityMatrix()
        else:
            for entry in self.entries.values():
                setEntry(entry, 1)

    def permutationMatrix(self):
        row = self.getRow()
        col = self.getCol()
        if not row:
            row = col = randrange(self.maxSize)
            self.setRow(row)
            self.setCol(col)
            self.generateEntries(row, col)
            self.fillIdentityMatrix()
        self.setResultType(MATRIX)
        cols = list(range(col))
        for i in range(row):
            j = cols.pop(randrange(len(cols)))
            setEntry(self.entries[(i, i)], 0)
            setEntry(self.entries[(i, j)], 1)

    def showDialog(self):
        self.settings[self.SHOW_DIALOG] = self.showDialogVar.get()
        
    def clear(self, *mode):
        if 0 in mode:
            clearEntry(self.rowEntry)
            clearEntry(self.colEntry)
            for key, entry in self.entries.copy().items():
                entry.grid_forget()
                del self.entries[key]
        if 1 in mode and self.resultType.get() != IDENTITY_MATRIX:
            for entry in self.entries.values():
                clearEntry(entry)
        
    def generate(self):
        for entry in list(self.entries.values()) + [self.rowEntry, self.colEntry]:
            if not entry.get():
                messagebox.showerror(title = "Error", message = "Not All Entries are Filled")
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
