from tkinter import *
from tkinter import messagebox, simpledialog
from eztk import setEntry, clearEntry
from random import randrange, shuffle, randint
import ez, ezs, os
from dialog import *
from constants import *

settings = ez.Settings(__file__)
settings.setSettingOptions(settingOptions)

class Generator(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        ## init variables
        self.row = 0
        self.col = 0
        self.entries = {}
        self.entryLabels = {}
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
        ## Insert Menu
        self.insertMenu = Menu(self)
        self.insertMenu.add_command(label = APPEND_START, accelerator = shortcuts[APPEND_START], command = lambda: self.append(APPEND_START))
        self.insertMenu.add_command(label = APPEND_END, accelerator = shortcuts[APPEND_END], command = lambda: self.append(APPEND_END))
        self.insertMenu.add_command(label = APPEND_INDEX, accelerator = shortcuts[APPEND_INDEX], command = self.appendIndex)
        self.insertMenu.add_separator()
        self.insertMenu.add_command(label = FILL_ROW, accelerator = shortcuts[FILL_ROW], command = lambda: self.fillRC(FILL_ROW))
        self.insertMenu.add_command(label = FILL_COLUMN, accelerator = shortcuts[FILL_COLUMN], command = lambda: self.fillRC(FILL_COLUMN))
        self.insertMenu.add_separator()
        self.insertMenu.add_command(label = FROM_LATEX, accelerator = shortcuts[FROM_LATEX], command = lambda: self.insert(LATEX))
        self.insertMenu.add_command(label = FROM_ARRAY, accelerator = shortcuts[FROM_ARRAY], command = lambda: self.insert(ARRAY))
        self.insertMenu.add_separator()
        self.insertMenu.add_command(label = ONE_TO_N, accelerator = shortcuts[ONE_TO_N], command = self.oneToN)
        self.insertMenu.add_command(label = A_TO_Z, accelerator = shortcuts[A_TO_Z], command = self.aToZ)
        self.insertMenu.add_command(label = 'Fibonacci', command = self.fibonacci)
        self.insertMenu.add_separator()
        self.randomMenu = Menu(self, tearoff = False)
        self.randomMenu.add_command(label = RANDOM_MATRIX, accelerator = shortcuts[RANDOM_MATRIX], command = self.randomFill)
        self.randomMenu.add_command(label = RANDOM_REORDER, accelerator = shortcuts[RANDOM_REORDER], command = self.randomReorder)
        self.randomMenu.add_separator()
        self.randomMatrixOption = StringVar(self)
        for option in randomMatrixOptions:
            self.randomMenu.add_radiobutton(label = option, variable = self.randomMatrixOption, \
                                            command = lambda: settings.set(RANDOM_MATRIX_OPTION, self.randomMatrixOption.get()))
        self.randomMatrixOption.set(settings.setdefault(RANDOM_MATRIX_OPTION, RANDOM_INT_MATRIX))
        self.randomMenu.add_separator()
        self.randomMenu.add_command(label = 'Set Random Range', command = self.setRandomRange)
        self.randomMenu.add_command(label = 'Set Random Var', command = self.setRandomVar)
        self.randomMenu.add_separator()
        self.uniqueRandomVar = BooleanVar(self, value = settings.setdefault(UNIQUE_RANDOM, True))
        self.randomMenu.add_checkbutton(label = 'Unique Randomness', variable = self.uniqueRandomVar, \
                                        command = lambda: settings.set(UNIQUE_RANDOM, self.uniqueRandomVar.get()))
        self.insertMenu.add_cascade(label = RANDOM, menu = self.randomMenu)
        ## Edit Menu
        self.editMenu = Menu(self)
        self.editMenu.add_command(label = UNDO, accelerator = shortcuts[UNDO], command = self.undo)
        self.editMenu.add_command(label = REDO, accelerator = shortcuts[REDO], command = self.redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = FIND_VALUE, accelerator = shortcuts[FIND_VALUE], command = lambda: self.find(FIND_VALUE))
        self.editMenu.add_command(label = FIND_LOCATION, accelerator = shortcuts[FIND_LOCATION], command = lambda: self.find(FIND_LOCATION))
        self.editMenu.add_command(label = REPLACE, accelerator = shortcuts[REPLACE], command = self.replace)
        self.editMenu.add_separator()
        self.editMenu.add_command(label = SWITCH_ROWS, accelerator = shortcuts[SWITCH_ROWS], command = lambda: self.switch(ROWS))
        self.editMenu.add_command(label = SWITCH_COLUMNS, accelerator = shortcuts[SWITCH_COLUMNS], command = lambda: self.switch(COLS))
        self.editMenu.add_command(label = 'Copy ' + ROW, command = lambda: self.copyRC(ROW))
        self.editMenu.add_command(label = 'Copy ' + COL, command = lambda: self.copyRC(COL))
        self.editMenu.add_command(label = 'Duplicate ' + ROWS, command = lambda: self.duplicateRC(ROWS))
        self.editMenu.add_command(label = 'Duplicate ' + COLS, command = lambda: self.duplicateRC(COLS))
        self.editMenu.add_separator()
        self.editMenu.add_command(label = CLEAR_ZEROS, accelerator = shortcuts[CLEAR_ZEROS], command = lambda: self.clear(0))
        self.editMenu.add_command(label = CLEAR_ENTRIES, accelerator = shortcuts[CLEAR_ENTRIES], command = lambda: self.clear(1))
        self.editMenu.add_command(label = CLEAR_ALL, accelerator = shortcuts[CLEAR_ALL], command = lambda: self.clear(2))
        ## Modify Menu
        self.modifyMenu = Menu(self)
        self.modifyMenu.add_command(label = ADD, accelerator = shortcuts[ADD], command = self.add)
        self.modifyMenu.add_command(label = MULTIPLY, accelerator = shortcuts[MULTIPLY], command = self.multiply)
        self.modifyMenu.add_separator()
        self.modifyMenu.add_command(label = TRANSPOSE, accelerator = shortcuts[TRANSPOSE], command = self.transpose)
        self.modifyMenu.add_command(label = RESHAPE, command = self.reshape)
        self.modifyMenu.add_separator()
        self.modifyMenu.add_command(label = LOWER_TRIANGULAR, accelerator = shortcuts[LOWER_TRIANGULAR], command = lambda: self.triangularMatrix(LOWER))
        self.modifyMenu.add_command(label = UPPER_TRIANGULAR, accelerator = shortcuts[UPPER_TRIANGULAR], command = lambda: self.triangularMatrix(UPPER))
        self.modifyMenu.add_separator()
        self.sortMenu = Menu(self, tearoff = False)
        self.sortMenu.add_command(label = SORT + ' ' + ROWS, command = lambda: self.sort(ROWS))
        self.sortMenu.add_command(label = SORT + ' ' + COLS, command = lambda: self.sort(COLS))
        self.sortMenu.add_command(label = SORT + ' ' + ALL, command = lambda: self.sort(ALL))
        self.modifyMenu.add_cascade(label = SORT, menu = self.sortMenu)
        self.reverseMenu = Menu(self, tearoff = False)
        self.reverseMenu.add_command(label = REVERSE + ' ' + ROWS, command = lambda: self.reverse(ROWS))
        self.reverseMenu.add_command(label = REVERSE + ' ' + COLS, command = lambda: self.reverse(COLS))
        self.reverseMenu.add_command(label = REVERSE + ' ' + ALL, command = lambda: self.reverse(ALL))
        self.modifyMenu.add_cascade(label = REVERSE, menu = self.reverseMenu)

        ## Generate Menu
        self.generateMenu = Menu(self)
        self.generateMenu.add_command(label = GENERATE, accelerator = shortcuts[GENERATE], command = self.generate)
        self.generateClearVar = StringVar(self, value = settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.generateMenu, self.generateClearVar, \
                            lambda: settings.set(GENERATE_CLEAR_OPTION, self.generateClearVar.get()), \
                            SHOW_GENERATION_RESULT, COPY_GENERATION_RESULT, 'After Generation')
        ## Result Menu
        self.resultMenu = Menu(self)
        ## Result Type Menu
        self.matMenu = Menu(self)
        self.matMenu.add_command(label = IDENTITY_MATRIX, accelerator = shortcuts[IDENTITY_MATRIX], command = self.identityMatrix)
        self.matMenu.add_command(label = ZERO_MATRIX, accelerator = shortcuts[ZERO_MATRIX], command = self.zeroMatrix)
        self.matMenu.add_command(label = UNIT_MATRIX, accelerator = shortcuts[UNIT_MATRIX], command = self.unitMatrix)
        self.matMenu.add_separator()
        self.matMenu.add_command(label = PERMUTATION_MATRIX, accelerator = shortcuts[PERMUTATION_MATRIX], command = self.permutationMatrix)
        self.matMenu.add_command(label = PERMUTATION_MATRIX_TO_VECTOR, accelerator = shortcuts[PERMUTATION_MATRIX_TO_VECTOR], command = self.permutationConversion)
        self.matMenu.add_separator()
        self.matMenu.add_command(label = 'Unknown Matrix', command = self.unknownMatrix)
        self.detMenu = Menu(self)
        self.detMenu.add_command(label = CALCULATE, accelerator = shortcuts[CALCULATE], command = self.calculateDet)
        self.calculateClearVar = StringVar(self, value = settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        self.setupClearMenu(self.detMenu, self.calculateClearVar, \
                            lambda: settings.set(CALCULATE_CLEAR_OPTION, self.calculateClearVar.get()), \
                            SHOW_CALCULATION_RESULT, COPY_CALCULATION_RESULT, 'After Calculation')
        self.vecMenu = Menu(self)
        self.vecMenu.add_command(label = PERMUTATION_VECTOR, accelerator = shortcuts[PERMUTATION_VECTOR], command = self.permutationVector)
        self.vecMenu.add_command(label = PERMUTATION_VECTOR_TO_MATRIX, accelerator = shortcuts[PERMUTATION_VECTOR_TO_MATRIX], command = self.permutationConversion)
        self.vecOptionMenu = Menu(self, tearoff = False)
        self.arrayVecVar = BooleanVar(self, value = settings.setdefault(ARRAY_VECTOR, False))
        self.vecOptionMenu.add_checkbutton(label = 'Array Vector', variable = self.arrayVecVar, \
                                           command = lambda: settings.set(ARRAY_VECTOR, self.arrayVecVar.get()))
        self.vecOptionMenu.add_separator()
        self.vecOptionVar = StringVar(self)
        for option in vectorOptions:
            self.vecOptionMenu.add_radiobutton(label = option, variable = self.vecOptionVar, \
                                               command = lambda: settings.set(VECTOR_OPTION, self.vecOptionVar.get()))
        self.vecOptionVar.set(settings.setdefault(VECTOR_OPTION, COLUMN_VECTOR))
        self.vecMenu.add_cascade(label = 'Vector Options', menu = self.vecOptionMenu)
        for name, menu in zip(resultTypeOptions, [self.matMenu, self.detMenu, self.vecMenu]):
            menu['tearoff'] = False
            self.resultMenu.add_cascade(label = name, menu = menu)
        ## Result Format Menu
        self.latexMenu = Menu(self)
        self.latexNewlineVar = BooleanVar(self, value = settings.setdefault(LATEX_NEWLINE, False))
        self.latexMenu.add_checkbutton(label = NEWLINE_ENDING, variable = self.latexNewlineVar, \
                                       command = lambda: settings.set(LATEX_NEWLINE, self.latexNewlineVar.get()))
        self.latexMenu.add_separator()
        self.latexOptionVar = StringVar(self)
        for option in [PARENTHESE, SQUARE_BRACKET]:
            self.latexMenu.add_radiobutton(label = option, variable = self.latexOptionVar, \
                                           command = lambda: settings.set(LATEX_OPTION, self.latexOptionVar.get()))
        self.latexOptionVar.set(settings.setdefault(LATEX_OPTION, SQUARE_BRACKET))
        self.arrayMenu = Menu(self)
        self.arrayNewlineVar = BooleanVar(self, value = settings.setdefault(ARRAY_NEWLINE, False))
        self.arrayMenu.add_checkbutton(label = NEWLINE_ENDING, variable = self.arrayNewlineVar, \
                                       command = lambda: settings.set(ARRAY_NEWLINE, self.arrayNewlineVar.get()))
        self.arrayMenu.add_separator()
        self.arrayOptionVar = StringVar(self)
        for option in arrayOptions:
            self.arrayMenu.add_radiobutton(label = option, variable = self.arrayOptionVar, \
                                           command = lambda: settings.set(ARRAY_OPTION, self.arrayOptionVar.get()))
        self.arrayOptionVar.set(settings.setdefault(ARRAY_OPTION, NORMAL_ARRAY))
        for name, menu in zip(resultFormatOptions, [self.latexMenu, self.arrayMenu]):
            menu['tearoff'] = False
            self.resultMenu.add_cascade(label = name, menu = menu)

        ## Help Menu
        self.helpMenu = Menu(self)
        self.helpMenu.add_command(label = 'Adjust Entry Width', command = self.adjustWidth)
        self.rememberSizeVar = BooleanVar(self, value = settings.setdefault(REMEMBER_SIZE, (-1, -1)) != (-1, -1))
        self.helpMenu.add_checkbutton(label = 'Remember Size', variable = self.rememberSizeVar, \
                                      command = lambda: settings.set(REMEMBER_SIZE, self.getRowCol() if self.rememberSizeVar.get() else (-1, -1)))
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label = 'Other Keyboard Shortcuts', command = lambda: messagebox.showinfo(title = 'Shortcuts', message = otherShortcuts))
        for name, menu in zip(['Insert', 'Edit', 'Modify', 'Generate', 'Result', 'Help'], [self.insertMenu, self.editMenu, self.modifyMenu, self.generateMenu, self.resultMenu, self.helpMenu]):
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

        self.rowLabel = Label(self.topFrame, text = ROWS + ':')
        self.rowEntry = Entry(self.topFrame)
        self.colLabel = Label(self.topFrame, text = COLS + ':')
        self.colEntry = Entry(self.topFrame)
        # Move focus before Emptry Delete
        # bindtags = self.colEntry.bindtags()
        # self.colEntry.bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))
        # self.colEntry.bind('<BackSpace>', self.rowEntry.focus())
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
        self.master.bind('<Control-A>', lambda event: self.clear(2))
        self.master.bind('<Control-C>', lambda event: self.calculateDet())
        self.master.bind('<Control-E>', lambda event: self.clear(1))
        self.master.bind('<Control-F>', lambda event: self.find(FIND_LOCATION))
        self.master.bind('<Control-L>', lambda event: self.triangularMatrix(LOWER))
        self.master.bind('<Control-P>', lambda event: self.permutationConversion())
        self.master.bind('<Control-R>', lambda event: self.randomReorder())
        self.master.bind('<Control-U>', lambda event: self.triangularMatrix(UPPER))
        self.master.bind('<Control-Z>', lambda event: self.clear(0))
        self.master.bind('<Alt-a>', lambda event: self.aToZ())
        self.master.bind('<Alt-c>', lambda event: self.switch(COLS))
        self.master.bind('<Alt-e>', lambda event: self.append(APPEND_END))
        self.master.bind('<Alt-i>', lambda event: self.appendIndex())
        self.master.bind('<Alt-n>', lambda event: self.oneToN())
        self.master.bind('<Alt-r>', lambda event: self.switch(ROWS))
        self.master.bind('<Alt-s>', lambda event: self.append(APPEND_START))
        self.master.bind('<Alt-t>', lambda event: self.transpose())
        self.master.bind('<Alt-[>', lambda event: self.switchResultFormat(-1))
        self.master.bind('<Alt-]>', lambda event: self.switchResultFormat(1))
        self.master.bind('<Alt-A>', lambda event: self.insert(ARRAY))
        self.master.bind('<Alt-C>', lambda event: self.fillRC(FILL_COLUMN))
        self.master.bind('<Alt-L>', lambda event: self.insert(LATEX))
        self.master.bind('<Alt-R>', lambda event: self.fillRC(FILL_ROW))

        ## Set Values
        self.setResultType(settings.setdefault(RESULT_TYPE, MATRIX))
        self.setResultFormat(settings.setdefault(RESULT_FORMAT, LATEX))
        settings.setdefault(RANDOM_MIN, 1)
        settings.setdefault(RANDOM_MAX, maxSize)
        settings.setdefault(RANDOM_VAR, defaultVar)
        settings.setdefault(UNKNOWN_MATRIX, ('a', 'i', 'j'))
        if self.rememberSizeVar.get():
            r, c = settings[REMEMBER_SIZE]
            if r > 0:
                setEntry(self.rowEntry, r)
            if c > 0:
                setEntry(self.colEntry, c)
            self.generateEntries(r, c)
        self.modifyState()

    def getRow(self):
        return int(self.rowEntry.get() or self.row)

    def getCol(self):
        return int(self.colEntry.get() or self.col)

    def getRowCol(self):
        return self.getRow(), self.getCol()

    def setRow(self, row):
        setEntry(self.rowEntry, row)

    def setCol(self, col):
        setEntry(self.colEntry, col)

    def setRowCol(self, row, col):
        self.setRow(row)
        self.setCol(col)

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
        settings[RESULT_TYPE] = resultType
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
            if self.getFocusEntry() == self.colEntry:
                self.rowEntry.focus()
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
        settings[RESULT_FORMAT] = self.resultFormat.get()

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
            settings[REMEMBER_SIZE] = (r, c)
        self.row = r
        self.col = c
        self.modifyState()

    def generateEntries(self, row, col):
        if row < 1 or col < 1:
            return
        width = settings.setdefault(ENTRY_WIDTH, 20)
        for i in range(1, col + 1):
            if (0, i) in self.entryLabels:
                continue
            label = Label(self.entryFrame, width = columnLabelWidth, text = i)
            label.grid(row = 0, column = i)
            self.entryLabels[(0, i)] = label
        for i in range(row):
            if (i + 1, 0) not in self.entryLabels:
                label = Label(self.entryFrame, text = i + 1)
                label.grid(row = i + 1, column = 0)
                self.entryLabels[(i + 1, 0)] = label
            for j in range(col):
                if (i, j) in self.entries:
                    continue
                entry = Entry(self.entryFrame, width = width)
                self.bindMoveFocus(entry)
                entry.bind('<KeyRelease>', self.onEntryChange)
                entry.bind('<BackSpace>', self.beforeDelete)
                bindtags = entry.bindtags()
                entry.bindtags((bindtags[2], bindtags[0], bindtags[1], bindtags[3]))
                entry.grid(row = i + 1, column = j + 1, sticky = NSEW)
                self.entries[(i, j)] = entry
        for i, j in self.entries.copy():
            if i >= row or j >= col:
                self.entries[(i, j)].grid_forget()
                del self.entries[(i, j)]
        for i, j in self.entryLabels.copy():
            if i > row:
                self.entryLabels[(i, 0)].grid_forget()
                del self.entryLabels[(i, 0)]
            elif j > col:
                self.entryLabels[(0, j)].grid_forget()
                del self.entryLabels[(0, j)]

    def beforeDelete(self, event):
        entry = self.getFocusEntry()
        if entry.get(): return
        info = entry.grid_info()
        r, c = info['row'] - 1, info['column'] - 1
        col = self.getCol()
        if r == 0 and c == 0:
            self.colEntry.focus()
        elif c == 0:
            self.entries[(r - 1, col - 1)].focus()
        else:
            self.entries[(r, c - 1)].focus()

    def onEntryChange(self, event):
        self.modifyState()

    def bindMoveFocus(self, entry):
        for key in ['<Up>', '<Down>', '<Left>', '<Right>']:
            entry.bind(key, self.moveFocus)

    def moveFocus(self, event):
        key = event.keysym
        entry = event.widget
        cursorIndex = entry.index(INSERT)
        isEnd = cursorIndex == len(entry.get())
        if (key == LEFT and cursorIndex) or (key == RIGHT and not isEnd):
            return
        row, col = self.getRowCol()
        if entry in self.sizeEntries:
            if key in [LEFT, RIGHT]:
                fEntry = self.sizeEntries[entry == self.rowEntry]
            else:
                # check empty
                if not self.entries: return
                fEntry = self.entries[(row - 1 if key == UP else 0, 0 if entry == self.rowEntry else col - 1)]
        else:
            info = entry.grid_info()
            r, c = info['row'] - 1, info['column'] - 1
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
                if not result:
                    break
                asked = True
            entry.insert(0, 0)
        else:
            result = True
        return result

    def generate(self):
        checkEmpty = self.checkEmpty()
        if checkEmpty == None: return
        result = ''
        r, c = self.getRowCol()
        resultType = self.resultType.get()
        resultFormat = self.resultFormat.get()
        if resultFormat == LATEX:
            vecOption = settings[VECTOR_OPTION]
            if resultType == VECTOR and vecOption != COLUMN_VECTOR:
                result = ezs.vl(','.join(self.collectEntries(r, c, False, False, checkEmpty)), vecOption == OVERRIGHTARROW)
            else:
                result = ezs.ml(r, c, ' '.join(self.collectEntries(r, c, False, False, checkEmpty)), resultType == DETERMINANT, settings[LATEX_NEWLINE], settings[LATEX_OPTION])
        elif resultFormat == ARRAY:
            arrayOption = settings[ARRAY_OPTION]
            normalArray = arrayOption == NORMAL_ARRAY
            if resultType == VECTOR and settings[ARRAY_VECTOR]:
                result = str(self.collectEntries(r, c, True, False, checkEmpty))
            else:
                result_list = self.collectEntries(r, c, True, True, checkEmpty)
                result = str(result_list)
                if settings[ARRAY_VECTOR]:
                    try:
                        if len(result_list) == 1 or len(result_list[0]) == 1:
                            result = str(ez.flatten(result_list))
                    except: pass
                for row in result_list:
                    for entry in row:
                        ## if is expression
                        if isinstance(entry, str) and ezs.isNumeric(ez.tryEval(entry)):
                            result = result.replace(f"'{entry}'", f'{entry}')
                if settings[ARRAY_NEWLINE]:
                    # Maybe ], \\\n?
                    result = result.replace('],', '],\n')
            if not normalArray:
                prefix = 'np' if arrayOption == NP_ARRAY else 'numpy'
                result = f'{prefix}.array({result})'
        if settings[COPY_GENERATION_RESULT]:
            ez.copyToClipboard(result)
        if settings[SHOW_GENERATION_RESULT]:
            messagebox.showinfo(title = 'Result', message = result + '\nhas been copied to the clipboard!')
        clearOption = settings[GENERATE_CLEAR_OPTION]
        if clearOption == CLEAR_ENTRIES:
            self.clear(1)
        elif clearOption == CLEAR_ALL:
            self.clear(2)
        return result

    def collectEntries(self, r: int, c: int, evaluate: bool = True, nested: bool = False, withEmpty: bool = True):
        entries = []
        for i in range(r):
            if nested: lst = []
            for j in range(c):
                text = self.entries[(i, j)].get()
                if not withEmpty and not text: continue
                if evaluate and text: text = ezs.numEval(text)
                if nested: lst.append(text)
                else: entries.append(text)
            if nested and (lst or withEmpty): entries.append(lst)
        return entries

    def switchResultType(self, move):
        self.setResultType(resultTypeOptions[(resultTypeOptions.index(self.resultType.get()) + move) % len(resultTypeOptions)])

    def switchResultFormat(self, move):
        self.setResultFormat(resultFormatOptions[(resultFormatOptions.index(self.resultFormat.get()) + move) % len(resultFormatOptions)])

    def add(self):
        fEntry = self.getFocusEntry()
        result = simpledialog.askstring(title = 'Multiply', prompt = 'Add to Each Entry')
        fEntry.focus()
        if not result: return
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
        self.modifyState()

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
                            for ch in text:
                                coeff = coef + ch
                                if ezs.isNumeric(ezs.numEval(coeff)):
                                    coef = coeff
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
        self.modifyState()

    def insert(self, fromFormat):
        '''fromFormat can only be LaTeX or Array'''
        getType = lambda matrix: VECTOR if len(matrix) > 1 and len(matrix[0]) == 1 else MATRIX
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
                            self.setResultType(getType(matrix))
                        elif 'vmatrix' in result:
                            self.setResultType(DETERMINANT)
                        else:
                            raise Exception()
                    else:
                        matrix = [[i] for i in ez.find(result).between('{', '}').split(',')]
                        self.setResultType(VECTOR)
                elif fromFormat == ARRAY:
                    matrix = ez.tryEval(result)
                    entries = [item.strip() for item in ez.without(result, '[', ']').split(',')]
                    if type(matrix) == str:
                        matrix = [entries]
                    else:
                        # Avoid Arithmatric Expression Evaluation
                        hasLen = '__len__' in dir(matrix)
                        r = len(matrix) if hasLen else 1
                        c = len(matrix[0]) if hasLen and '__len__' in dir(matrix[0]) else 1
                        matrix = [entries[i:i + c] for i in range(r)]
                    self.setResultType(getType(matrix))
                r = len(matrix)
                c = len(matrix[0])
                if r == 1 and c > 1 and settings[VECTOR_OPTION] == COLUMN_VECTOR:
                    r, c = c, r
                    matrix = [[item] for item in matrix[0]]
                if (r * c > maxSize ** 2):
                    messagebox.showerror(title = 'Error', message = 'Matrix Too Large')
                break
            except:
                messagebox.showerror(title = 'Error', message = 'Invalid Input')
        fEntry.focus()
        if result:
            self.setRowCol(r, c)
            self.generateEntries(r, c)
            for i in range(r):
                for j in range(c):
                    setEntry(self.entries[(i, j)], matrix[i][j])
            self.modifyState()

    def appendIndex(self):
        isLatex = self.resultFormat.get() == LATEX
        for i in range(self.getRow()):
            for j in range(self.getCol()):
                text = f'{i + 1}{j + 1}'
                self.entries[(i, j)].insert(END, '_{%s}' % text if isLatex else text)

    def fillRC(self, title):
        isRow = title == FILL_ROW
        fEntry = self.getFocusEntry()
        result = ''
        while True:
            result = simpledialog.askstring(title = title, prompt = title + ' N With x. \nInput N,x', initialvalue = result)
            if result:
                try:
                    resultLst = result.split(',')
                    row, col = self.getRowCol()
                    if len(resultLst) == 1:
                        if (row == 1 and isRow) or (col == 1 and not isRow):
                            k, x = 0, resultLst[0]
                        else:
                            raise Exception()
                    else:
                        k, x = list(map(str.strip, resultLst))
                        k = eval(k) - 1
                    for i in range(col if isRow else row):
                        setEntry(self.entries[(k, i) if isRow else (i, k)], x)
                except:
                    messagebox.showerror('Error', 'Invalid Input')
                    continue
            break
        fEntry.focus()

    def copyRC(self, title):
        isRow = title == ROW
        fEntry = self.getFocusEntry()
        result = ''
        prompt = f'Input i,j to Copy {title} i to {title} j.'
        r, c = self.getRowCol()
        while True:
            result = simpledialog.askstring(title = f'Copy {title}', prompt = prompt, initialvalue = result)
            if not result: break
            try:
                i, j = map(int, result.split(','))
                i, j = i - 1, j - 1
                if (isRow and not (0 <= i <= r and 0 <= j <= r)) or \
                   (not isRow and not (0 <= i <= c and 0 <= j <= c)):
                    raise Exception()
            except:
                messagebox.showerror('Error', 'Invalid Input')
                continue
            if isRow:
                for _ in range(c):
                    setEntry(self.entries[(j, _)], self.entries[(i, _)].get())
            else:
                for _ in range(r):
                    setEntry(self.entries[(_, j)], self.entries[(_, i)].get())
            break
        fEntry.focus()

    def duplicateRC(self, title):
        isRow = title == ROWS
        fEntry = self.getFocusEntry()
        result = ''
        prompt = f'Input n to make other {title} the duplicate of {title[:-1]} n.'
        r, c = self.getRowCol()
        entries = self.collectEntries(r, c, False, True)
        auto = 0
        if isRow:
            for i, row in enumerate(entries):
                if all(entry for entry in row):
                    auto += 1
                    if auto > 1:
                        auto = 0
                        result = ''
                        break
                    result = i
        else:
            for i in range(c):
                if all(row[i] for row in entries):
                    auto += 1
                    if auto > 1:
                        auto = 0
                        result = ''
                        break
                    result = i
        while True:
            if not auto:
                result = simpledialog.askinteger(title = f'Duplicate {title}', prompt = prompt, initialvalue = result)
                if not result: break
                try:
                    if (isRow and not 0 <= result <= r) or (not isRow and not 0 <= result <= c):
                        raise Exception()
                    result -= 1
                except Exception as e:
                    messagebox.showerror('Error', 'Invalid Input')
                    continue
            if isRow:
                entries = [entries[result]] * r
            else:
                entries = [[entries[i][result]] * c for i in range(r)]
            for i in range(r):
                for j in range(c):
                    setEntry(self.entries[(i, j)], entries[i][j])
            break
        fEntry.focus()

    def identityMatrix(self):
        if self.resultType.get() == VECTOR:
            self.setResultType(MATRIX)
        row, col = self.getRowCol()
        if row != col:
            self.syncRowCol(max(row, col))
        for i, j in self.entries:
            setEntry(self.entries[(i, j)], 1 if i == j else 0)
        self.modifyState()

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
                result = simpledialog.askstring(title = findType, prompt = 'Input Location x,y', initialvalue = result)
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
        self.modifyState()

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
        self.modifyState()
        dialog.close()

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

    def switch(self, target):
        isRow = target == ROWS
        row, col = self.getRowCol()
        if row == 0 or col == 0 or (isRow and row == 1) or (not isRow and col == 1):
            return
        autoSwitch = (isRow and row == 2) or (not isRow and col == 2)
        fEntry = self.getFocusEntry()
        result = ''
        while True:
            if autoSwitch:
                size1, size2 = 0, 1
            else:
                result = simpledialog.askstring(title = 'Switch ' + target, prompt = f'Input {target[:-1]} Numbers x,y', initialvalue = result)
                if not result:
                    break
                try:
                    size = row if isRow else col
                    size1, size2 = result.split(',')
                    size1, size2 = eval(size1) - 1, eval(size2) - 1
                    if not (0 <= size1 < size and 0 <= size2 < size):
                        raise Exception()
                except:
                    messagebox.showerror(title = 'Error', message = 'Invalid Input')
                    continue
            for i in range(col if isRow else row):
                e1 = self.entries[(size1, i) if isRow else (i, size1)]
                e2 = self.entries[(size2, i) if isRow else (i, size2)]
                t1, t2 = e1.get(), e2.get()
                setEntry(e1, t2)
                setEntry(e2, t1)
            break
        fEntry.focus()
        self.modifyState()

    def transpose(self):
        resultType = self.resultType.get()
        if resultType not in [MATRIX, DETERMINANT, VECTOR]:
            return
        row, col = self.getRowCol()
        entries = { key: self.entries[key].get() for key in self.entries }
        if row != col:
            if resultType == VECTOR:
                self.setResultType(MATRIX)
            self.setRowCol(col, row)
            self.generateEntries(col, row)
        for i in range(row):
            for j in range(col):
                setEntry(self.entries[(j, i)], entries[(i, j)])
        self.modifyState()

    def zeroMatrix(self):
        for entry in self.entries.values():
            setEntry(entry, 0)
        self.modifyState()

    def oneToN(self):
        row, col = self.getRowCol()
        if not row or not col or not self.entries:
            return
        for i in range(row * col):
            setEntry(self.entries[divmod(i, col)], i + 1)
        self.modifyState()

    def aToZ(self):
        row, col = self.getRowCol()
        if not row or not col or not self.entries:
            return
        ordA = ord('a')
        for i in range(row * col):
            count, char = divmod(i, 26)
            setEntry(self.entries[divmod(i, col)], chr(ordA + char) * (count + 1))
        self.modifyState()

    def fibonacci(self):
        row, col = self.getRowCol()
        if not row or not col or not self.entries:
            return
        def fib(num):
            a, b = 1, 1
            for _ in range(num):
                yield a
                a, b = b, a + b
        for i, n in enumerate(fib(row * col)):
            setEntry(self.entries[divmod(i, col)], n)
        self.modifyState()

    def setRandomVar(self):
        result = settings[RANDOM_VAR]
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
                settings[RANDOM_VAR] = result
                break
        fEntry.focus()

    def onConfirmRange(self, dialog, minValue, maxValue):
        try:
            minValue = int(minValue)
            maxValue = int(maxValue)
            if minValue > maxValue:
                raise Exception()
            settings[RANDOM_MIN] = minValue
            settings[RANDOM_MAX] = maxValue
        except:
            messagebox.showerror('Error', 'Invalid Input')
            return

    def setRandomRange(self):
        dialog = RangeDialog(self)
        dialog.setMinMax(settings[RANDOM_MIN], settings[RANDOM_MAX])
        dialog.setOnConfirmListener(self.onConfirmRange)
        self.wait_window(dialog)

    def randomFill(self):
        resultType = self.resultType.get()
        row, col = self.getRowCol()
        total = row * col
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
        option = settings[RANDOM_MATRIX_OPTION]
        randMin = settings[RANDOM_MIN]
        randMax = settings[RANDOM_MAX]
        if option in [RANDOM_INT_MATRIX, RANDOM_VAR_MATRIX]:
            if settings[UNIQUE_RANDOM]:
                values = list(range(randMin, randMax + 1)) + [randint(randMin, randMax) for _ in range(randMin + total - randMax - 1)]
                shuffle(values)
            else:
                values = [randint(randMin, randMax)  for _ in range(total)]
            if option == RANDOM_VAR_MATRIX and self.resultFormat.get() == LATEX:
                values = ['{%s}_{%d}' % (settings[RANDOM_VAR], value) for value in values]
        elif option == RANDOM_MULTIVAR_MATRIX:
            values = [chr(randrange(ord('a'), ord('z') + 1)) for _ in range(total)]
        hasEmpty = False
        for entry in self.entries.values():
            if not entry.get():
                hasEmpty = True
                setEntry(entry, values.pop())
        if not hasEmpty:
            for entry in self.entries.values():
                setEntry(entry, values.pop())
        self.modifyState()

    def randomReorder(self):
        current = self.collectEntries(self.getRow(), self.getCol())
        values = current
        while current == values:
            shuffle(values)
        for entry in self.entries.values():
            setEntry(entry, values.pop(0))
        self.modifyState()

    def sort(self, target):
        row, col = self.getRowCol()
        if not row or not col or not self.entries:
            return
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
        if target == ALL:
            if varFormat:
                values = [f'{var}_{number}' for var, number in sorted(vars)]
            else:
                try: values = sorted(self.collectEntries(row, col))
                except: values = sorted(self.collectEntries(row, col, False))
            for i in range(row * col):
                setEntry(self.entries[divmod(i, col)], values[i])
        else:
            if varFormat:
                vars = [vars[i:i + col] for i in range(row)]
                if target == ROWS:
                    values = [sorted(row) for row in vars]
                else:
                    values = sorted(values)
                values = [f'{var}_{number}' for var, number in sorted(vars)]
            else:
                try: values = self.collectEntries(row, col, True, True)
                except: values = self.collectEntries(row, col, False, True)
                if target == ROWS:
                    values = [sorted(row) for row in values]
                else:
                    values = sorted(values)
            for i in range(row):
                for j in range(col):
                    setEntry(self.entries[(i, j)], values[i][j])
        self.modifyState()

    def reverse(self, target):
        row, col = self.getRowCol()
        if not row or not col or not self.entries:
            return
        if target == ALL:
            for i in range(row * col // 2):
                r, c = divmod(i, col)
                e1, e2 = self.entries[(r, c)], self.entries[(row - r - 1, col - c - 1)]
                t1, t2 = e2.get(), e1.get()
                setEntry(e1, t1)
                setEntry(e2, t2)
        else:
            values = self.collectEntries(row, col, False, True)
            if target == ROWS:
                values = [list(reversed(row)) for row in values]
            else:
                values = list(reversed(values))
            for i in range(row):
                for j in range(col):
                    setEntry(self.entries[(i, j)], values[i][j])
        self.modifyState()

    def reshape(self):
        r, c = self.getRowCol()
        size = r * c
        if size <= 1:
            return
        factors = ezs.findAllFactors(size)
        if ezs.isPrime(size) or (size > maxSize and len(factors) == 4):
            x, y = c, r
        else:
            result = f'{c},{r}' if len(factors) == 4 else ''
            fEntry = self.getFocusEntry()
            while True:
                result = simpledialog.askstring(title = 'Reshape', prompt = 'Input New Shape r,c', initialvalue = result)
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
        values = self.collectEntries(r, c, False)
        self.setResultType(VECTOR if x > 1 and y == 1 else MATRIX)
        self.setRowCol(x, y)
        self.generateEntries(x, y)
        for i, value in enumerate(values):
            setEntry(self.entries[divmod(i, y)], value)
        self.modifyState()

    def triangularMatrix(self, mode):
        for i, j in self.entries:
            if i < j if mode == LOWER else i > j:
                setEntry(self.entries[(i, j)], 0)
        self.modifyState()

    def unitMatrix(self):
        for entry in self.entries.values():
            setEntry(entry, 1)
        self.modifyState()

    def permutationMatrix(self):
        row, col = self.getRowCol()
        size = max(row, col) or min(row, col) or randrange(maxSize) + 1
        self.setResultType(MATRIX)
        if not row == col == size:
            self.syncRowCol(size)
        cols = list(range(size))
        shuffle(cols)
        for i in range(size):
            for j in range(size):
                setEntry(self.entries[(i, j)], 0)
            setEntry(self.entries[(i, cols.pop())], 1)
        self.modifyState()

    def unknownMatrix(self):
        dialog = UnknownMatrix(self)
        var, row, col = settings[UNKNOWN_MATRIX]
        dialog.setData(var, row, col)
        dialog.setOnCopyListener(lambda dialog, result: ez.copyToClipboard(result))
        dialog.setOnCloseListener(lambda dialog, var, row, col: settings.set(UNKNOWN_MATRIX, (var, row, col)) )
        self.wait_window(dialog)

    def permutationVector(self):
        self.setResultType(VECTOR)
        row = self.getRow()
        if not row:
            row = randrange(maxSize) + 1
        values = list(range(row) if settings[ARRAY_OPTION] != NORMAL_ARRAY and self.resultFormat.get() == ARRAY else range(1, row + 1))
        current = self.collectEntries(row, 1)
        while values == current:
            shuffle(values)
        for entry in self.entries.values():
            setEntry(entry, values.pop(0))
        self.modifyState()

    def permutationConversion(self):
        resultType = self.resultType.get()
        r, c = self.getRowCol()
        isNormal = settings[ARRAY_OPTION] == NORMAL_ARRAY
        notVector = resultType != VECTOR
        entries = self.collectEntries(r, c, True, notVector)
        if notVector:
            for i, row in enumerate(entries):
                if row.count(1) != 1 and row.count(0) != len(row) - 1:
                    return
                setEntry(self.entries[(i, 0)], row.index(1) + isNormal)
            self.setResultType(VECTOR)
        else:
            if any(i not in entries for i in range(isNormal, r + isNormal)):
                return
            self.setResultType(MATRIX)
            self.syncRowCol(r)
            for i in range(r):
                for j in range(r):
                    setEntry(self.entries[(i, j)], entries[i] == j + isNormal)
        self.modifyState()

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
            if settings[COPY_CALCULATION_RESULT]:
                ez.copyToClipboard(str_result)
            if settings[SHOW_CALCULATION_RESULT]:
                messagebox.showinfo(title = 'Result', message = 'Value: ' + str_result)
            clearOption = self.calculateClearVar.get()
            if clearOption == CLEAR_ENTRIES:
                self.clear(1)
            elif clearOption == CLEAR_ALL:
                self.clear(2)
            return result
        except ValueError:
            messagebox.showerror(title = 'Error', message = 'Numerical Entries Only')

    def setupClearMenu(self, master, variable, command, showResultOption, copyResultOption, label = 'Clear Options'):
        clearMenu = Menu(master = master, tearoff = False)
        showResultVar = BooleanVar(self, value = settings.setdefault(showResultOption, True))
        clearMenu.add_checkbutton(label = SHOW_RESULT, variable = showResultVar, \
                                  command = lambda: settings.set(showResultOption, showResultVar.get()))
        copyResultVar = BooleanVar(self, value = settings.setdefault(copyResultOption, True))
        clearMenu.add_checkbutton(label = COPY_RESULT, variable = copyResultVar, \
                                  command = lambda: settings.set(copyResultOption, copyResultVar.get()))
        clearMenu.add_separator()
        for option in clearOptions:
            clearMenu.add_radiobutton(label = option, value = option, variable = variable, command = command)
        variable.set(settings.setdefault(GENERATE_CLEAR_OPTION, NONE))
        master.add_cascade(label = label, menu = clearMenu)

    def clear(self, mode):
        '''0 for clear zeros, 1 for clear entries, 1 for clear all'''
        if mode == 0:
            for entry in self.entries.values():
                if ez.tryEval(entry.get()) == 0:
                    clearEntry(entry)
        else:
            if mode >= 1:
                for entry in self.entries.values():
                    clearEntry(entry)
            if mode >= 2:
                clearEntry(self.rowEntry)
                clearEntry(self.colEntry)
                for entry in self.entries.values():
                    entry.grid_forget()
                self.entries.clear()
                for label in self.entryLabels.values():
                    label.grid_forget()
                self.entryLabels.clear()
                self.rowEntry.focus()
        self.modifyState()

    def modifyEntryWidth(self, dialog, value):
        settings[ENTRY_WIDTH] = value
        for entry in self.entries.values():
            entry['width'] = value
        for i in range(1, self.getCol() + 1):
            self.entryLabels[(0, i)]['width'] = value

    def adjustWidth(self):
        dialog = SliderDialog(self, 20)
        dialog.setSliderValue(settings[ENTRY_WIDTH])
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

    def modifyState(self):
        row, col = self.getRowCol()
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
        index = (0, 0, END)
        try:
            entry = self.master.focus_get()
            f = ez.find(str(entry))
            index = (int(f.between('frame', '.') or 1) - 1, int(f.after('.!entry') or 1) - 1, entry.index(ANCHOR) if entry.selection_present() else entry.index(INSERT))
        except:
            pass
        return index

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

if __name__ == "__main__":
    root = Tk()
    app = Generator(root)
    app.pack()
    root.title('Matrix Generator')
    ez.py2pyw(__file__)
    root.mainloop()
