from tkinter import *
from tkinter import messagebox, simpledialog
from eztk import setEntry, clearEntry
from random import randrange, shuffle
from numpy import linalg
import ez, ezs, os
from Dialogs import *

## Constant Variables
maxSize = 25
maxRandomVarLength = 10
minValue = -100
maxValue = 100

defaultVar = 'x'

MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX = 'Matrix', 'Determinant', 'Vector', 'Identity Matrix'
resultTypeOptions = [MATRIX, DETERMINANT, VECTOR]
LATEX, ARRAY = 'LaTeX', 'Array'
resultFormatOptions = [LATEX, ARRAY]
LEFT, RIGHT, UP, DOWN = 'Left', 'Right', 'Up', 'Down'
directions = [LEFT, RIGHT, UP, DOWN]
CLEAR_ENTRIES, CLEAR_ALL = 'Clear Entries', 'Clear All'
NONE = 'None'
clearOptions = [CLEAR_ENTRIES, CLEAR_ALL, NONE]
GENERATE_CLEAR_OPTION = 'GenerateClearOption'
CALCULATE_CLEAR_OPTION = 'CalculateClearOption'
VECTOR_OPTION = 'VectorOption'
ARRAY_VECTOR = 'ArrayVector'
COLUMN_VECTOR = 'Column Vector'
OVERRIGHTARROW = 'OverRightArrow'
vectorOptions = [COLUMN_VECTOR, OVERRIGHTARROW,  VECTOR]
REMEMBER_SIZE = 'RememberSize'
SHOW_RESULT = 'Show Result'
SHOW_CALCULATION_RESULT = 'ShowCalculationResult'
SHOW_GENERATION_RESULT = 'ShowGenerationResult'
COPY_RESULT = 'Copy Result'
COPY_CALCULATION_RESULT = 'CopyCalculationResult'
COPY_GENERATION_RESULT = 'CopyGenerationResult'
RESULT_TYPE = 'ResultType'
RESULT_FORMAT = 'ResultFormat'
ZERO_MATRIX = 'Zero Matrix'
APPEND_START = 'Append Start'
APPEND_END = 'Append End'
FIND_VALUE = 'Find Value'
FIND_LOCATION = 'Find Location'
REPLACE = 'Replace'
CALCULATE = 'Calculate'
UNIT_MATRIX = 'Unit Matrix'
PERMUTATION_MATRIX = 'Permutation Matrix'
PERMUTATION_VECTOR = 'Permutation Vector'
ADD = 'Add'
MULTIPLY = 'Multiply'
TRANSPOSE = 'Transpose'
RANDOM = 'Random'
RANDOM_MATRIX = 'Random Matrix'
RANDOM_REORDER = 'Random Reorder'
RANDOM_INT_MATRIX = 'Random Int Matrix'
RANDOM_VAR_MATRIX = 'Random Var Matrix'
RANDOM_MULTIVAR_MATRIX = 'Random Multi-Var Matrix'
RANDOM_MATRIX_OPTION = 'RandomMatrixOption'
randomMatrixOptions = [RANDOM_INT_MATRIX, RANDOM_VAR_MATRIX, RANDOM_MULTIVAR_MATRIX]
RANDOM_MIN = 'RandomMin'
RANDOM_MAX = 'RandomMax'
RANDOM_VAR = 'RandomVar'
GENERATE = 'Generate'
UNDO = 'Undo'
REDO = 'Redo'
SORT = 'Sort'
REVERSE = 'Reverse'
RESHAPE = 'Reshape'
LOWER = 'Lower'
UPPER = 'Upper'
LOWER_TRIANGULAR = 'Lower Triangular'
UPPER_TRIANGULAR = 'Upper Triangular'
LOWER_CASE = 'Lower Case'
UPPER_CASE = 'Upper Case'
ONE_TO_N = '1 to N'
A_TO_Z = 'A to Z'
FROM_ARRAY = 'From ' + ARRAY
FROM_LATEX = 'From ' + LATEX
EXIT = 'Exit'
ENTRY_WIDTH = 'EntryWidth'

## Settings
settingOptions = [RESULT_TYPE, RESULT_FORMAT, REMEMBER_SIZE, VECTOR_OPTION, RANDOM_VAR, RANDOM_MIN, RANDOM_MAX, RANDOM_MATRIX_OPTION, ENTRY_WIDTH, \
                  SHOW_GENERATION_RESULT, SHOW_CALCULATION_RESULT, COPY_GENERATION_RESULT, COPY_CALCULATION_RESULT, GENERATE_CLEAR_OPTION, CALCULATE_CLEAR_OPTION]

## Shortcuts
shortcuts = { GENERATE: 'Enter/Return', ADD: 'Ctrl+=', ZERO_MATRIX: 'Ctrl+0', IDENTITY_MATRIX: 'Ctrl+I', RANDOM_MATRIX: 'Ctrl+R', UNIT_MATRIX: 'Ctrl+U', EXIT: 'Ctrl+W', \
              MULTIPLY: 'Ctrl+M', PERMUTATION_MATRIX: 'Ctrl+P', PERMUTATION_VECTOR: 'Ctrl+P', FIND_VALUE: 'Ctrl+F', REPLACE: 'Ctrl+H', REDO: 'Ctrl+Y', UNDO: 'Ctrl+Z', \
              CLEAR_ALL: 'Ctrl+Shift+A', CALCULATE: 'Ctrl+Shift+C', CLEAR_ENTRIES: 'Ctrl+Shift+E', FIND_LOCATION: 'Ctrl+Shift+F', LOWER_TRIANGULAR: 'Ctrl+Shift+L', RANDOM_REORDER: 'Ctrl+Shift+R', UPPER_TRIANGULAR: 'Ctrl+Shift+U', \
              A_TO_Z: 'Alt+A', APPEND_END: 'Alt+E', LOWER_CASE: 'Alt+L', ONE_TO_N: 'Alt+N', RESHAPE: 'Alt+R', APPEND_START: 'Alt+S', TRANSPOSE: 'Alt+T', UPPER_CASE: 'Alt+U', \
              FROM_ARRAY: 'Alt+Shift+A', FROM_LATEX: 'Alt+Shift+L', REVERSE: 'Alt+Shift+R', SORT: 'Alt+Shift+S'}
otherShortcutFormatter = lambda command, shortcut: '{:<25}{:<15}'.format(command, shortcut)
otherShortcuts = '\n'.join([otherShortcutFormatter(command, shortcut) for command, shortcut in \
                            [('Switch Result Type', 'Ctrl+[ Ctrl+]'), ('Switch Result Format', 'Alt+[ Alt+]'), ('Exit', 'Ctrl+W')]])

class Generator(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        ## Settings
        self.settings = ez.Settings(__file__)
        self.settings.setSettingOptions(settingOptions)

        ## init variables
        self.minRows = self.maxRows = 2
        self.minCols = self.maxCols = 4
        self.entries = {}
        self.stateIndex = 0
        self.states = [] ## (resultType, entries, focusEntry)
        ## Find Dialog
        self.findDialog = None
        self.findResult = []
        self.prevFind = ''
        self.findIndex = -1
        ## Replace Dialog
        self.replaceDialog = None
        self.prevReplace = ''
        self.currentDialog = None
        ## Slider Dialog
        self.sliderDialog = None

        ## Generate Menus
        self.menu = Menu(self)
        ## Result Menu
        self.resultMenu = Menu(self)
        self.matMenu = Menu(self)
        self.matMenu.add_command(label = IDENTITY_MATRIX, accelerator = shortcuts[IDENTITY_MATRIX], command = self.fillIdentityMatrix)
        self.matMenu.add_command(label = PERMUTATION_MATRIX, accelerator = shortcuts[PERMUTATION_MATRIX], command = self.permutationMatrix)
        self.matMenu.add_command(label = ZERO_MATRIX, accelerator = shortcuts[ZERO_MATRIX], command = self.fillZeroMatrix)
        self.matMenu.add_command(label = UNIT_MATRIX, accelerator = shortcuts[UNIT_MATRIX], command = self.unitMatrix)
        self.detMenu = Menu(self)
        self.detMenu.add_command(label = CALCULATE, accelerator = shortcuts[CALCULATE], command = self.calculateDet)
        self.calculateClearVar = StringVar(self, value = self.settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.detMenu, self.calculateClearVar, \
                            lambda: self.settings.setitem(CALCULATE_CLEAR_OPTION, self.calculateClearVar.get()), \
                            SHOW_CALCULATION_RESULT, COPY_CALCULATION_RESULT, 'After Calculation')
        self.vecMenu = Menu(self)
        self.vecMenu.add_command(label = PERMUTATION_VECTOR, accelerator = shortcuts[PERMUTATION_VECTOR], command = self.permutationVector)
        self.vecOptionMenu = Menu(self, tearoff = False)
        self.arrayVecVar = BooleanVar(self, value = self.settings.setdefault(ARRAY_VECTOR, False))
        self.vecOptionMenu.add_checkbutton(label = 'Array Vector', variable = self.arrayVecVar, \
                                           command = lambda: self.settings.setitem(ARRAY_VECTOR, self.arrayVecVar.get()))
        self.vecOptionMenu.add_separator()
        self.vecOptionVar = StringVar(self)
        for option in vectorOptions:
            self.vecOptionMenu.add_radiobutton(label = option, variable = self.vecOptionVar, \
                                               command = lambda: self.settings.setitem(VECTOR_OPTION, self.vecOptionVar.get()))
        self.vecOptionVar.set(self.settings.setdefault(VECTOR_OPTION, COLUMN_VECTOR))
        self.vecMenu.add_cascade(label = 'Vector Options', menu = self.vecOptionMenu)
        for name, menu in zip(resultTypeOptions, [self.matMenu, self.detMenu, self.vecMenu]):
            menu['tearoff'] = False
            self.resultMenu.add_cascade(label = name, menu = menu)
        ## Edit Menu
        self.editMenu = Menu(self)
        self.editMenu.add_command(label = UNDO, accelerator = shortcuts[UNDO], command = self.undo)
        self.editMenu.add_command(label = REDO, accelerator = shortcuts[REDO], command = self.redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = FIND_VALUE, accelerator = shortcuts[FIND_VALUE], command = lambda: self.find(FIND_VALUE))
        self.editMenu.add_command(label = FIND_LOCATION, accelerator = shortcuts[FIND_LOCATION], command = lambda: self.find(FIND_LOCATION))
        self.editMenu.add_command(label = REPLACE, accelerator = shortcuts[REPLACE], command = self.replace)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = LOWER_CASE, accelerator = shortcuts[LOWER_CASE], command = lambda: self.toCase(LOWER_CASE))
        self.editMenu.add_command(label = UPPER_CASE, accelerator = shortcuts[UPPER_CASE], command = lambda: self.toCase(UPPER_CASE))
        self.editMenu.add_separator()
        self.editMenu.add_command(label = CLEAR_ENTRIES, accelerator = shortcuts[CLEAR_ENTRIES], command = lambda: self.clear(0))
        self.editMenu.add_command(label = CLEAR_ALL, accelerator = shortcuts[CLEAR_ALL], command = lambda: self.clear(1))
        ## Insert Menu
        self.insertMenu = Menu(self)
        self.insertMenu.add_command(label = APPEND_START, accelerator = shortcuts[APPEND_START], command = lambda: self.append(APPEND_START))
        self.insertMenu.add_command(label = APPEND_END, accelerator = shortcuts[APPEND_END], command = lambda: self.append(APPEND_END))
        self.insertMenu.add_separator()
        self.insertMenu.add_command(label = FROM_LATEX, accelerator = shortcuts[FROM_LATEX], command = lambda: self.insert(LATEX))
        self.insertMenu.add_command(label = FROM_ARRAY, accelerator = shortcuts[FROM_ARRAY], command = lambda: self.insert(ARRAY))
        self.insertMenu.add_separator()
        self.insertMenu.add_command(label = ONE_TO_N, accelerator = shortcuts[ONE_TO_N], command = self.oneToN)
        self.insertMenu.add_command(label = A_TO_Z, accelerator = shortcuts[A_TO_Z], command = self.aToZ)
        self.randomMenu = Menu(self, tearoff = False)
        self.randomMenu.add_command(label = RANDOM_MATRIX, accelerator = shortcuts[RANDOM_MATRIX], command = self.randomFill)
        self.randomMenu.add_command(label = RANDOM_REORDER, accelerator = shortcuts[RANDOM_REORDER], command = self.randomReorder)
        self.randomMenu.add_separator()
        self.randomMatrixOption = StringVar(self)
        for option in randomMatrixOptions:
            self.randomMenu.add_radiobutton(label = option, variable = self.randomMatrixOption, \
                                            command = lambda: self.settings.setitem(RANDOM_MATRIX_OPTION, self.randomMatrixOption.get()))
        self.randomMatrixOption.set(self.settings.setdefault(RANDOM_MATRIX_OPTION, RANDOM_INT_MATRIX))
        self.randomMenu.add_separator()
        self.randomMenu.add_command(label = 'Set Random Min', command = lambda: self.setRandom(min))
        self.randomMenu.add_command(label = 'Set Random Max', command = lambda: self.setRandom(max))
        self.randomMenu.add_command(label = 'Set Random Var', command = lambda: self.setRandom('var'))
        self.insertMenu.add_cascade(label = RANDOM, menu = self.randomMenu)
        ## Modify Menu
        self.modifyMenu = Menu(self)
        self.modifyMenu.add_command(label = ADD, accelerator = shortcuts[ADD], command = self.add)
        self.modifyMenu.add_command(label = MULTIPLY, accelerator = shortcuts[MULTIPLY], command = self.multiply)
        self.modifyMenu.add_separator()
        self.modifyMenu.add_command(label = TRANSPOSE, accelerator = shortcuts[TRANSPOSE], command = self.transpose)
        self.modifyMenu.add_command(label = RESHAPE, accelerator = shortcuts[RESHAPE], command = self.reshape)
        self.modifyMenu.add_separator()
        self.modifyMenu.add_command(label = LOWER_TRIANGULAR, accelerator = shortcuts[LOWER_TRIANGULAR], command = lambda: self.triangularMatrix(LOWER))
        self.modifyMenu.add_command(label = UPPER_TRIANGULAR, accelerator = shortcuts[UPPER_TRIANGULAR], command = lambda: self.triangularMatrix(UPPER))
        self.modifyMenu.add_separator()
        self.modifyMenu.add_command(label = SORT, accelerator = shortcuts[SORT], command = self.sort)
        self.modifyMenu.add_command(label = REVERSE, accelerator = shortcuts[REVERSE], command = self.reverse)
        ## Generate Menu
        self.generateMenu = Menu(self)
        self.generateMenu.add_command(label = GENERATE, accelerator = shortcuts[GENERATE], command = self.generate)
        self.generateClearVar = StringVar(self, value = self.settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.generateMenu, self.generateClearVar, \
                            lambda: self.settings.setitem(GENERATE_CLEAR_OPTION, self.generateClearVar.get()), \
                            SHOW_GENERATION_RESULT, COPY_GENERATION_RESULT, 'After Generation')
        ## Settings Menu
        self.settingsMenu = Menu(self)
        self.rememberSizeVar = BooleanVar(self, value = self.settings.setdefault(REMEMBER_SIZE, (-1, -1)) != (-1, -1))
        self.settingsMenu.add_command(label = 'Adjust Entry Width', command = self.adjustEntryWidth)
        self.settingsMenu.add_checkbutton(label = 'Remember Size', variable = self.rememberSizeVar, \
                                          command = lambda: self.settings.setitem(REMEMBER_SIZE, (self.getRow(), self.getCol()) if self.rememberSizeVar.get() else (0, 0) ))
        self.settingsMenu.add_separator()
        self.settingsMenu.add_command(label = 'Other Keyboard Shortcuts', command = lambda: messagebox.showinfo(title = 'Shortcuts', message = otherShortcuts))
        for name, menu in zip(['Result', 'Edit', 'Insert', 'Modify', 'Generate', 'Settings'], [self.resultMenu, self.editMenu, self.insertMenu, self.modifyMenu, self.generateMenu, self.settingsMenu]):
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

        self.rowLabel = Label(self, text = 'Rows:')
        self.rowEntry = Entry(self)
        self.colLabel = Label(self, text = 'Columns:')
        self.colEntry = Entry(self)
        self.rowEntry.focus()
        for entry in [self.rowEntry, self.colEntry]:
            self.bindMoveFocus(entry)
            entry.bind('<KeyRelease>', self.onRowColChange)
            bindtags = entry.bindtags()
            entry.bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))
        if self.rememberSizeVar.get():
            r, c = self.settings[REMEMBER_SIZE]
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
        self.master.bind('<Destroy>', lambda event: self.onDestroy())
        self.master.bind('<Return>', lambda event: self.generate())
        self.master.bind('<Control-0>', lambda event: self.fillZeroMatrix())
        self.master.bind('<Control-f>', lambda event: self.find(FIND_VALUE))
        self.master.bind('<Control-h>', lambda event: self.replace())
        self.master.bind('<Control-i>', lambda event: self.fillIdentityMatrix())
        self.master.bind('<Control-m>', lambda event: self.multiply())
        self.master.bind('<Control-p>', lambda event: self.permutationVector() if self.resultType.get() == VECTOR or self.getCol() == 1 else self.permutationMatrix())
        self.master.bind('<Control-r>', lambda event: self.randomFill())
        self.master.bind('<Control-u>', lambda event: self.unitMatrix())
        self.master.bind('<Control-w>', lambda event: self.master.destroy())
        self.master.bind('<Control-y>', lambda event: self.redo())
        self.master.bind('<Control-z>', lambda event: self.undo())
        self.master.bind('<Control-=>', lambda event: self.add())
        self.master.bind('<Control-[>', lambda event: self.switchResultType(-1))
        self.master.bind('<Control-]>', lambda event: self.switchResultType(1))
        self.master.bind('<Control-A>', lambda event: self.clear(1))
        self.master.bind('<Control-C>', lambda event: self.calculateDet())
        self.master.bind('<Control-E>', lambda event: self.clear(0))
        self.master.bind('<Control-F>', lambda event: self.find(FIND_LOCATION))
        self.master.bind('<Control-L>', lambda event: self.triangularMatrix(LOWER))
        self.master.bind('<Control-R>', lambda event: self.randomReorder())
        self.master.bind('<Control-U>', lambda event: self.triangularMatrix(UPPER))
        self.master.bind('<Alt-a>', lambda event: self.aToZ())
        self.master.bind('<Alt-e>', lambda event: self.append(APPEND_END))
        self.master.bind('<Alt-l>', lambda event: self.toCase(LOWER))
        self.master.bind('<Alt-n>', lambda event: self.oneToN())
        self.master.bind('<Alt-r>', lambda event: self.reshape())
        self.master.bind('<Alt-s>', lambda event: self.append(APPEND_START))
        self.master.bind('<Alt-t>', lambda event: self.transpose())
        self.master.bind('<Alt-u>', lambda event: self.toCase(UPPER))
        self.master.bind('<Alt-[>', lambda event: self.switchResultFormat(-1))
        self.master.bind('<Alt-]>', lambda event: self.switchResultFormat(1))
        self.master.bind('<Alt-A>', lambda event: self.insert(ARRAY))
        self.master.bind('<Alt-L>', lambda event: self.insert(LATEX))
        self.master.bind('<Alt-R>', lambda event: self.reverse())
        self.master.bind('<Alt-S>', lambda event: self.sort())

        ## Set Values
        self.settings.setdefault(RANDOM_MIN, 1)
        self.settings.setdefault(RANDOM_MAX, maxSize)
        self.settings.setdefault(RANDOM_VAR, defaultVar)
        self.setResultType(self.settings.setdefault(RESULT_TYPE, MATRIX))
        self.setResultFormat(self.settings.setdefault(RESULT_FORMAT, LATEX))
        self.modifyStates()

    def getRow(self):
        try: return int(self.rowEntry.get())
        except ValueError: return 0

    def getCol(self):
        try: return int(self.colEntry.get())
        except ValueError: return 0

    def setRow(self, row):
        setEntry(self.rowEntry, row)

    def setCol(self, col):
        setEntry(self.colEntry, col)

    def setRowCol(self, row, col):
        self.setRow(row)
        self.setCol(col)

    def setResultType(self, resultType):
        if self.resultType.get() == resultType:
            return
        self.resultType.set(resultType)
        self.onResultTypeChange()

    def onResultTypeChange(self):
        resultType = self.resultType.get()
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

    def setResultFormat(self, resultFormat):
        if self.resultFormat.get() == resultFormat:
            return
        self.resultFormat.set(resultFormat)
        self.onResultFormatChange()

    def onResultFormatChange(self):
        self.settings[RESULT_FORMAT] = self.resultFormat.get()

    def onRowColChange(self, event):
        text = event.widget.get()
        if not text:
            return
        value = ez.tryEval(text)
        if not text.isnumeric():
            new_text = ''
            for ch in text:
                if ch.isnumeric():
                    new_text += ch
                else:
                    break
            value = int(new_text) if new_text else 0
        setEntry(event.widget, min(value, maxSize))
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
                entry = Entry(self, width = self.settings.setdefault(ENTRY_WIDTH, 20))
                self.bindMoveFocus(entry)
                entry.bind('<KeyRelease>', lambda event: self.onEntryChange)
                bindtags = entry.bindtags()
                entry.bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))
                entry.grid(row = self.minRows + i, column = j, sticky = NSEW)
                self.entries[(i, j)] = entry
        for i, j in self.entries.copy():
            if i not in range(row) or j not in range(col):
                self.entries[(i, j)].grid_forget()
                del self.entries[(i, j)]
        self.maxRows = self.minRows + row
        self.maxCols = max(self.minCols, col)

    def onEntryChange(self):
        self.modifyStates()

    def add(self):
        result = simpledialog.askstring(title = 'Multiply', prompt = 'Add to Each Entry')
        if not result:
            return
        result = ezs.integer(ez.tryEval(result))
        if result == 0:
            return
        for entry in self.entries.values():
            text = ez.tryEval(entry.get())
            if not text:
                new_text = result
            elif ezs.isNumeric(text) and ezs.isNumeric(result):
                new_text = ezs.integer(text + result)
            else:
                if ezs.isNumeric(result):
                    result = ('+' if result > 0 else '') + str(result)
                new_text = f'{text}{result}'
            setEntry(entry, new_text)
        self.modifyStates()

    def multiply(self):
        result = ezs.integer(ez.tryEval(simpledialog.askstring(title = 'Multiply', prompt = 'Multiply Each Entry By')))
        if result == None or result == 1:
            return
        if result == 0:
            self.fillZeroMatrix()
            return
        isResultNumeric = ezs.isNumeric(result)
        for entry in self.entries.values():
            text = ez.tryEval(entry.get())
            if text:
                isTextNumeric = ezs.isNumeric(text)
                if isResultNumeric:
                    if isTextNumeric:
                        new_text = ezs.integer(text * result)
                    else:
                        if '+' in text or '-' in text:
                            new_text = f'{result}({text})'
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
                            new_text = str(ezs.integer(eval(coef) * result)) + text[len(coef):] if coef else \
                                    str(ezs.integer(result)) + text
                else:
                    if '+' in result or '-' in result:
                        new_text = f'{text}({result})'
                    else:
                        new_text = f'{text}{result}'
            else:
                new_text = 0
            setEntry(entry, new_text)
        self.modifyStates()

    def moveFocus(self, event):
        key = event.keysym
        cursor_index = event.widget.index(INSERT)
        if (key == LEFT and cursor_index > 0) or \
           (key == RIGHT and cursor_index < len(event.widget.get())):
            return
        x, y = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}[key]
        info = event.widget.grid_info()
        r, c = info['row'], info['column']
        while True:
            r += x
            c += y
            if r == self.maxRows:
                r = 0
                c = (c + 1) % self.maxCols if self.entries else c
            elif r == -1:
                r = self.maxRows - 1
                c = (c - 1) % self.maxCols if self.entries else c
            elif c == self.maxCols:
                c = 0
                r = (r + 1) % self.maxRows if self.entries else r
            elif c == -1:
                c = self.maxCols - 1
                r = (r - 1) % self.maxRows if self.entries else r
            w = self.findByGrid(r, c)
            if w == event.widget:
                break
            elif type(w) == Entry and w['state'] != DISABLED:
                w.focus()
                w.icursor({LEFT: END, RIGHT: 0, UP: min(cursor_index, len(w.get())), DOWN: min(cursor_index, len(w.get()))}[key])
                break

    def bindMoveFocus(self, entry):
        for key in ['<Up>', '<Down>', '<Left>', '<Right>']:
            entry.bind(key, self.moveFocus)

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
            if len(matrix) == 1 and len(matrix[0]) == 1:
                return MATRIX
            elif len(matrix[0]) == 1:
                return VECTOR
            else:
                return IDENTITY_MATRIX if isIdentity(matrix) else MATRIX
        result = ''
        while True:
            try:
                result = simpledialog.askstring(title = 'Insert', prompt = f'Input Your Matrix in {fromFormat} Form', initialvalue = result)
                if not result:
                    return
                if fromFormat == LATEX:
                    if 'matrix' in result:
                        matrix = [row.split('&') for row in ez.find(result).between('}', '\\end').split('\\\\')]
                        if 'bmatrix' in result:
                            self.setResultType(getResultType(matrix))
                        elif 'vmatrix' in result:
                            self.setResultType(DETERMINANT)
                    else:
                        matrix = [[i] for i in ez.find(result).between('{', '}').split(',')]
                        self.setResultType(VECTOR)
                elif fromFormat == ARRAY:
                    matrix = ez.tryEval(result)
                    if type(matrix) == str:
                        matrix = matrix.replace(',', ' ').split()
                    if matrix == ez.flatten(matrix):
                        matrix = [matrix]
                    else:
                        try:
                            len(matrix)
                            len(matrix[0])
                        except:
                            matrix = [[matrix]]
                    self.setResultType(getResultType(matrix))
                else:
                    raise Exception()
                r = len(matrix)
                c = len(matrix[0])
                self.setRowCol(r, c)
                self.generateEntries(r, c)
                for i in range(r):
                    for j in range(c):
                        setEntry(self.entries[(i, j)], matrix[i][j])
                return
            except:
                messagebox.showerror(title = 'Error', message = 'Invalid Input')
        self.modifyStates()

    def switchResultType(self, move):
        self.setResultType(resultTypeOptions[(resultTypeOptions.index(self.resultType.get()) + move) % len(resultTypeOptions)])

    def switchResultFormat(self, move):
        self.setResultFormat(resultFormatOptions[(resultFormatOptions.index(self.resultFormat.get()) + move) % len(resultFormatOptions)])

    def syncRowCol(self, size):
        self.setRowCol(size, size)
        self.generateEntries(size, size)

    def fillIdentityMatrix(self):
        row = self.getRow()
        col = self.getCol()
        if row != col:
            self.syncRowCol(max(row, col))
        for i, j in self.entries:
            setEntry(self.entries[(i, j)], 1 if i == j else 0)
        self.modifyStates()

    def append(self, position):
        isStart = position == APPEND_START
        result = simpledialog.askstring(title = 'Append', \
                                        prompt = 'Append to the {} of Every Entry'.format('Start' if isStart else 'End'))
        if not result:
            return
        for entry in self.entries.values():
            text = entry.get()
            setEntry(entry, result + text if isStart else text + result)

    def setFindDirection(self, direction):
        if self.findResult:
            self.findIndex = (self.findIndex + (1 if direction == DOWN else -1)) % len(self.findResult)

    def setFoundEntry(self):
        if not self.findResult or self.findIndex == -1: return
        location, start, end = self.findResult[self.findIndex]
        entry = self.entries[location]
        self.master.deiconify()
        entry.focus()
        entry.select_range(start, end)
        entry.icursor(end)\

    def onFind(self, target, direction):
        if not target:
            messagebox.showerror('Error', 'Empty Find!')
            self.currentDialog.show()
            return
        if self.findIndex == -1 or target != self.prevFind:
            self.prevFind = target
            self.findResult = []
            targetLen = len(target)
            for i in range(self.getRow()):
                for j in range(self.getCol()):
                    text = self.entries[(i, j)].get()
                    index = text.find(target)
                    if index > -1:
                        self.findResult.append(((i, j), index, index + targetLen))
            if self.findResult:
                self.findIndex = 0
            else:
                self.findIndex = -1
                messagebox.showerror('Error', 'Not Found')
                self.currentDialog.show()
                return
        self.setFoundEntry()
        self.setFindDirection(direction)

    def onFindClose(self):
        self.findDialog = None

    def find(self, findType):
        if findType == FIND_VALUE:
            self.findIndex = -1
            if self.findDialog:
                self.findDialog.show()
            else:
                self.prevFind = self.master.focus_get().selection_get() or self.prevFind
                self.findDialog = FindDialog()
                self.findDialog.setOnFindListner(self.onFind)
                self.findDialog.setOnCloseListener(self.onFindClose)
                self.findDialog.setFind(self.prevFind)
            self.currentDialog = self.findDialog
        elif findType == FIND_LOCATION:
            result = ''
            while True:
                result = simpledialog.askstring(title = findType, prompt = 'Input Location in the Form of x,y', initialvalue = result)
                if not result:
                    break
                try:
                    x, y = result.replace(' ', '').split(',')
                    entry = self.entries[(int(x) - 1, int(y) - 1)]
                    entry.focus()
                    entry.select_range(0, END)
                    break
                except:
                    messagebox.showerror('Error', 'Invalid Input')
                    continue
                break
        return 'break'

    def onReplace(self, find, replace, direction):
        self.prevReplace = replace
        if self.findIndex == -1:
            self.onFind(find, direction)
        if self.findIndex == -1:
            return
        self.setFindDirection(DOWN if direction == UP else UP)
        entry = self.entries[self.findResult.pop(self.findIndex)[0]]
        if not self.findResult:
            self.findIndex = -1
        setEntry(entry, entry.get().replace(find, replace))
        self.setFindDirection(direction)
        self.modifyStates()

    def onReplaceFind(self, find, replace, direction):
        self.onReplace(find, replace, direction)
        self.setFoundEntry()
        self.setFindDirection(direction)

    def onReplaceAll(self, find, replace):
        self.prevFind = find
        self.prevReplace = replace
        if not find:
            messagebox.showerror('Error', 'Empty Find!')
            self.currentDialog.show()
            return
        for entry in self.entries.values():
            setEntry(entry, entry.get().replace(find, replace))
        self.modifyStates()

    def onReplaceClose(self):
        self.replaceDialog = None

    def replace(self):
        if self.replaceDialog:
            self.replaceDialog.show()
        else:
            self.prevFind = self.master.focus_get().selection_get() or self.prevFind
            self.replaceDialog = ReplaceDialog()
            self.replaceDialog.setOnFindListner(self.onFind)
            self.replaceDialog.setOnReplaceListener(self.onReplace)
            self.replaceDialog.setOnReplaceFindListener(self.onReplaceFind)
            self.replaceDialog.setOnReplaceAllListener(self.onReplaceAll)
            self.replaceDialog.setOnCloseListener(self.onReplaceClose)
            self.replaceDialog.setFind(self.prevFind)
            self.replaceDialog.setReplace(self.prevReplace)
        self.currentDialog = self.replaceDialog
        return 'break'

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
            self.setRowCol(col, row)
            self.generateEntries(col, row)
        for i in range(row):
            for j in range(col):
                setEntry(self.entries[(j, i)], entries[(i, j)])
        self.modifyStates()

    def fillZeroMatrix(self):
        for entry in self.entries.values():
            setEntry(entry, 0)
        self.modifyStates()

    def oneToN(self):
        row = self.getRow()
        col = self.getCol()
        if not row or not col or not self.entries:
            return
        for i in range(row * col):
            setEntry(self.entries[divmod(i, col)], i + 1)
        self.modifyStates()

    def aToZ(self):
        row = self.getRow()
        col = self.getCol()
        if not row or not col or not self.entries:
            return
        ordA = ord('a')
        for i in range(row * col):
            count, char = divmod(i, 26)
            setEntry(self.entries[divmod(i, col)], chr(ordA + char) * (count + 1))
        self.modifyStates()

    def setRandom(self, option):
        '''bound should be either min or max or var'''
        if option == 'var':
            result = self.settings[RANDOM_VAR]
            while True:
                result = simpledialog.askstring(title = 'Set Variable', prompt = f'Input a Variable Name With Length <= {maxRandomVarLength}', \
                                                initialvalue = result)
                if not result:
                    return
                if len(result) > 5:
                    messagebox.showerror('Error', 'Variable too long')
                elif not result[0].isalpha():
                    messagebox.showerror('Error', 'The first letter should be alphabetical')
                else:
                    self.settings[RANDOM_VAR] = result
                    return
        else:
            isMin = option == min
            lower = minValue if isMin else self.settings[RANDOM_MIN] + 1
            upper = self.settings[RANDOM_MAX] - 1 if isMin else maxValue
            result = simpledialog.askinteger(title = 'Set Random', \
                                             prompt = f'Input an Integer between {lower} and {upper}', \
                                             initialvalue = self.settings[RANDOM_MIN if isMin else RANDOM_MAX],
                                             minvalue = lower, maxvalue = upper)
            if result != None:
                self.settings[RANDOM_MIN if isMin else RANDOM_MAX] = result

    def randomFill(self):
        resultType = self.resultType.get()
        row = self.getRow()
        col = self.getCol()
        if not row or not col:
            if resultType == MATRIX:
                if not row:
                    row = randrange(maxSize) + 1
                if not col:
                    col = randrange(maxSize) + 1
            elif resultType == DETERMINANT:
                row = col = randrange(maxSize) + 1
            elif resultType == VECTOR:
                row = randrange(maxSize) + 1
            self.setRowCol(row, col)
            self.generateEntries(row, col)
        option = self.settings[RANDOM_MATRIX_OPTION]
        if option == RANDOM_INT_MATRIX:
            setEntryFunc = lambda entry: setEntry(entry, randrange(self.settings[RANDOM_MIN], self.settings[RANDOM_MAX] + 1))
        elif option == RANDOM_VAR_MATRIX:
            setEntryFunc = lambda entry: setEntry(entry, self.settings[RANDOM_VAR] + '_{' + str(randrange(self.settings[RANDOM_MIN], self.settings[RANDOM_MAX] + 1)) + '}')
        elif option == RANDOM_MULTIVAR_MATRIX:
            setEntryFunc = lambda entry: setEntry(entry, chr(randrange(ord('a'), ord('z') + 1)))
        hasEmpty = False
        for entry in self.entries.values():
            if not entry.get():
                hasEmpty = True
                setEntryFunc(entry)
        if not hasEmpty:
            for entry in self.entries.values():
                setEntryFunc(entry)
        self.modifyStates()

    def randomReorder(self):
        values = [entry.get() for entry in self.entries.values()]
        shuffle(values)
        for i, entry in enumerate(self.entries.values()):
            setEntry(entry, values[i])
        self.modifyStates()

    def toCase(self, case):
        '''Case: LOWER or UPPER'''
        for entry in self.entries.values():
            setEntry(entry, entry.get().lower() if case == LOWER else entry.get().upper())
        self.modifyStates()

    def sort(self):
        row = self.getRow()
        col = self.getCol()
        if not row or not col or not self.entries:
            return 'break'
        varFormat = True
        vars = []
        for i in range(row):
            for j in range(col):
                text = self.entries[(i, j)].get()
                fText = ez.find(text)
                varNumber = ez.tryEval(fText.between('_{', '}'))
                varType = type(varNumber)
                if varType == str:
                    varFormat = False
                    break
                elif varType == int:
                    vars.append((fText.before('_'), varNumber))
        if varFormat:
            values = [f'{var}_' + '{' + str(number) + '}' for var, number in sorted(vars)]
        else:
            try:
                values = sorted(self.collectEntries(row, col))
            except:
                values = sorted(self.collectEntries(row, col, False))
        for i in range(row * col):
            setEntry(self.entries[divmod(i, col)], values[i])
        self.modifyStates()
        return 'break'

    def reverse(self):
        row = self.getRow()
        col = self.getCol()
        if not row or not col or not self.entries:
            return 'break'
        for i in range(row * col // 2):
            r, c = divmod(i, col)
            e1, e2 = self.entries[(r, c)], self.entries[(row - r - 1, col - c - 1)]
            t1, t2 = e2.get(), e1.get()
            setEntry(e1, t1)
            setEntry(e2, t2)
        self.modifyStates()
        return 'break'

    def reshape(self):
        if self.resultType.get() in [DETERMINANT, IDENTITY_MATRIX]:
            messagebox.showerror('Error', 'Invalid Option')
            return
        r = self.getRow()
        c = self.getCol()
        size = r * c
        if ezs.isPrime(size) or (size > maxSize and len(ezs.findAllFactors(size)) == 4):
            x, y = c, r
        else:
            result = ''
            while True:
                result = simpledialog.askstring(title = 'Reshape', prompt = 'Input Shape in the Form of x,y', initialvalue = result)
                if not result:
                    return
                try:
                    x, y = map(int, result.replace(' ', '').split(','))
                    if x * y != size:
                        messagebox.showerror('Error', 'Inconsistent Matrix Size')
                        continue
                    if x == r and y == c:
                        return
                except:
                    messagebox.showerror('Error', 'Invalid Input')
                    continue
                break
        values = [self.entries[(i, j)].get() for i in range(r) for j in range(c)]
        self.setRowCol(x, y)
        self.generateEntries(x, y)
        for i, value in enumerate(values):
            setEntry(self.entries[divmod(i, y)], value)
        self.modifyStates()

    def triangularMatrix(self, mode):
        for i, j in self.entries:
            if i < j if mode == LOWER else i > j:
                setEntry(self.entries[(i, j)], 0)
        self.modifyStates()

    def unitMatrix(self):
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
        shuffle(cols)
        for i in range(size):
            c = cols.pop()
            for j in range(size):
                setEntry(self.entries[(i, j)], 0)
            setEntry(self.entries[(i, c)], 1)
        self.modifyStates()

    def permutationVector(self):
        self.setResultType(VECTOR)
        row = self.getRow()
        if not row:
            row = randrange(maxSize) + 1
        values = list(range(1, row + 1))
        shuffle(values)
        for i, entry in enumerate(self.entries.values()):
            setEntry(entry, values[i])
        self.modifyStates()

    def calculateDet(self):
        size = self.getRow()
        if size != self.getCol() or self.checkEmpty():
            return
        try:
            result = ezs.integer(linalg.det(self.collectEntries(size, size, True, True)))
            # result = ezs.integer(ezs.dc(self.generate()))
            str_result = str(result)
            if self.settings[COPY_CALCULATION_RESULT]:
                ez.copyToClipboard(str_result)
            if self.settings[SHOW_CALCULATION_RESULT]:
                messagebox.showinfo(title = 'Result', message = 'Value: ' + str_result)
            clearOption = self.calculateClearVar.get()
            if clearOption == CLEAR_ENTRIES:
                self.clear(0)
            elif clearOption == CLEAR_ALL:
                self.clear(1)
            return result
        except ValueError:
            messagebox.showerror(title = 'Error', message = 'Numerical Entries Only')

    def setupClearMenu(self, master, variable, command, showResultOption, copyResultOption, label = 'Clear Options'):
        clearMenu = Menu(master = master, tearoff = False)
        showResultVar = BooleanVar(self, value = self.settings.setdefault(showResultOption, True))
        clearMenu.add_checkbutton(label = SHOW_RESULT, variable = showResultVar, \
                                  command = lambda: self.settings.setitem(showResultOption, showResultVar.get()))
        copyResultVar = BooleanVar(self, value = self.settings.setdefault(copyResultOption, True))
        clearMenu.add_checkbutton(label = COPY_RESULT, variable = copyResultVar, \
                                  command = lambda: self.settings.setitem(copyResultOption, copyResultVar.get()))
        clearMenu.add_separator()
        for option in clearOptions:
            clearMenu.add_radiobutton(label = option, value = option, variable = variable, command = command)
        variable.set(self.settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        master.add_cascade(label = label, menu = clearMenu)

    def clear(self, mode = 0):
        '''0 for clear entries, 1 for clear all'''
        if mode >= 0:
            for entry in self.entries.values():
                clearEntry(entry)
        if mode >= 1:
            clearEntry(self.rowEntry)
            clearEntry(self.colEntry)
            for key, entry in self.entries.copy().items():
                entry.grid_forget()
                del self.entries[key]
            self.rowEntry.focus()
        self.modifyStates()

    def onSliderDestroy(self):
        self.sliderDialog = None

    def modifyEntryWidth(self, value):
        self.settings[ENTRY_WIDTH] = value
        for entry in self.entries.values():
            entry['width'] = value

    def adjustEntryWidth(self):
        if self.sliderDialog:
            self.sliderDialog.show()
        else:
            self.sliderDialog = SliderDialog()
            self.sliderDialog.setSliderValue(self.settings[ENTRY_WIDTH])
            self.sliderDialog.setOnSliderChangeListener(self.modifyEntryWidth)
            self.sliderDialog.setOnDestroyListener(self.onSliderDestroy)
        self.currentDialog = self.sliderDialog

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
            vecOption = self.vecOptionVar.get()
            if resultType == VECTOR and vecOption != COLUMN_VECTOR:
                result = ezs.vl(','.join(self.collectEntries(r, c, False)), vecOption == OVERRIGHTARROW)
            else:
                result = ezs.ml(r, c, ' '.join(self.collectEntries(r, c, False)))
        elif resultFormat == ARRAY:
            if resultType == VECTOR and self.settings[ARRAY_VECTOR]:
                result = str(self.collectEntries(r, c))
            else:
                result = ezs.ma(r, c, ' '.join(self.collectEntries(r, c, False)))
        if self.settings[COPY_GENERATION_RESULT]:
            ez.copyToClipboard(result)
        if self.settings[SHOW_GENERATION_RESULT]:
            messagebox.showinfo(title = 'Result', message = result + '\nis Copied to the Clipboard!')
        clearOption = self.settings[GENERATE_CLEAR_OPTION]
        if clearOption == CLEAR_ENTRIES:
            self.clear(0)
        elif clearOption == CLEAR_ALL:
            self.clear(1)
        return result

    def collectEntries(self, r, c, evaluate = True, nested = False):
        entries = []
        for i in range(r):
            if nested:
                lst = []
            for j in range(c):
                text = self.entries[(i, j)].get()
                if evaluate: text = ez.tryEval(text)
                if nested: lst.append(text)
                else: entries.append(text)
            if nested:
                entries.append(lst)
        return entries

    def undo(self):
        if self.stateIndex == 0:
            return
        self.stateIndex -= 1
        self.resumeState()

    def redo(self):
        if self.stateIndex == len(self.states) - 1:
            return
        self.stateIndex += 1
        self.resumeState()

    def resumeState(self):
        resultType, entries, focus = self.states[self.stateIndex]
        r = len(entries)
        c = len(entries[0])
        self.setRowCol(r, c)
        self.generateEntries(r, c)
        self.setResultType(resultType)
        for i, row in enumerate(entries):
            for j, entry in enumerate(row):
                setEntry(self.entries[(i, j)], entry)
        if focus == 0:
            self.rowEntry.focus()
        elif focus == 2:
            self.colEntry.focus()
        else:
            focus -= 3
            self.entries[divmod(focus, c)].focus()

    def modifyStates(self):
        row = self.getRow()
        col = self.getCol()
        if not row and not col:
            return
        state = (self.resultType.get(), \
                 self.collectEntries(row, col, False, True), \
                 self.getFocusEntry())
        if self.states and state[:-1] == self.states[self.stateIndex][:-1]:
            return
        self.states = self.states[:self.stateIndex + 1] + [state]
        self.stateIndex = len(self.states) - 1

    def getFocusEntry(self):
        try: return int(ez.find(str(self.master.focus_get())).after('.!generator.!entry') or 0)
        except: return 0

    def onDestroy(self):
        if self.currentDialog:
            try: self.currentDialog.withdraw()
            except: pass

root = Tk()
app = Generator(root)
app.pack()
root.title('Matrix Generator')
ez.py2pyw(__file__)
root.mainloop()
