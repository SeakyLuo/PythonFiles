from tkinter import *
from tkinter import messagebox, simpledialog
from json import dumps, loads
from atexit import register
from eztk import setEntry, clearEntry
from random import randrange
from numpy import linalg
from ez import fread, fwrite, copyToClipboard, py2pyw, find
import ezs, os

## Static Variables
maxSize = 15

MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX = 'Matrix', 'Determinant', 'Vector', 'Identity Matrix'
resultTypeOptions = [MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX]
LATEX, ARRAY = 'LaTeX', 'Array'
resultFormatOptions = [LATEX, ARRAY]
LEFT, RIGHT, UP, DOWN = 'Left', 'Right', 'Up', 'Down'
CLEAR_ENTRIES, CLEAR_ALL = 'Clear Entries', 'Clear All'
NONE = 'None'
clearOptions = [CLEAR_ENTRIES, CLEAR_ALL, NONE]
GENERATE_CLEAR_OPTION = 'GenerateClearOption'
CALCULATE_CLEAR_OPTION = 'CalculateClearOption'
COLUMN_VECTOR = 'ColumnVector'
REMEMBER_SIZE = 'RememberSize'
SHOW_DIALOG = 'ShowDialog'
RESULT_TYPE = 'ResultType'
RESULT_FORMAT = 'ResultFormat'
LAST_USED_DROPDOWN = 'LastUsedDropdown'
UNIT_MATRIX = 'Unit Matrix'
MULTIPLY = 'Multiply'
TRANSPOSE = 'Transpose'
RANDOM = 'Random'
GENERATE = 'Generate'
UNDO = 'Undo'
REDO = 'Redo'
settingsFile = 'settings.json'

## Shortcuts
shortcuts = { RANDOM: 'Ctrl+R', GENERATE: 'Enter/Return', UNDO: 'Ctrl+Z', REDO: 'Ctrl+Y', UNIT_MATRIX: 'Ctrl+U', \
              MULTIPLY: 'Ctrl+M', TRANSPOSE: 'Ctrl+T', CLEAR_ENTRIES: 'Ctrl+Shift+E', CLEAR_ALL: 'Ctrl+Shift+A' }
otherShortcutFormatter = lambda command, shortcut: '{:<25}{:<15}'.format(command, shortcut)
otherShortcuts = '\n'.join([otherShortcutFormatter('Switch Result Type', 'Ctrl+['), \
                            otherShortcutFormatter('Switch Result Type', 'Ctrl+]'), \
                            otherShortcutFormatter('Switch Result Format', 'Alt+['), \
                            otherShortcutFormatter('Switch Result Format', 'Alt+]')])

class Generator(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        ## init variables
        self.master = master
        self.minRows = self.maxRows = 2
        self.minCols = self.maxCols = 4
        self.entries = {}
        self.statePointer = 0
        self.states = [] ## (resultType, entries)

        ## Settings
        self.settings = loads(fread(settingsFile)) if os.path.exists(settingsFile) else {}

        ## Generate Menus
        self.menu = Menu(self)
        ## Result Menu
        self.resultMenu = Menu(self.menu)
        self.matMenu = Menu(self.menu)
        self.matMenu.add_command(label = 'Lower Triangular', command = lambda: self.triangularMatrix(0))
        self.matMenu.add_command(label = 'Upper Triangular', command = lambda: self.triangularMatrix(1))
        self.detMenu = Menu(self.menu)
        self.detMenu.add_command(label = 'Calculate', command = self.calculateDet)
        self.calculateClearVar = StringVar(self, value = self.settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.detMenu, self.calculateClearVar, \
                            lambda :self.settings.__setitem__(CALCULATE_CLEAR_OPTION, self.calculateClearVar.get()), \
                            'Clear After Calculation')
        self.vecMenu = Menu(self.menu)
        self.colVecVar = BooleanVar(self, value = self.settings.setdefault(COLUMN_VECTOR, True))
        self.vecMenu.add_checkbutton(label = 'Column Vector', variable = self.colVecVar, command = lambda :self.settings.__setitem__(COLUMN_VECTOR, self.colVecVar.get()))
        self.imatMenu = Menu(self.menu)
        self.imatMenu.add_command(label = 'Permutation Matrix', command = self.permutationMatrix)
        for name, menu in zip(resultTypeOptions, [self.matMenu, self.detMenu, self.vecMenu, self.imatMenu]):
            menu['tearoff'] = False
            self.resultMenu.add_cascade(label = name, menu = menu)
        ## Edit Menu
        self.editMenu = Menu(self.menu)
        self.editMenu.add_command(label = UNDO, accelerator = shortcuts[UNDO], command = self.undo)
        self.editMenu.add_command(label = REDO, accelerator = shortcuts[REDO], command = self.redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = MULTIPLY, accelerator = shortcuts[MULTIPLY], command = self.multiply)
        self.editMenu.add_command(label = TRANSPOSE, accelerator = shortcuts[TRANSPOSE], command = self.transpose)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = CLEAR_ENTRIES, accelerator = shortcuts[CLEAR_ENTRIES], command = lambda: self.clear(0))
        self.editMenu.add_command(label = CLEAR_ALL, accelerator = shortcuts[CLEAR_ALL], command = lambda: self.clear(1))
        ## Insert Menu
        self.insertMenu = Menu(self)
        self.insertMenu.add_command(label = RANDOM, accelerator = shortcuts[RANDOM], command = self.randomFill)
        self.insertMenu.add_command(label = UNIT_MATRIX, accelerator = shortcuts[UNIT_MATRIX], command = self.unitMatrix)
        self.insertMenu.add_command(label = 'From ' + LATEX, command = lambda: self.insert(LATEX))
        self.insertMenu.add_command(label = 'From ' + ARRAY, command = lambda: self.insert(ARRAY))
        ## Generate Menu
        self.generateMenu = Menu(self.menu)
        self.generateMenu.add_command(label = GENERATE, accelerator = shortcuts[GENERATE], command = self.generate)
        self.generateClearVar = StringVar(self, value = self.settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.generateMenu, self.generateClearVar, \
                            lambda :self.settings.__setitem__(GENERATE_CLEAR_OPTION, self.generateClearVar.get()), \
                            'Clear After Generation')
        ## Settings Menu
        self.settingsMenu = Menu(self.menu)
        self.rememberSizeVar = BooleanVar(self, value = self.settings.setdefault(REMEMBER_SIZE, (-1, -1)) != (-1, -1))
        self.settingsMenu.add_checkbutton(label = 'Remember Size', variable = self.rememberSizeVar, \
                                          command = lambda :self.settings.__setitem__(REMEMBER_SIZE, (self.getRow(), self.getCol()) if self.rememberSizeVar.get() else (0, 0) ))
        self.showDialogVar = BooleanVar(self, value = self.settings.setdefault(SHOW_DIALOG, True))
        self.settingsMenu.add_checkbutton(label = 'Show Dialog', variable = self.showDialogVar, \
                                          command = lambda :self.settings.__setitem__(SHOW_DIALOG, self.showDialogVar.get()))
        self.settingsMenu.add_separator()
        self.settingsMenu.add_command(label = 'Other Keyboard Shortcuts', command = lambda: messagebox.showinfo(title = 'Shortcuts', message = otherShortcuts))
        for name, menu in zip(['Result', 'Edit', 'Insert', 'Generate', 'Settings'], [self.resultMenu, self.editMenu, self.insertMenu, self.generateMenu, self.settingsMenu]):
            menu['tearoff'] = False
            self.menu.add_cascade(label = name, menu = menu)
        self.master.config(menu = self.menu)

        ## Generate Widgets
        self.resultTypeLabel = Label(self, text = 'Type:')
        self.resultType = StringVar(self)
        self.resultTypeDropdown = OptionMenu(self, self.resultType, *resultTypeOptions, command = lambda event: self.onResultTypeChange())
        self.resultFormatLabel = Label(self, text = 'Format:')
        self.resultFormat = StringVar(self)
        self.resultFormatDropdown = OptionMenu(self, self.resultFormat, *resultFormatOptions, command = lambda event: self.onResultFormatChange())
        self.dropdownTypes = [RESULT_TYPE, RESULT_FORMAT]

        self.rowLabel = Label(self, text = 'Rows:')
        self.rowEntry = Entry(self)
        self.colLabel = Label(self, text = 'Columns:')
        self.colEntry = Entry(self)
        self.rowEntry.focus()
        for entry in [self.rowEntry, self.colEntry]:
            entry.bind('<KeyPress>', self.moveFocus)
            entry.bind('<KeyRelease>', self.onRowColChange)
        if self.rememberSizeVar.get():
            rememberedSize = self.settings[REMEMBER_SIZE]
            r, c = rememberedSize
            if r:
                setEntry(self.rowEntry, r)
            if c:
                setEntry(self.colEntry, c)
            self.generateEntries(r, c)

        ## Place Widgets
        for i, w in enumerate([self.resultTypeLabel, self.resultTypeDropdown, self.resultFormatLabel, self.resultFormatDropdown]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)

        ## Bind
        self.master.bind('<Return>', lambda event: self.generate())
        self.master.bind('<Control-r>', lambda event: self.randomFill())
        self.master.bind('<Control-z>', lambda event: self.undo())
        self.master.bind('<Control-y>', lambda event: self.redo())
        self.master.bind('<Control-u>', lambda event: self.unitMatrix())
        self.master.bind('<Control-m>', lambda event: self.multiply())
        self.master.bind('<Control-t>', lambda event: self.transpose())
        self.master.bind('<Control-[>', lambda event: self.switchResultType(-1))
        self.master.bind('<Control-]>', lambda event: self.switchResultType(1))
        self.master.bind('<Control-E>', lambda event: self.clear(0))
        self.master.bind('<Control-A>', lambda event: self.clear(1))
        self.master.bind('<Alt-[>', lambda event: self.switchResultFormat(-1))
        self.master.bind('<Alt-]>', lambda event: self.switchResultFormat(1))

        ## Set Values
        self.settings.setdefault(LAST_USED_DROPDOWN, LATEX)
        self.setResultType(self.settings.setdefault(RESULT_TYPE, MATRIX))
        self.setResultFormat(self.settings.setdefault(RESULT_FORMAT, LATEX))
        register(lambda: fwrite(settingsFile, dumps(self.settings)))

    def getRow(self):
        try:
            return int(self.rowEntry.get())
        except ValueError:
            return 0

    def getCol(self):
        try:
            return int(self.colEntry.get())
        except ValueError:
            return 0

    def setRow(self, num):
        setEntry(self.rowEntry, num)

    def setCol(self, num):
        setEntry(self.colEntry, num)

    def setResultType(self, resultType):
        if self.resultType.get() == resultType:
            return
        self.resultType.set(resultType)
        self.onResultTypeChange()

    def onResultTypeChange(self):
        resultType = self.resultType.get()
        self.settings[LAST_USED_DROPDOWN] = RESULT_TYPE
        self.settings[RESULT_TYPE] = resultType
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
        if self.resultFormat.get() == resultFormat:
            return
        self.resultFormat.set(resultFormat)
        self.onResultFormatChange()

    def onResultFormatChange(self):
        self.settings[LAST_USED_DROPDOWN] = RESULT_FORMAT
        self.settings[RESULT_FORMAT] = self.resultFormat.get()

    def onRowColChange(self, event):
        text = event.widget.get()
        if not text:
            return
        if not text.isnumeric():
            text = text[:-1]
            setEntry(event.widget, text)
        elif int(text) > maxSize:
            text = str(maxSize)
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
        if self.rememberSizeVar.get():
            self.settings[REMEMBER_SIZE] = (r, c)
        self.modifyStates()

    def generateEntries(self, row, col):
        if not row or not col:
            return
        for i in range(row):
            for j in range(col):
                if (i, j) in self.entries:
                    continue
                e = Entry(self)
                e.bind('<KeyRelease>', self.onEntryChange)
                e.bind('<KeyPress>', self.moveFocus)
                e.grid(row = i + self.minRows, column = j, sticky = NSEW)
                self.entries[(i, j)] = e
        for i, j in self.entries.copy():
            if i not in range(row) or j not in range(col):
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
        self.modifyStates()

    def multiply(self):
        multiplier = simpledialog.askfloat(title = 'Multiply', \
                                           prompt = 'Multiply Each Entry By', \
                                           minvalue = -maxSize, \
                                           maxvalue = maxSize)
        if not multiplier or multiplier == 1:
            return
        for entry in self.entries.values():
            text = entry.get()
            if text.isnumeric():
                new_text = ezs.integer(eval(text) * multiplier)
            else:
                coef = ''
                countDot = 0
                for ch in text:
                    if ch.isnumeric():
                        coef += ch
                    elif ch == '.':
                        if countDot == 1:
                            coef = ''
                            break
                        countDot = 1
                        coef += ch
                    else:
                        break
                new_text = str(ezs.integer(eval(coef) * multiplier)) + text[len(coef):] if coef else \
                           str(ezs.integer(multiplier)) + text
            setEntry(entry, new_text)
        self.modifyStates()

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

    def insert(self, fromFormat):
        '''fromFormat can only be LaTeX or Array'''
        def isIdentity(matrix):
            zero = ['0', 0]
            one = ['1', 1]
            for i, row in enumerate(matrix):
                for j, entry in enumerate(row):
                    if (i == j and entry not in one) or (i != j and entry not in zero):
                        return False
            return True
        def getResultType(matrix):
            if matrix in [[[1]], [['1']]]:
                return MATRIX
            elif len(matrix[0]) == 1:
                return VECTOR
            else:
                return IDENTITY_MATRIX if isIdentity(matrix) else MATRIX
        try:
            title = 'Insert'
            prompt = f'Input Your Matrix in {fromFormat} Form'
            result = simpledialog.askstring(title = title, prompt = prompt)
            if not result:
                return
            if fromFormat == LATEX:
                if 'matrix' in result:
                    matrix = [row.split('&') for row in find(result).between('}', '\\end').split('\\\\')]
                    if 'bmatrix' in result:
                        self.setResultType(getResultType(matrix))
                    elif 'vmatrix' in result:
                        self.setResultType(DETERMINANT)
                else:
                    matrix = [[i] for i in find(result).between('{', '}').split(',')]
                    self.setResultType(VECTOR)
            elif fromFormat == ARRAY:
                matrix = eval(result)
                self.setResultType(getResultType(matrix))
            else:
                raise Exception()
            r = len(matrix)
            c = len(matrix[0])
            self.setRow(r)
            self.setCol(c)
            self.generateEntries(r, c)
            for i in range(r):
                for j in range(c):
                    setEntry(self.entries[(i, j)], matrix[i][j])
        except:
            messagebox.showerror(title = 'Error!', message = 'Invalid Input')

    def switchResultType(self, move):
        self.setResultType(resultTypeOptions[(resultTypeOptions.index(self.resultType.get()) + move) % len(resultTypeOptions)])

    def switchResultFormat(self, move):
        self.setResultFormat(resultFormatOptions[(resultFormatOptions.index(self.resultFormat.get()) + move) % len(resultFormatOptions)])

    def syncRowCol(self, size):
        self.setRow(size)
        self.setCol(size)
        self.generateEntries(size, size)

    def fillIdentityMatrix(self):
        for i, j in self.entries:
            setEntry(self.entries[(i, j)], 1 if i == j else 0)
        self.modifyStates()

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
            self.setRow(col)
            self.setCol(row)
            self.generateEntries(col, row)
        for i in range(row):
            for j in range(col):
                setEntry(self.entries[(j, i)], entries[(i, j)])
        self.modifyStates()

    def randomFill(self):
        resultType = self.resultType.get()
        ## Use ezs random matrix instead
        row = self.getRow()
        col = self.getCol()
        isIdentity = resultType == IDENTITY_MATRIX
        if not row or not col or isIdentity:
            if resultType == MATRIX:
                if not row:
                    row = randrange(maxSize) + 1
                if not col:
                    col = randrange(maxSize) + 1
            elif resultType == DETERMINANT:
                row = col = randrange(maxSize) + 1
            elif resultType == VECTOR:
                row = randrange(maxSize) + 1
            elif resultType == IDENTITY_MATRIX:
                row = col = randrange(maxSize) + 1
            self.setRow(row)
            self.setCol(col)
            self.generateEntries(row, col)
        if isIdentity:
            self.fillIdentityMatrix()
        else:
            for entry in self.entries.values():
                setEntry(entry, randrange(1, 10))
        self.modifyStates()

    def triangularMatrix(self, mode):
        '''Mode: 0 for lower, 1 for upper'''
        isIdentity = self.resultType.get() == IDENTITY_MATRIX
        for i, j in self.entries:
            if i < j if mode == 0 else i > j:
                setEntry(self.entries[(i ,j)], 0)
            elif isIdentity:
                setEntry(self.entries[(i ,j)], 1)
        if isIdentity:
            self.setResultType(MATRIX)
        self.modifyStates()

    def unitMatrix(self):
        if self.resultType.get() == IDENTITY_MATRIX:
            self.fillIdentityMatrix()
        else:
            for entry in self.entries.values():
                setEntry(entry, 1)
        self.modifyStates()

    def permutationMatrix(self):
        row = self.getRow()
        col = self.getCol()
        size = max(row, col) or min(row, col) or randrange(maxSize) + 1
        self.setResultType(MATRIX)
        if not row == col == size:
            self.syncRowCol(size)
        cols = list(range(size))
        for i in range(size):
            c = cols.pop(randrange(len(cols)))
            for j in range(size):
                setEntry(self.entries[(i, j)], 0)
            setEntry(self.entries[(i, c)], 1)
        self.modifyStates()

    def calculateDet(self):
        size = self.getRow()
        if size != self.getCol() or self.checkEmpty():
            return
        try:
            result = linalg.det([[eval(self.entries[(i, j)].get()) for j in range(size)] for i in range(size)])
            # result = ezs.dc(self.generate())
            str_result = str(result)
            copyToClipboard(str_result)
            if self.settings[SHOW_DIALOG]:
                messagebox.showinfo(title = 'Result', message = 'Value: ' + str_result)
            clearOption = self.calculateClearVar.get()
            if clearOption == CLEAR_ENTRIES:
                self.clear(0)
            elif clearOption == CLEAR_ALL:
                self.clear(1)
            return result
        except ValueError:
            messagebox.showerror(title = 'Error', message = 'Numerical Entries Only')

    def setupClearMenu(self, master, variable, command, label = 'Clear Options'):
        clearMenu = Menu(master = master, tearoff = False)
        for option in clearOptions[1:]:
            clearMenu.add_radiobutton(label = option, value = option, variable = variable, command = command)
        variable.set(self.settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        master.add_cascade(label = label, menu = clearMenu)

    def clear(self, mode = 0):
        '''0 for clear entries, 1 for clear all'''
        if mode >= 0:
            if self.resultType.get() == IDENTITY_MATRIX and mode == 0:
                return
            for entry in self.entries.values():
                clearEntry(entry)
        if mode >= 1:
            clearEntry(self.rowEntry)
            clearEntry(self.colEntry)
            for key, entry in self.entries.copy().items():
                entry.grid_forget()
                del self.entries[key]
        self.modifyStates()

    def checkEmpty(self):
        for entry in list(self.entries.values()) + [self.rowEntry, self.colEntry]:
            if not entry.get():
                messagebox.showerror(title = 'Error', message = 'Not All Entries are Filled')
                return True
        return False

    def generate(self):
        if self.checkEmpty():
            return
        result = ''
        r = self.getRow()
        c = self.getCol()
        resultType = self.resultType.get()
        resultFormat = self.resultFormat.get()
        if resultFormat == LATEX:
            if resultType == VECTOR and not self.colVecVar.get():
                result = ezs.vl(','.join(self.entries[(i, j)].get() for i in range(r) for j in range(c)), True, False)
            else:
                result = ezs.ml(r, c, ' '.join(self.entries[(i, j)].get() for i in range(r) for j in range(c)), False)
        elif resultFormat == ARRAY:
            result = ezs.mw(r, c, ' '.join(self.entries[(i, j)].get() for i in range(r) for j in range(c)), False)
        copyToClipboard(result)
        if self.settings[SHOW_DIALOG]:
            messagebox.showinfo(title = 'Result', message = result + '\nis Copied to the Clipboard!')
        clearOption = self.settings[GENERATE_CLEAR_OPTION]
        if clearOption == CLEAR_ENTRIES:
            self.clear(0)
        elif clearOption == CLEAR_ALL:
            self.clear(1)
        return result

    def undo(self):
        if not self.statePointer:
            return
        self.statePointer -= 1
        self.resumeState()

    def redo(self):
        if self.statePointer == len(self.states) - 1:
            return
        self.statePointer += 1
        self.resumeState()

    def resumeState(self):
        resultType, entries = self.states[self.statePointer]
        r = len(entries)
        c = len(entries[0])
        self.setRow(r)
        self.setCol(c)
        self.generateEntries(r, c)
        self.setResultType(resultType)
        for i, row in enumerate(entries):
            for j, entry in enumerate(row):
                setEntry(self.entries[(i, j)], entry)

    def modifyStates(self):
        row = self.getRow()
        col = self.getCol()
        if not row and not col:
            return
        state = (self.resultType.get(), [[self.entries[(i, j)].get() for j in range(col)] for i in range(row)])
        if self.states and state == self.states[self.statePointer]:
            return
        self.states = self.states[:self.statePointer + 1] + [state]
        self.statePointer = len(self.states) - 1

root = Tk()
gui = Generator(root)
gui.pack()
root.title('Generator')
root.mainloop()

py2pyw(__file__)
