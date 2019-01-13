from tkinter import *
from tkinter import messagebox, simpledialog
from json import dumps, loads
from atexit import register
from eztk import setEntry, clearEntry
from random import randrange
from numpy import linalg
from ez import fread, fwrite, copyToClipboard, py2pyw, find
import ezs, os

MATRIX = 'Matrix'
DETERMINANT = 'Determinant'
VECTOR = 'Vector'
IDENTITY_MATRIX = 'Identity Matrix'
resultTypeOptions = [MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX]
LATEX = 'LaTeX'
ARRAY = 'Array'
resultFormatOptions = [LATEX, ARRAY]
LEFT = 'Left'
RIGHT = 'Right'
UP = 'Up'
DOWN = 'Down'
shortcutFormatter = lambda command, shortcut: '{:<25}{:>15}'.format(command, shortcut)
SHORTCUTS = '\n'.join([shortcutFormatter('Switch Dropdown', 'Alt + ['), \
                       shortcutFormatter('Switch Dropdown', 'Alt + ]'), \
                       shortcutFormatter('Switch Dropdown Option', 'Ctrl + ['),\
                       shortcutFormatter('Switch Dropdown Option', 'Ctrl + ]'), \
                       shortcutFormatter('Generate', 'Enter/Return')])
CLEAR_SIZE = 'Clear Size'
CLEAR_ENTRIES = 'Clear Entries'
CLEAR_ALL = 'Clear All'
NONE = 'None'
clearOptions = [CLEAR_SIZE, CLEAR_ENTRIES, CLEAR_ALL, NONE]

class Generator(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        ## init variables
        self.master = master
        self.minRows = self.maxRows = 2
        self.minCols = self.maxCols = 4
        self.maxSize = 15
        self.entries = {}
        ## Strings
        self.GENERATE_CLEAR_OPTION = 'GenerateClearOption'
        self.CALCULATE_CLEAR_OPTION = 'CalculateClearOption'
        self.COLUMN_VECTOR = 'ColumnVector'
        self.REMEMBER_SIZE = 'RememberSize'
        self.SHOW_DIALOG = 'ShowDialog'
        self.RESULT_TYPE = 'ResultType'
        self.RESULT_FORMAT = 'ResultFormat'
        self.LAST_USED_DROPDOWN = 'LastUsedDropdown'
        ## Settings
        self.settingsFileName = 'settings.json'
        self.settings = loads(fread(self.settingsFileName)) if os.path.exists(self.settingsFileName) else {}

        ## generate menus
        self.menu = Menu(self)
        ## Edit Menu
        self.editMenu = Menu(self.menu)
        self.matMenu = Menu(self.menu)
        self.matMenu.add_command(label = 'Lower Triangular', command = lambda: self.triangularMatrix(0))
        self.matMenu.add_command(label = 'Upper Triangular', command = lambda: self.triangularMatrix(1))
        self.detMenu = Menu(self.menu)
        self.detMenu.add_command(label = 'Calculate', command = self.calculateDet)
        self.calculateClearVar = StringVar(self, value = self.settings.setdefault(self.GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.detMenu, self.calculateClearVar, \
                            lambda :self.settings.__setitem__(self.CALCULATE_CLEAR_OPTION, self.calculateClearVar.get()), \
                            'Clear After Calculate')
        self.vecMenu = Menu(self.menu)
        self.colVecVar = BooleanVar(self, value = self.settings.setdefault(self.COLUMN_VECTOR, True))
        self.vecMenu.add_checkbutton(label = 'Column Vector', variable = self.colVecVar, command = lambda :self.settings.__setitem__(self.COLUMN_VECTOR, self.colVecVar.get()))
        self.imatMenu = Menu(self.menu)
        self.imatMenu.add_command(label = 'Permutation Matrix', command = self.permutationMatrix)
        for name, menu in zip(resultTypeOptions, [self.matMenu, self.detMenu, self.vecMenu, self.imatMenu]):
            menu['tearoff'] = False
            self.editMenu.add_cascade(label = name, menu = menu)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = 'Multiply', command = self.multiply)
        self.editMenu.add_command(label = 'Transpose', command = self.transpose)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = CLEAR_SIZE, command = lambda: self.clear(0))
        self.editMenu.add_command(label = CLEAR_ENTRIES, command = lambda: self.clear(1))
        self.editMenu.add_command(label = CLEAR_ALL, command = lambda: self.clear(0, 1))
        ## Insert Menu
        self.insertMenu = Menu(self)
        self.insertMenu.add_command(label = 'Random', command = self.randomFill)
        self.insertMenu.add_command(label = 'Unit Matrix', command = self.unitMatrix)
        self.insertMenu.add_command(label = 'From ' + LATEX, command = lambda: self.insert(LATEX))
        self.insertMenu.add_command(label = 'From ' + ARRAY, command = lambda: self.insert(ARRAY))
        ## Generate Menu
        self.generateMenu = Menu(self.menu)
        self.generateMenu.add_command(label = shortcutFormatter('Generate', 'Enter/Return'), command = self.generate)
        self.generateClearVar = StringVar(self, value = self.settings.setdefault(self.GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.generateMenu, self.generateClearVar, \
                            lambda :self.settings.__setitem__(self.GENERATE_CLEAR_OPTION, self.generateClearVar.get()), \
                            'Clear After Generate')
        ## Settings Menu
        self.settingsMenu = Menu(self.menu)
        self.rememberSizeVar = BooleanVar(self, value = self.settings.setdefault(self.REMEMBER_SIZE, (-1, -1)) != (-1, -1))
        self.settingsMenu.add_checkbutton(label = 'Remember Size', variable = self.rememberSizeVar, \
                                          command = lambda :self.settings.__setitem__(self.REMEMBER_SIZE, (self.getRow(), self.getCol()) if self.rememberSizeVar.get() else (0, 0) ))
        self.showDialogVar = BooleanVar(self, value = self.settings.setdefault(self.SHOW_DIALOG, True))
        self.settingsMenu.add_checkbutton(label = 'Show Dialog', variable = self.showDialogVar, \
                                          command = lambda :self.settings.__setitem__(self.SHOW_DIALOG, self.showDialogVar.get()))
        self.settingsMenu.add_separator()
        self.settingsMenu.add_command(label = 'Keyboard Shortcuts', command = lambda: messagebox.showinfo(title = 'Shortcuts', message = SHORTCUTS))
        for name, menu in zip(['Edit', 'Insert', 'Generate', 'Settings'], [self.editMenu, self.insertMenu, self.generateMenu, self.settingsMenu]):            
            menu['tearoff'] = False
            self.menu.add_cascade(label = name, menu = menu)
        self.master.config(menu = self.menu)
        
        ## generate widgets
        self.resultTypeLabel = Label(self, text = 'Type:')
        self.resultType = StringVar(self)
        self.resultTypeDropdown = OptionMenu(self, self.resultType, *resultTypeOptions, command = lambda event: self.onResultTypeChange())
        self.resultFormatLabel = Label(self, text = 'Format:')
        self.resultFormat = StringVar(self)
        self.resultFormatDropdown = OptionMenu(self, self.resultFormat, *resultFormatOptions, command = lambda event: self.onResultFormatChange())
        self.dropdownTypes = [self.RESULT_TYPE, self.RESULT_FORMAT]
        
        self.rowLabel = Label(self, text = 'Rows:')
        self.rowEntry = Entry(self)
        self.colLabel = Label(self, text = 'Columns:')
        self.colEntry = Entry(self)
        self.rowEntry.focus()
        for entry in [self.rowEntry, self.colEntry]:
            entry.bind('<KeyPress>', self.moveFocus)
            entry.bind('<KeyRelease>', self.onRowColChange)
        if self.rememberSizeVar.get():            
            rememberedSize = self.settings[self.REMEMBER_SIZE]
            r, c = rememberedSize
            if r:
                setEntry(self.rowEntry, r)
            if c:
                setEntry(self.colEntry, c)
            self.generateEntries(r, c)

        ## place widgets
        for i, w in enumerate([self.resultTypeLabel, self.resultTypeDropdown, self.resultFormatLabel, self.resultFormatDropdown]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)

        ## set values        
        self.master.bind('<Return>', lambda event: self.generate())
        self.master.bind('<Control-[>', lambda event: self.switchDropdownOption(-1))
        self.master.bind('<Alt-[>', lambda event: self.switchLastUsedDropdown(-1))
        self.master.bind('<Control-]>', lambda event: self.switchDropdownOption(1))
        self.master.bind('<Alt-]>', lambda event: self.switchLastUsedDropdown(1))
        # self.master.bind('<Control-r>', lambda event: self.randomFill)
        self.settings.setdefault(self.LAST_USED_DROPDOWN, self.RESULT_TYPE)
        self.setResultType(self.settings.setdefault(self.RESULT_TYPE, MATRIX))
        self.setResultFormat(self.settings.setdefault(self.RESULT_FORMAT, LATEX))
        register(lambda: fwrite(self.settingsFileName, dumps(self.settings)))
        
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
        self.resultType.set(resultType)
        self.onResultTypeChange()

    def onResultTypeChange(self):
        resultType = self.resultType.get()
        self.settings[self.LAST_USED_DROPDOWN] = self.RESULT_TYPE
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
        self.settings[self.LAST_USED_DROPDOWN] = self.RESULT_FORMAT
        self.settings[self.RESULT_FORMAT] = self.resultFormat.get()

    def onRowColChange(self, event):
        text = event.widget.get()
        if not text:
            return
        if not text.isnumeric():
            text = text[:-1]
            setEntry(event.widget, text)
        elif int(text) > self.maxSize:
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
        if self.rememberSizeVar.get():
            self.settings[self.REMEMBER_SIZE] = (r, c)

    def generateEntries(self, row, column):
        if not row or not column:
            return
        for i in range(row):
            for j in range(column):
                if (i, j) in self.entries:
                    continue
                e = Entry(self)
                e.bind('<KeyRelease>', self.onEntryChange)
                e.bind('<KeyPress>', self.moveFocus)
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

    def multiply(self):
        multiplier = simpledialog.askfloat(title = 'Multiply', \
                                           prompt = 'Multiply Each Entry By', \
                                           minvalue = -self.maxSize, \
                                           maxvalue = self.maxSize)
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

    def switchDropdownOption(self, move):
        '''Move should mostly be 1 or -1'''
        last = self.settings[self.LAST_USED_DROPDOWN]
        if last == self.RESULT_TYPE:
            self.setResultType(resultTypeOptions[(resultTypeOptions.index(self.resultType.get()) + move) % len(resultTypeOptions)])
        elif last == self.RESULT_FORMAT:
            self.setResultFormat(resultFormatOptions[(resultFormatOptions.index(self.resultFormat.get()) + move) % len(resultFormatOptions)])

    def switchLastUsedDropdown(self, move):
        self.settings[self.LAST_USED_DROPDOWN] = self.dropdownTypes[(self.dropdownTypes.index(self.settings[self.LAST_USED_DROPDOWN]) + move) % len(self.dropdownTypes)]

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
            self.setRow(col)
            self.setCol(row)
            self.generateEntries(col, row)
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
                    row = randrange(self.maxSize) + 1
                if not col:
                    col = randrange(self.maxSize) + 1
            elif resultType == DETERMINANT:
                row = col = randrange(self.maxSize) + 1
            elif resultType == VECTOR:
                row = randrange(self.maxSize) + 1
            elif resultType == IDENTITY_MATRIX:
                row = col = randrange(self.maxSize) + 1
            self.setRow(row)
            self.setCol(col)
            self.generateEntries(row, col)
        if isIdentity:
            self.fillIdentityMatrix()
        else:
            for entry in self.entries.values():
                setEntry(entry, randrange(1, 10))

    def triangularMatrix(self, mode):
        '''Mode: 0 for lower, 1 for upper'''
        isIdentity = self.resultType.get() == IDENTITY_MATRIX
        f = lambda i, j: i < j if mode == 0 else i > j
        for i, j in self.entries:
            if f(i, j):
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
        size = max(row, col) or min(row, col) or randrange(self.maxSize) + 1
        self.setResultType(MATRIX)
        if not row == col == size:
            self.syncRowCol(size)
        cols = list(range(size))
        for i in range(size):
            c = cols.pop(randrange(len(cols)))
            for j in range(size):
                setEntry(self.entries[(i, j)], 0)
            setEntry(self.entries[(i, c)], 1)

    def calculateDet(self):
        size = self.getRow()
        if size != self.getCol() or self.checkEmpty():
            return
        try:
            result = linalg.det([[eval(self.entries[(i, j)].get()) for j in range(size)] for i in range(size)])
            # result = ezs.dc(self.generate())
            str_result = str(result)
            copyToClipboard(str_result)
            if self.settings[self.SHOW_DIALOG]:
                messagebox.showinfo(title = 'Result', message = 'Value: ' + str_result)
            clearOption = self.calculateClearVar.get()
            if clearOption == CLEAR_ENTRIES:
                self.clear(1)
            elif clearOption == CLEAR_ALL:
                self.clear(0, 1)
            return result
        except ValueError:
            messagebox.showerror(title = 'Error', message = 'Numerical Entries Only')

    def setupClearMenu(self, master, variable, command, label = 'Clear Options'):
        clearMenu = Menu(master = master, tearoff = False)
        for option in clearOptions[1:]:
            clearMenu.add_radiobutton(label = option, value = option, variable = variable, command = command)
        variable.set(self.settings.setdefault(self.GENERATE_CLEAR_OPTION, NONE))
        master.add_cascade(label = label, menu = clearMenu)
        
    def clear(self, *mode):
        '''0 for clear size, 1 for clear entries'''
        if 0 in mode:
            clearEntry(self.rowEntry)
            clearEntry(self.colEntry)
            for key, entry in self.entries.copy().items():
                entry.grid_forget()
                del self.entries[key]
        if 1 in mode and self.resultType.get() != IDENTITY_MATRIX:
            for entry in self.entries.values():
                clearEntry(entry)
    
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
        if self.settings[self.SHOW_DIALOG]:
            messagebox.showinfo(title = 'Result', message = result + '\nis Copied to the Clipboard!')
        clearOption = self.settings[self.GENERATE_CLEAR_OPTION]
        if clearOption == CLEAR_ENTRIES:
            self.clear(1)
        elif clearOption == CLEAR_ALL:
            self.clear(0, 1)
        return result

root = Tk()
gui = Generator(root)
gui.pack()
root.title('Generator')
root.mainloop()

py2pyw(__file__)
