from tkinter import *

MATRIX = 'Matrix'
DETERMINANT = 'Determinant'
VECTOR = 'Vector'
IDENTITY_MATRIX = 'Identity Matrix'
resultTypeOptions = [MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX]
LATEX = 'LaTeX'
ARRAY = 'Array'
resultFormatOptions = [LATEX, ARRAY]
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
        self.settings = {}

        ## generate menus
        self.menu = Menu(self)
        self.editMenu = Menu(self.menu, tearoff = False)
        self.editMenu.add_command(label = 'Random')
        self.editMenu.add_command(label = 'Unit Matrix')
        self.editMenu.add_command(label = 'Multiply')
        self.editMenu.add_command(label = 'Transpose')
        self.editMenu.add_separator()
        self.editMenu.add_command(label = CLEAR_SIZE)
        self.editMenu.add_command(label = CLEAR_ENTRIES)
        self.editMenu.add_command(label = CLEAR_ALL)
        self.generateMenu = Menu(self.menu, tearoff = False)
        self.generateMenu.add_command(label = 'Generate' + ' ' * 10 + 'Enter/Return')
        self.GENERATE_CLEAR_OPTION = 'GenerateClearOption'
        self.generateClearVar = StringVar(self)
        self.matMenu = Menu(self.menu, tearoff = False)
        self.matMenu.add_command(label = 'Lower Triangular')
        self.matMenu.add_command(label = 'Upper Triangular')
        self.detMenu = Menu(self.menu, tearoff = False)
        self.detMenu.add_command(label = 'Calculate')
        self.CALCULATE_CLEAR_OPTION = 'CalculateClearOption'
        self.vecMenu = Menu(self.menu, tearoff = False)
        self.COLUMN_VECTOR = 'ColumnVector'
        self.colVecVar = BooleanVar(self, value = self.settings.get(self.COLUMN_VECTOR, True))
        self.vecMenu.add_checkbutton(label = 'Column Vector', variable = self.colVecVar)
        self.imatMenu = Menu(self.menu, tearoff = False)
        self.imatMenu.add_command(label = 'Permutation Matrix')
        self.settingsMenu = Menu(self.menu, tearoff = False)
        self.REMEMBER_SIZE = 'RememberSize'
        self.rememberSizeVar = BooleanVar(self, value = self.settings.get(self.REMEMBER_SIZE, self.settings.setdefault(self.REMEMBER_SIZE, (-1, -1))) != (-1, -1))
        self.settingsMenu.add_checkbutton(label = 'Remember Size', variable = self.rememberSizeVar)
        self.SHOW_DIALOG = 'ShowDialog'
        self.showDialogVar = BooleanVar(self, value = self.settings.get(self.SHOW_DIALOG, True))
        self.settingsMenu.add_checkbutton(label = 'Show Dialog', variable = self.showDialogVar)
        self.settingsMenu.add_separator()
        self.settingsMenu.add_command(label = 'Keyboard Shortcuts')
        for name, menu in zip(['Edit', 'Generate'] + resultTypeOptions + ['Settings'], [self.editMenu, self.generateMenu, self.matMenu, self.detMenu, self.vecMenu, self.imatMenu, self.settingsMenu]):            
            self.menu.add_cascade(label = name, menu = menu)
        self.master.config(menu = self.menu)
        
        ## generate widgets
        self.resultTypeLabel = Label(self, text = 'Result Type:')
        self.RESULT_TYPE = 'ResultType'
        self.resultType = StringVar(self)
        self.resultTypeDropdown = OptionMenu(self, self.resultType, *resultTypeOptions)
        self.resultFormatLabel = Label(self, text = 'Result Format:')
        self.RESULT_FORMAT = 'ResultFormat'
        self.resultFormat = StringVar(self)
        self.resultFormatDropdown = OptionMenu(self, self.resultFormat, *resultFormatOptions)
        self.dropdownTypes = [self.RESULT_TYPE, self.RESULT_FORMAT]
        
        self.rowLabel = Label(self, text = 'Rows:')
        self.rowEntry = Entry(self)
        self.colLabel = Label(self, text = 'Columns:')
        self.colEntry = Entry(self)
        self.rowEntry.focus()

        ## place widgets
        for i, w in enumerate([self.resultTypeLabel, self.resultTypeDropdown, self.resultFormatLabel, self.resultFormatDropdown]):
            w.grid(row = 0, column = i, sticky = NSEW)
        for i, w in enumerate([self.rowLabel, self.rowEntry, self.colLabel, self.colEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)

root = Tk()
gui = Generator(root)
gui.pack()
root.title('Generator')
root.mainloop()