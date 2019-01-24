from tkinter import *
from tkinter import messagebox, simpledialog
from eztk import setEntry, clearEntry
from random import randrange, shuffle
import ez, ezs, os
from Dialogs import *

## Constant Variables
maxSize = 25
maxRandomVarLength = 10

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
COLUMN_VECTOR, OVERRIGHTARROW = 'Column Vector', 'OverRightArrow'
vectorOptions = [COLUMN_VECTOR, OVERRIGHTARROW,  VECTOR]
ARRAY_OPTION = 'ArrayOption'
NORMAL_ARRAY, NUMPY_ARRAY, NP_ARRAY = 'Normal Array', 'Numpy Array', 'Np Array'
arrayOptions = [NORMAL_ARRAY, NUMPY_ARRAY, NP_ARRAY]
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
APPEND_INDEX = 'Append Index'
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
NEWLINE_ENDING = 'Newline Row Ending'
LATEX_NEWLINE = 'LaTexNewline'
ARRAY_NEWLINE = 'ArrayNewline'
UNKNOWN_MATRIX = 'UnknownMatrix'

## Settings
settingOptions = [RESULT_TYPE, RESULT_FORMAT, REMEMBER_SIZE, VECTOR_OPTION, RANDOM_VAR, RANDOM_MIN, RANDOM_MAX, RANDOM_MATRIX_OPTION, ENTRY_WIDTH, \
                  SHOW_GENERATION_RESULT, SHOW_CALCULATION_RESULT, COPY_GENERATION_RESULT, COPY_CALCULATION_RESULT, GENERATE_CLEAR_OPTION, CALCULATE_CLEAR_OPTION]

## Shortcuts
shortcuts = { GENERATE: 'Enter/Return', ADD: 'Ctrl+=', ZERO_MATRIX: 'Ctrl+0', IDENTITY_MATRIX: 'Ctrl+I', RANDOM_MATRIX: 'Ctrl+R', UNIT_MATRIX: 'Ctrl+U', EXIT: 'Ctrl+W', \
              MULTIPLY: 'Ctrl+M', PERMUTATION_MATRIX: 'Ctrl+P', PERMUTATION_VECTOR: 'Ctrl+P', FIND_VALUE: 'Ctrl+F', REPLACE: 'Ctrl+H', REDO: 'Ctrl+Y', UNDO: 'Ctrl+Z', \
              CLEAR_ALL: 'Ctrl+Shift+A', CALCULATE: 'Ctrl+Shift+C', CLEAR_ENTRIES: 'Ctrl+Shift+E', FIND_LOCATION: 'Ctrl+Shift+F', APPEND_INDEX: 'Ctrl+Shift+I', LOWER_TRIANGULAR: 'Ctrl+Shift+L', RANDOM_REORDER: 'Ctrl+Shift+R', UPPER_TRIANGULAR: 'Ctrl+Shift+U', \
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
        self.entries = {}
        self.stateIndex = 0
        self.states = [] ## (resultType, entries, focusEntry)
        ## Find Dialog
        self.findResult = []
        self.prevFind = ''
        self.findIndex = -1
        self.findDirection = DOWN
        self.currentEntry = None
        ## Replace Dialog
        self.prevReplace = ''
        self.replaceDirection = DOWN

        ## Generate Menus
        self.menu = Menu(self)
        ## Result Menu
        self.resultMenu = Menu(self)
        ## Result Type Menu
        self.matMenu = Menu(self)
        self.matMenu.add_command(label = IDENTITY_MATRIX, accelerator = shortcuts[IDENTITY_MATRIX], command = self.identityMatrix)
        self.matMenu.add_command(label = PERMUTATION_MATRIX, accelerator = shortcuts[PERMUTATION_MATRIX], command = self.permutationMatrix)
        self.matMenu.add_command(label = ZERO_MATRIX, accelerator = shortcuts[ZERO_MATRIX], command = self.zeroMatrix)
        self.matMenu.add_command(label = UNIT_MATRIX, accelerator = shortcuts[UNIT_MATRIX], command = self.unitMatrix)
        self.matMenu.add_separator()
        self.matMenu.add_command(label = 'Unknown Matrix', command = self.unknownMatrix)
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
        ## Result Format Menu
        self.latexMenu = Menu(self)
        self.latexNewlineVar = BooleanVar(self, value = self.settings.setdefault(LATEX_NEWLINE, False))
        self.latexMenu.add_checkbutton(label = NEWLINE_ENDING, variable = self.latexNewlineVar, \
                                       command = lambda: self.settings.setitem(LATEX_NEWLINE, self.latexNewlineVar.get()))
        self.arrayMenu = Menu(self)
        self.arrayNewlineVar = BooleanVar(self, value = self.settings.setdefault(ARRAY_NEWLINE, False))
        self.arrayMenu.add_checkbutton(label = NEWLINE_ENDING, variable = self.arrayNewlineVar, \
                                       command = lambda: self.settings.setitem(ARRAY_NEWLINE, self.arrayNewlineVar.get()))
        self.arrayMenu.add_separator()
        self.arrayOptionVar = StringVar(self)
        for option in arrayOptions:
            self.arrayMenu.add_radiobutton(label = option, variable = self.arrayOptionVar, \
                                           command = lambda: self.settings.setitem(ARRAY_OPTION, self.arrayOptionVar.get()))
        self.arrayOptionVar.set(self.settings.setdefault(ARRAY_OPTION, NORMAL_ARRAY))
        for name, menu in zip(resultFormatOptions, [self.latexMenu, self.arrayMenu]):
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
        self.insertMenu.add_command(label = APPEND_INDEX, accelerator = shortcuts[APPEND_INDEX], command = self.appendIndex)
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
        self.randomMenu.add_command(label = 'Set Random Range', command = self.setRandomRange)
        self.randomMenu.add_command(label = 'Set Random Var', command = self.setRandomVar)
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
        ## Help Menu
        self.helpMenu = Menu(self)
        self.helpMenu.add_command(label = 'Adjust Entry Width', command = self.adjustEntryWidth)
        self.rememberSizeVar = BooleanVar(self, value = self.settings.setdefault(REMEMBER_SIZE, (-1, -1)) != (-1, -1))
        self.helpMenu.add_checkbutton(label = 'Remember Size', variable = self.rememberSizeVar, \
                                          command = lambda: self.settings.setitem(REMEMBER_SIZE, (self.getRow(), self.getCol()) if self.rememberSizeVar.get() else (-1, -1)))
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label = 'Other Keyboard Shortcuts', command = lambda: messagebox.showinfo(title = 'Shortcuts', message = otherShortcuts))
        for name, menu in zip(['Result', 'Edit', 'Insert', 'Modify', 'Generate', 'Help'], [self.resultMenu, self.editMenu, self.insertMenu, self.modifyMenu, self.generateMenu, self.helpMenu]):
            menu['tearoff'] = False
            self.menu.add_cascade(label = name, menu = menu)
        self.master.config(menu = self.menu)

        ## Generate Widgets
        self.topFrame = Frame(self)
        self.entryFrame = Frame(self)
        self.resultTypeLabel = Label(self.topFrame, text = 'Type:')
        self.resultType = StringVar(self)
        self.resultTypeDropdown = OptionMenu(self.topFrame, self.resultType, *resultTypeOptions, command = lambda event: self.onResultTypeChange())
        self.resultFormatLabel = Label(self.topFrame, text = 'Format:')
        self.resultFormat = StringVar(self)
        self.resultFormatDropdown = OptionMenu(self.topFrame, self.resultFormat, *resultFormatOptions, command = lambda event: self.onResultFormatChange())

        self.rowLabel = Label(self.topFrame, text = 'Rows:')
        self.rowEntry = Entry(self.topFrame)
        self.colLabel = Label(self.topFrame, text = 'Columns:')
        self.colEntry = Entry(self.topFrame)
        self.sizeEntries = [self.rowEntry, self.colEntry]
        self.rowEntry.focus()

        ## Place Widgets
        for i, w in enumerate([self.resultTypeLabel, self.resultTypeDropdown, self.resultFormatLabel, self.resultFormatDropdown]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)
        self.topFrame.pack(side = TOP, anchor = W)
        self.entryFrame.pack(side = BOTTOM, anchor = W)

        for entry in self.sizeEntries:
            self.bindMoveFocus(entry)
            entry.bind('<KeyRelease>', self.onRowColChange)
            bindtags = entry.bindtags()
            entry.bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))
        if self.rememberSizeVar.get():
            r, c = self.settings[REMEMBER_SIZE]
            if r > 0:
                setEntry(self.rowEntry, r)
            if c > 0:
                setEntry(self.colEntry, c)
            self.generateEntries(r, c)

        ## Bind
        self.master.bind('<Destroy>', lambda event: self.onDestroy())
        self.master.bind('<Return>', lambda event: self.generate())
        self.master.bind('<Control-0>', lambda event: self.zeroMatrix())
        self.master.bind('<Control-f>', lambda event: self.find(FIND_VALUE))
        self.master.bind('<Control-h>', lambda event: self.replace())
        self.master.bind('<Control-i>', lambda event: self.identityMatrix())
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
        self.master.bind('<Control-I>', lambda event: self.appendIndex())
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
        self.setResultType(self.settings.setdefault(RESULT_TYPE, MATRIX))
        self.setResultFormat(self.settings.setdefault(RESULT_FORMAT, LATEX))
        self.settings.setdefault(RANDOM_MIN, 1)
        self.settings.setdefault(RANDOM_MAX, maxSize)
        self.settings.setdefault(RANDOM_VAR, defaultVar)
        self.settings.setdefault(UNKNOWN_MATRIX, ('a', 'i', 'j'))
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

    def getRowCol(self):
        return (self.getRow(), self.getCol())

    def syncRowCol(self, size):
        self.setRowCol(size, size)
        self.generateEntries(size, size)

    def setResultType(self, resultType):
        if self.resultType.get() == resultType:
            return
        self.resultType.set(resultType)
        self.onResultTypeChange()

    def onResultTypeChange(self):
        resultType = self.resultType.get()
        self.settings[RESULT_TYPE] = resultType
        row, col = self.getRowCol()
        if resultType == MATRIX:
            self.colEntry['state'] = NORMAL
        elif resultType == DETERMINANT:
            self.colEntry['state'] = NORMAL
            size = max(row, col)
            if size:
                row = col = size
                self.syncRowCol(size)
        elif resultType == VECTOR:
            entries = []
            if self.entries and row == 1 and col > 1:
                entries = self.collectEntries(row, col, False)
                row = col
                self.setRow(row)
            self.setCol(1)
            self.colEntry['state'] = DISABLED
            if row:
                self.generateEntries(row, 1)
            if entries:
                for i in range(1, col):
                    setEntry(self.entries[(i, 0)], entries[i])

    def setResultFormat(self, resultFormat):
        if self.resultFormat.get() == resultFormat:
            return
        self.resultFormat.set(resultFormat)
        self.onResultFormatChange()

    def onResultFormatChange(self):
        self.settings[RESULT_FORMAT] = self.resultFormat.get()

    def onRowColChange(self, event):
        if event.keysym in directions:
            return
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
        r, c = self.getRowCol()
        if resultType == DETERMINANT:
            size = r if text == str(r) else c
            r = c = size
            self.syncRowCol(size)
        self.generateEntries(r, c)
        if self.rememberSizeVar.get():
            self.settings[REMEMBER_SIZE] = (r, c)
        self.modifyStates()

    def generateEntries(self, row, col):
        if row < 1 or col < 1:
            return
        for i in range(row):
            for j in range(col):
                if (i, j) in self.entries:
                    continue
                entry = Entry(self.entryFrame, width = self.settings.setdefault(ENTRY_WIDTH, 20))
                self.bindMoveFocus(entry)
                entry.bind('<KeyRelease>', lambda event: self.onEntryChange())
                bindtags = entry.bindtags()
                entry.bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))
                entry.grid(row = i, column = j, sticky = NSEW)
                self.entries[(i, j)] = entry
        for i, j in self.entries.copy():
            if i not in range(row) or j not in range(col):
                self.entries[(i, j)].grid_forget()
                del self.entries[(i, j)]

    def onEntryChange(self):
        self.modifyStates()

    def bindMoveFocus(self, entry):
        for key in ['<Up>', '<Down>', '<Left>', '<Right>']:
            entry.bind(key, self.moveFocus)

    def moveFocus(self, event):
        key = event.keysym
        entry = event.widget
        cursorIndex = entry.index(INSERT)
        isEnd = cursorIndex == len(entry.get())
        if (key == LEFT and cursorIndex > 0) or \
           (key == RIGHT and not isEnd):
            return
        row, col = self.getRowCol()
        if entry in self.sizeEntries:
            if key in [LEFT, RIGHT]:
                fEntry = self.sizeEntries[entry == self.rowEntry]
            else:
                # check empty
                if self.entries:
                    fEntry = self.entries[(row - 1 if key == UP else 0, 0 if entry == self.rowEntry else col - 1)]
                else:
                    return
        else:
            info = entry.grid_info()
            r, c = info['row'], info['column']
            if c in [0, col - 1] and ((key == UP and r == 0) or (key == DOWN and r == row - 1)):
                fEntry = self.sizeEntries[c != 0]
            else:
                x, y = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}[key]
                r = (r + x) % row
                c = (c + y) % col
                fEntry = self.entries[(r, c)]
        fEntry.focus()
        if key in [UP, DOWN]:
            fEntry.icursor(END if isEnd else min(len(fEntry.get()), cursorIndex))
        else:
            fEntry.icursor(END if key == LEFT else 0)
        return

    def checkEmpty(self):
        result = None
        for entry in [self.rowEntry, self.colEntry]:
            if not entry.get():
                messagebox.showerror(title = 'Error', message = 'Empty Size')
                return result
        asked = False
        for entry in self.entries.values():
            if entry.get():
                continue
            if not asked:
                result = messagebox.askyesnocancel(title = 'Warning', message = 'Not All Entries are Filled\nDo you want to fill them with zeros?')
                asked = True
            if result:
                entry.insert(0, 0)
            elif result == None:
                break
        return result

    def generate(self):
        if self.checkEmpty() == None:
            return
        result = ''
        r, c = self.getRowCol()
        resultType = self.resultType.get()
        resultFormat = self.resultFormat.get()
        if resultFormat == LATEX:
            vecOption = self.vecOptionVar.get()
            if resultType == VECTOR and vecOption != COLUMN_VECTOR:
                result = ezs.vl(','.join(self.collectEntries(r, c, False)), vecOption == OVERRIGHTARROW)
            else:
                result = ezs.ml(r, c, ' '.join(self.collectEntries(r, c, False)), resultType == DETERMINANT, self.settings[LATEX_NEWLINE])
        elif resultFormat == ARRAY:
            if resultType == VECTOR and self.settings[ARRAY_VECTOR]:
                result = str(self.collectEntries(r, c))
            else:
                result = str(self.collectEntries(r, c, True, True))
                if self.settings[ARRAY_NEWLINE]:
                    result = result.replace('],', '],\n')
            arrayOption = self.settings[ARRAY_OPTION]
            if arrayOption != NORMAL_ARRAY:
                prefix = 'np' if arrayOption == NP_ARRAY else 'numpy'
                result = f'{prefix}.array({result})'
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

    def switchResultType(self, move):
        self.setResultType(resultTypeOptions[(resultTypeOptions.index(self.resultType.get()) + move) % len(resultTypeOptions)])

    def switchResultFormat(self, move):
        self.setResultFormat(resultFormatOptions[(resultFormatOptions.index(self.resultFormat.get()) + move) % len(resultFormatOptions)])

    def add(self):
        fEntry = self.getFocusEntry()
        result = simpledialog.askstring(title = 'Multiply', prompt = 'Add to Each Entry')
        fEntry.focus()
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
        fEntry = self.getFocusEntry()
        result = ezs.integer(ez.tryEval(simpledialog.askstring(title = 'Multiply', prompt = 'Multiply Each Entry By')))
        fEntry.focus()
        if result == None or result == 1:
            return
        if result == 0:
            self.zeroMatrix()
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

    def insert(self, fromFormat):
        '''fromFormat can only be LaTeX or Array'''
        def getResultType(matrix):
            if len(matrix) == 1 and len(matrix[0]) == 1:
                return MATRIX
            elif len(matrix[0]) == 1:
                return VECTOR
            return MATRIX
        result = ''
        fEntry = self.getFocusEntry()
        while True:
            try:
                result = simpledialog.askstring(title = 'Insert', prompt = f'Input Your Matrix in {fromFormat} Form', initialvalue = result)
                fEntry.focus()
                if not result:
                    break
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
                if (r * c > maxSize ** 2):
                    messagebox.showerror(title = 'Error', message = 'Matrix Too Large')
                    break
                self.setRowCol(r, c)
                self.generateEntries(r, c)
                for i in range(r):
                    for j in range(c):
                        setEntry(self.entries[(i, j)], matrix[i][j])
                break
            except:
                messagebox.showerror(title = 'Error', message = 'Invalid Input')
        fEntry.focus()
        if result:
            self.modifyStates()

    def appendIndex(self):
        isLatex = self.resultFormat.get() == LATEX
        for i in range(self.getRow()):
            for j in range(self.getCol()):
                text = f'{i + 1}{j + 1}'
                self.entries[(i, j)].insert(END, '_{%s}' % text if isLatex else text)

    def identityMatrix(self):
        row, col = self.getRowCol()
        if row != col:
            self.syncRowCol(max(row, col))
        for i, j in self.entries:
            setEntry(self.entries[(i, j)], 1 if i == j else 0)
        self.modifyStates()

    def append(self, position):
        isStart = position == APPEND_START
        fEntry = self.getFocusEntry()
        result = simpledialog.askstring(title = 'Append', \
                                        prompt = 'Append to the {} of Every Entry'.format('Start' if isStart else 'End'))
        fEntry.focus()
        if not result: return
        for entry in self.entries.values():
            entry.insert(0 if isStart else END, result)

    def setFindDirection(self, direction):
        if self.findResult:
            self.findIndex = (self.findIndex + (1 if direction == DOWN else -1)) % len(self.findResult)

    def setFoundEntry(self):
        if not self.findResult or self.findIndex == -1: return
        location, start, end = self.findResult[self.findIndex]
        entry = self.entries[location]
        entry.focus_set()
        entry.select_range(start, end)
        entry.icursor(end)

    def onFind(self, dialog, target, direction, findNext = True):
        if not target:
            messagebox.showerror('Error', 'Empty Find!')
            return
        if self.findIndex == -1 or target != self.prevFind:
            self.prevFind = target
            self.findResult = []
            targetLen = len(target)
            r, c = self.getRowCol()
            for i in range(r):
                for j in range(c):
                    text = self.entries[(i, j)].get()
                    for index in ez.find(text).all(target):
                        self.findResult.append(((i, j), index, index + targetLen))
                        if self.currentEntry and divmod(self.currentEntry[1], c) == (i, j) and self.currentEntry[2] == index:
                            self.findIndex = len(self.findResult) - 1
            if self.findResult:
                if self.findIndex < 0:
                    self.findIndex = 0
            else:
                self.findIndex = -1
                messagebox.showerror('Error', 'Not Found')
                return
        self.setFoundEntry()
        if findNext:
            self.setFindDirection(direction)

    def onFindDirectionChange(self, dialog, direction):
        self.findDirection = direction

    def find(self, findType):
        if findType == FIND_VALUE:
            self.findIndex = -1
            try:
                target = self.master.focus_get().selection_get()
                self.currentEntry = self.getFocusEntryIndex()
                if not self.currentEntry[0]: self.currentEntry = None
            except:
                target = self.prevFind
            dialog = FindDialog(self)
            dialog.setOnFindListner(self.onFind)
            dialog.setOnDirectionChangeListener(self.onFindDirectionChange)
            dialog.setFind(target)
            dialog.setDirection(self.findDirection)
            self.wait_window(dialog)
        elif findType == FIND_LOCATION:
            result = ''
            fEntry = self.getFocusEntry()
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
            fEntry.focus()
        return 'break'

    def onReplace(self, dialog, find, replace, direction):
        self.prevReplace = replace
        if self.findIndex == -1 or self.prevFind != find:
            self.onFind(find, direction, False)
        if self.findIndex == -1 or not self.findResult:
            return
        location, start, end = self.findResult[self.findIndex]
        entry = self.entries[location]
        text = entry.get()
        setEntry(entry, text[:start] + replace + text[end:])
        self.setFoundEntry()
        self.findResult.pop(self.findIndex)
        difference = len(replace) - len(find)
        for i, (fLocation, fStart, fEnd) in enumerate(self.findResult[self.findIndex:]):
            if location == fLocation:
                self.findResult[self.findIndex + i] = (fLocation, fStart + difference, fEnd + difference)
            else:
                break
        if self.findResult:
            if direction == UP:
                self.findIndex = (self.findIndex - 1) % len(self.findResult)
        else:
            self.findIndex = -1
        self.modifyStates()

    def onReplaceFind(self, dialog, find, replace, direction):
        self.onReplace(dialog, find, replace, direction)
        self.setFoundEntry()

    def onReplaceAll(self, dialog, find, replace):
        self.prevFind = find
        self.prevReplace = replace
        if not find:
            messagebox.showerror('Error', 'Empty Find!')
            return
        for entry in self.entries.values():
            setEntry(entry, entry.get().replace(find, replace))
        self.modifyStates()

    def onReplaceDirectionChange(self, dialog, direction):
        self.replaceDirection = direction

    def replace(self):
        try:
            target = self.master.focus_get().selection_get()
            self.currentEntry = self.getFocusEntryIndex()
            if not self.currentEntry[0]: self.currentEntry = None
        except:
            target = self.prevFind
        dialog = ReplaceDialog(self)
        dialog.setOnFindListner(self.onFind)
        dialog.setOnReplaceListener(self.onReplace)
        dialog.setOnReplaceFindListener(self.onReplaceFind)
        dialog.setOnReplaceAllListener(self.onReplaceAll)
        dialog.setOnDirectionChangeListener(self.onReplaceDirectionChange)
        dialog.setFind(target)
        dialog.setReplace(self.prevReplace)
        dialog.setDirection(self.replaceDirection)
        self.wait_window(dialog)
        return 'break'

    def transpose(self):
        resultType = self.resultType.get()
        if resultType not in [MATRIX, DETERMINANT, VECTOR]:
            return
        row, col = self.getRow()
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

    def zeroMatrix(self):
        for entry in self.entries.values():
            setEntry(entry, 0)
        self.modifyStates()

    def oneToN(self):
        row, col = self.getRowCol()
        if not row or not col or not self.entries:
            return
        for i in range(row * col):
            setEntry(self.entries[divmod(i, col)], i + 1)
        self.modifyStates()

    def aToZ(self):
        row, col = self.getRowCol()
        if not row or not col or not self.entries:
            return
        ordA = ord('a')
        for i in range(row * col):
            count, char = divmod(i, 26)
            setEntry(self.entries[divmod(i, col)], chr(ordA + char) * (count + 1))
        self.modifyStates()

    def setRandomVar(self):
        result = self.settings[RANDOM_VAR]
        fEntry = self.getFocusEntry()
        while True:
            result = simpledialog.askstring(title = 'Set Variable', \
                                            prompt = f'Input a Variable Name With Length <= {maxRandomVarLength}', \
                                            initialvalue = result)
            if not result:
                break
            if len(result) > maxRandomVarLength:
                messagebox.showerror('Error', 'Variable too long')
            elif not result[0].isalpha():
                messagebox.showerror('Error', 'The first letter should be alphabetical')
            else:
                self.settings[RANDOM_VAR] = result
                break
        fEntry.focus()

    def onConfirmRange(self, dialog, minValue, maxValue):
        try:
            minValue = int(minValue)
            maxValue = int(maxValue)
            if minValue > maxValue:
                raise Exception()
            self.settings[RANDOM_MIN] = minValue
            self.settings[RANDOM_MAX] = maxValue
        except:
            messagebox.showerror('Error', 'Invalid Input')
            return

    def setRandomRange(self):
        dialog = RangeDialog(self)
        dialog.setMinMax(self.settings[RANDOM_MIN], self.settings[RANDOM_MAX])
        dialog.setOnConfirmListener(self.onConfirmRange)
        self.wait_window(dialog)

    def randomFill(self):
        resultType = self.resultType.get()
        row, col = self.getRowCol()
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
            isLatex = self.resultFormat.get() == LATEX
            setEntryFunc = lambda entry: setEntry(entry, self.settings[RANDOM_VAR] + ('_{%s}' % randrange(self.settings[RANDOM_MIN], self.settings[RANDOM_MAX] + 1) if isLatex else str(randrange(self.settings[RANDOM_MIN], self.settings[RANDOM_MAX] + 1))))
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
        row, col = self.getRowCol()
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
            try: values = sorted(self.collectEntries(row, col))
            except: values = sorted(self.collectEntries(row, col, False))
        for i in range(row * col):
            setEntry(self.entries[divmod(i, col)], values[i])
        self.modifyStates()
        return 'break'

    def reverse(self):
        row, col = self.getRowCol()
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
        r, c = self.getRowCol()
        size = r * c
        if size <= 1:
            return 'break'
        if ezs.isPrime(size) or (size > maxSize and len(ezs.findAllFactors(size)) == 4):
            x, y = c, r
        else:
            result = ''
            fEntry = self.getFocusEntry()
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
            fEntry.focus()
        values = [self.entries[(i, j)].get() for i in range(r) for j in range(c)]
        self.setResultType(VECTOR if x > 1 and y == 1 else MATRIX)
        self.setRowCol(x, y)
        self.generateEntries(x, y)
        for i, value in enumerate(values):
            setEntry(self.entries[divmod(i, y)], value)
        self.modifyStates()
        return 'break'

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
        row, col = self.getRowCol()
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

    def unknownMatrix(self):
        dialog = UnknownMatrix(self)
        var, row, col = self.settings[UNKNOWN_MATRIX]
        dialog.setData(var, row, col)
        dialog.setOnCopyListener(lambda dialog, result: ez.copyToClipboard(result))
        dialog.setOnCloseListener(lambda dialog, var, row, col: self.settings.setitem(UNKNOWN_MATRIX, (var, row, col)) )
        self.wait_window(dialog)

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
        if size != self.getCol() or self.checkEmpty() == None:
            return
        try:
            try:
                from numpy import linalg
                result = ezs.integer(linalg.det(self.collectEntries(size, size, True, True)))
            except ModuleNotFoundError:
                result = ezs.integer(ezs.dc(self.generate()))
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

    def modifyEntryWidth(self, dialog, value):
        self.settings[ENTRY_WIDTH] = value
        for entry in self.entries.values():
            entry['width'] = value

    def adjustEntryWidth(self):
        dialog = SliderDialog(self, 20)
        dialog.setSliderValue(self.settings[ENTRY_WIDTH])
        dialog.setOnSliderChangeListener(self.modifyEntryWidth)
        self.wait_window(dialog)

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
        entry = self.getLastFocusEntry(c)
        entry.focus()
        entry.icursor(focus[2])

    def modifyStates(self):
        row, col = self.getRowCol()
        if not row and not col:
            return
        state = (self.resultType.get(), \
                 self.collectEntries(row, col, False, True), \
                 self.getFocusEntryIndex())
        if self.states and state[:-1] == self.states[self.stateIndex][:-1]:
            return
        self.states = self.states[:self.stateIndex + 1] + [state]
        self.stateIndex = len(self.states) - 1

    def getFocusEntry(self):
        try: return self.master.focus_get()
        except: return self.rowEntry

    def getFocusEntryIndex(self):
        try:
            entry = self.master.focus_get()
            f = ez.find(str(entry))
            return (int(f.between('frame', '.') or 1) - 1, int(f.after('.!entry') or 1) - 1, entry.index(ANCHOR) if entry.selection_present() else entry.index(INSERT))
        except:
            return (0, 0, END)

    def getLastFocusEntry(self, col = None):
        focus = self.states[self.stateIndex][2]
        if focus[:2] == (0, 0):
            return self.rowEntry
        elif focus[:2] == (0, 1):
            return self.colEntry
        else:
            return self.entries[divmod(focus[1], col or self.getCol())]

    def onDestroy(self):
        pass

root = Tk()
app = Generator(root)
app.pack()
root.title('Matrix Generator')
ez.py2pyw(__file__)
root.mainloop()
