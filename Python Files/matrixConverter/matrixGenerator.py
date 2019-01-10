from tkinter import *
from tkinter import messagebox
import ez, ezs, eztk, os, atexit

MATRIX = 'Matrix'
DETERMINANT = 'Determinant'
VECTOR = 'Vector'
LATEX = 'LaTeX'
WOLFRAM = 'Wolfram'
LEFT = 'Left'
RIGHT = 'Right'
UP = 'Up'
DOWN = 'Down'

class Converter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        ## generate widgets
        self.settingsFileName = 'settings.json'
        self.settings = ez.fread(self.settingsFileName) if os.path.exists(self.settingsFileName) else {}
        self.resultTypeOptions = [MATRIX, DETERMINANT, VECTOR]
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
        self.rowEntry.bind('<KeyRelease>', self.onRowColChange)
        self.rowEntry.focus()
        self.colLabel = Label(self, text = 'Columns: ')
        self.colEntry = Entry(self)
        self.colEntry.bind('<KeyRelease>', self.onRowColChange)

        ## place widgets
        for i, w in enumerate([self.resultTypeDropdown, self.resultFormatDropdown, self.generateButton, self.showDialogButton, self.clearButton]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)

        ## init variables
        self.minRows = self.maxRows = 2
        self.minCols = self.maxCols = 4
        self.maxSize = 20
        self.setResultType(self.settings.get(self.RESULT_TYPE, MATRIX))
        self.setResultFormat(self.settings.get(self.RESULT_FORMAT, LATEX))
        self.switchButtonState(self.showDialogButton, self.settings.get(self.SHOW_DIALOG, True))
        self.entries = {}
        atexit.register(self.saveSettings)

    def saveSettings(self):
        ez.fwrite(self.settingsFileName, self.settings)

    def setResultType(self, resultType):
        self.resultType.set(resultType)
        self.onResultTypeChange()

    def onResultTypeChange(self):
        resultType = self.resultType.get()
        self.settings[self.RESULT_TYPE] = resultType
        row = self.getRow()
        col = self.getCol()
        if resultType == VECTOR:
            eztk.setEntry(self.colEntry, 1)
            self.colEntry['state'] = DISABLED
            if row:
                self.generateEntries(row, 1)
        elif resultType == DETERMINANT:
            self.colEntry['state'] = NORMAL
            if row != col:
                if row > col:
                    eztk.setEntry(self.colEntry, str(row))
                else:
                    eztk.setEntry(self.rowEntry, str(col))
                row = col = max(row, col)
                self.generateEntries(row, col)
        elif resultType == MATRIX:
            self.colEntry['state'] = NORMAL

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
        if self.moveFocus(event):
            return
        text = event.widget.get()
        if text == '':
            return
        if not text.isnumeric():
            text = text[:-1]
            eztk.setEntry(event.widget, text)
        elif eval(text) > self.maxSize:
            text = str(self.maxSize)
            eztk.setEntry(event.widget, self.maxSize)
        if self.resultType.get() == DETERMINANT:
            if event.widget == self.rowEntry:
                eztk.setEntry(self.colEntry, text)
            else:
                eztk.setEntry(self.rowEntry, text)
        r = self.getRow()
        c = self.getCol()
        self.maxRows = r + self.minRows
        self.maxCols = max(c, self.maxCols)
        self.generateEntries(r, c)

    def generateEntries(self, row, column):
        for i in range(row):
            for j in range(column):
                if (i, j) in self.entries:
                    continue
                e = Entry(self)
                e.bind('<KeyRelease>', self.moveFocus)
                e.bind('<Return>', lambda event: self.generate())
                e.grid(row = i + self.minRows, column = j, sticky = NSEW)
                self.entries[(i, j)] = e
        for i, j in self.entries.copy():
            if i not in range(row) or j not in range(column):
                self.entries[(i, j)].grid_forget()
                del self.entries[(i, j)]

    def moveFocus(self, event):
        key = event.keysym
        move = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
        if type(event.widget) != Entry or key not in move or (key == LEFT and event.widget.index(INSERT) > 0) or (key == RIGHT and event.widget.index(INSERT) == len(event.widget.get()) - 1):
            return False
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
            if (type(w) == Entry):
                w.focus()
                break
        return True

    def findByGrid(self, row, column):
        for child in self.children.values():
            info = child.grid_info()
            if info and info['row'] == row and info['column'] == column:
                return child
        return None

    def isOn(self, switchButton):
        return switchButton['relief'] == GROOVE

    def switchButtonState(self, switchButton, on = None):
        switchButton['relief'] = FLAT if self.isOn(switchButton) else GROOVE \
                                 if on == None else \
                                 GROOVE if on else FLAT
        # if on == None:
        #     switchButton['relief'] = FLAT if self.isOn(switchButton) else GROOVE
        # else:
        #     switchButton['relief'] = GROOVE if on else FLAT

    def showDialog(self):
        self.switchButtonState(self.showDialogButton)
        self.settings[self.SHOW_DIALOG] = self.isOn(self.showDialogButton)

    def clear(self):
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
        if self.resultFormat.get() == LATEX:
            text = ezs.ml(r, c, ' '.join(self.entries[(i, j)].get() for i in range(r) for j in range(c)), False)
        elif self.resultFormat.get() == WOLFRAM:
            text = ezs.mw(r, c, ' '.join(self.entries[(i, j)].get() for i in range(r) for j in range(c)), False)
        ez.copyToClipboard(text)
        if self.settings[self.SHOW_DIALOG]:
            messagebox.showinfo(title = "Result", message = text + "\nis Copied to the Clipboard!")

root=Tk()
gui=Converter(root)
gui.pack()
root.title('Generator')
root.mainloop()

ez.py2pyw('matrixGenerator.py')
