from tkinter import *
from tkinter import messagebox

UP = 'Up'
DOWN = 'Down'
SYSTEM_HIGHLIGHT = 'SystemHighlight'
BUTTON_BORDER = '#b5b5b5'

class FindDialog(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        self.title('Search Dialog')

        ## Variables
        self.findListner = None
        self.directionListener = None
        self.closeListener = None

        self.findLabel = Label(self, text = 'Find:')
        self.findEntry = Entry(self)
        self.findEntry.focus()
        self.findEntry.select_range(0, END)
        for i, w in enumerate([self.findLabel, self.findEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)
        self.findEntry.grid(columnspan = 5)
        self.directionLabel = Label(self, text = 'Direction:')
        self.directionVar = StringVar(self)
        self.upRadio = Radiobutton(self, text = UP, value = UP, variable = self.directionVar, command = self.onDirectionChange)
        self.downRadio = Radiobutton(self, text = DOWN, value = DOWN, variable = self.directionVar, command = self.onDirectionChange)
        self.directionVar.set(DOWN)
        for i, w in enumerate([self.directionLabel, self.upRadio, self.downRadio]):
            w.grid(row = 1, column = i, sticky = NSEW)

        self.findBorder = Frame(self, highlightbackground = SYSTEM_HIGHLIGHT)
        self.findButton = Button(self.findBorder, text = 'Find Next', command = self.find)
        self.closeBorder = Frame(self, highlightbackground = BUTTON_BORDER)
        self.closeButton = Button(self.closeBorder, text = 'Close', command = self.close)
        for i, (w, b) in enumerate(zip([self.findButton, self.closeButton], [self.findBorder, self.closeBorder])):
            b.grid(row = 2, column = i + 1)
            w.grid(row = 2, column = i + 1, sticky = NSEW)
            b.config(highlightthickness = 1, bd = 0)
            w['relief'] = FLAT

        self.bind('<Destroy>', lambda event: self.__onClose())
        self.bind('<Return>', lambda event: self.find())

    def setFind(self, target):
        if not target: return
        self.findEntry.insert(0, target)
        self.findEntry.focus()
        self.findEntry.select_range(0, END)

    def setOnFindListner(self, listener):
        '''listner should have the following arguments: dialog, target, direction.'''
        self.findListner = listener

    def find(self):
        if self.findListner: self.findListner(self, self.findEntry.get(), self.getDirection())

    def setOnDirectionChangeListener(self, listener):
        self.directionListener = listener

    def onDirectionChange(self):
        '''listner should have the following arguments: dialog, direction.'''
        if self.directionListener: self.directionListener(self, self.directionVar.get())

    def setDirection(self, direction):
        self.directionVar.set(direction)

    def setOnCloseListener(self, listener):
        '''listner should allow the following arguments: dialog.'''
        self.closeListener = listener

    def close(self):
        self.__onClose()
        self.withdraw()

    def __onClose(self):
        if self.closeListener: self.closeListener(self)
        self.grab_release()

    def getDirection(self):
        return self.directionVar.get()

class ReplaceDialog(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        self.title('Replace Dialog')

        ## Variables
        self.replaceText = ''
        self.findListner = None
        self.replaceListener = None
        self.replaceFindListener = None
        self.replaceAllListener = None
        self.directionListener = None
        self.closeListener = None

        self.findLabel = Label(self, text = 'Find:')
        self.findEntry = Entry(self)
        self.findEntry.select_range(0, END)
        for i, w in enumerate([self.findLabel, self.findEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)
        self.replaceLabel = Label(self, text = 'Replace With:')
        self.replaceEntry = Entry(self)
        for i, w in enumerate([self.replaceLabel, self.replaceEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)
        for entry in [self.findEntry, self.replaceEntry]:
            entry.grid(columnspan = 5)
            entry.bind('<Up>', self.moveFocus)
            entry.bind('<Down>', self.moveFocus)

        self.directionLabel = Label(self, text = 'Direction:')
        self.directionVar = StringVar(self)
        self.upRadio = Radiobutton(self, text = UP, value = UP, variable = self.directionVar, command = self.onDirectionChange)
        self.downRadio = Radiobutton(self, text = DOWN, value = DOWN, variable = self.directionVar, command = self.onDirectionChange)
        self.directionVar.set(DOWN)
        for i, w in enumerate([self.directionLabel, self.upRadio, self.downRadio]):
            w.grid(row = 2, column = i, sticky = NSEW)
        self.findBorder = Frame(self, highlightbackground = BUTTON_BORDER)
        self.findButton = Button(self.findBorder, text = 'Find', command = self.find)
        self.replaceBorder = Frame(self, highlightbackground = BUTTON_BORDER)
        self.replaceButton = Button(self.replaceBorder, text = 'Replace', command = self.replace)
        self.replaceFindBorder = Frame(self, highlightbackground = SYSTEM_HIGHLIGHT)
        self.replaceFindButton = Button(self.replaceFindBorder, text = 'Replace+Find', command = self.replaceFind)
        self.replaceAllBorder = Frame(self, highlightbackground = BUTTON_BORDER)
        self.replaceAllButton = Button(self.replaceAllBorder, text = 'Replace All', command = self.replaceAll)
        self.closeBorder = Frame(self, highlightbackground = BUTTON_BORDER)
        self.closeButton = Button(self.closeBorder, text = 'Close', command = self.close)
        for i, (w, b) in enumerate(zip([self.findButton, self.replaceButton, self.replaceFindButton, self.replaceAllButton, self.closeButton], \
                                       [self.findBorder, self.replaceBorder, self.replaceFindBorder, self.replaceAllBorder, self.closeBorder])):
            w.grid(row = 3, column = i + 1, sticky = NSEW)
            w['relief'] = FLAT
            b.grid(row = 3, column = i + 1)
            b.config(highlightthickness = 1, bd = 0)

        self.bind('<Destroy>', lambda event: self.__onClose())
        self.bind('<Return>', lambda event: self.replaceFind())

    def moveFocus(self, event):
        if event.widget == self.findEntry:
            self.replaceEntry.focus()
        else:
            self.findEntry.focus()

    def setFind(self, find):
        if not find: return
        self.findEntry.insert(0, find)
        self.findEntry.focus()
        self.findEntry.select_range(0, END)

    def setReplace(self, replace):
        self.replaceEntry.insert(0, replace)
        if not self.replaceText and replace:
            self.replaceEntry.select_range(0, END)
        self.replaceText = replace

    def setOnFindListner(self, listener):
        '''listner should have the following arguments: dialog, find and direction.'''
        self.findListner = listener

    def find(self):
        if self.findListner: self.findListner(self, self.findEntry.get(), self.getDirection())

    def setOnReplaceListener(self, listener):
        '''listner should have the following arguments: dialog, find, replace and direction.'''
        self.onReplaceListener = listener

    def replace(self):
        if self.onReplaceListener: self.onReplaceListener(self, self.findEntry.get(), self.replaceEntry.get(), self.getDirection())

    def setOnReplaceFindListener(self, listener):
        self.onReplaceFindListener = listener

    def replaceFind(self):
        '''listner should have the following arguments: dialog, find, replace and direction.'''
        if self.onReplaceFindListener: self.onReplaceFindListener(self, self.findEntry.get(), self.replaceEntry.get(), self.getDirection())

    def setOnReplaceAllListener(self, listener):
        self.onReplaceAllListener = listener

    def replaceAll(self):
        '''listner should have the following arguments: dialog, find and replace.'''
        if self.onReplaceAllListener: self.onReplaceAllListener(self, self.findEntry.get(), self.replaceEntry.get())

    def setOnDirectionChangeListener(self, listener):
        self.directionListener = listener

    def onDirectionChange(self):
        '''listner should have the following arguments: dialog, direction.'''
        if self.directionListener: self.directionListener(self, self.directionVar.get())

    def setDirection(self, direction):
        self.directionVar.set(direction)

    def setOnCloseListener(self, listener):
        '''listner should have the following arguments: dialog.'''
        self.closeListener = listener

    def close(self):
        self.__onClose()
        self.withdraw()

    def __onClose(self):
        if self.closeListener: self.closeListener(self)
        self.grab_release()

    def getDirection(self):
        return self.directionVar.get()

class SliderDialog(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        self.title('Adjust Width')

        self.destroyListener = None
        self.sliderListener = None
        self.ENTRY_WIDTH = 'Entry Width'
        self.slider = Scale(self, label = self.ENTRY_WIDTH, from_ = 5, to = 50, orient = HORIZONTAL,\
                        showvalue = 0, command = lambda event: self.onSliderChange())
        self.slider.pack()
        self.bind('<Destroy>', lambda event: self.__onDestroy())

    def setSliderValue(self, value):
        self.slider.set(value)
        self.__setSliderText(value)

    def setOnSliderChangeListener(self, listener):
        '''listner should have the following arguments: dialog, sliderValue.
           SliderText is updated automatically.'''
        self.sliderListener = listener

    def onSliderChange(self):
        sliderValue = self.slider.get()
        if self.sliderListener: self.sliderListener(self, sliderValue)
        self.__setSliderText(sliderValue)

    def __setSliderText(self, text):
        self.slider['label'] = f'{self.ENTRY_WIDTH}: {text}'

    def __onDestroy(self):
        if self.destroyListener: self.destroyListener(self)
        self.grab_release()
        self.withdraw()

    def setOnDestroyListener(self, listener):
        '''listner should have the following arguments: dialog.'''
        self.destroyListener = listener

class RangeDialog(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.master = master
        self.transient(master)
        self.grab_set()
        self.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        self.title('Set Range')

        self.confirmListener = None
        self.closeListener = None

        self.minLabel = Label(self, text = 'Min: ')
        self.minVar = IntVar(self)
        self.minEntry = Entry(self)
        self.maxLabel = Label(self, text = 'Max: ')
        self.maxVar = IntVar(self)
        self.maxEntry = Entry(self)
        self.minEntry.focus()
        for i, (l, e, v) in enumerate(zip([self.minLabel, self.maxLabel], [self.minEntry, self.maxEntry], [self.minVar, self.maxVar])):
            l.grid(row = i, column = 0)
            e.grid(row = i, column = 1, columnspan = 2)
            e['textvariable'] = v
            e.bind('<Up>', self.moveFocus)
            e.bind('<Down>', self.moveFocus)
        self.confirmBorder = Frame(self, highlightbackground = SYSTEM_HIGHLIGHT)
        self.confirmButton = Button(self.confirmBorder, text = 'Confirm', command = self.onConfirm)
        self.closeBorder = Frame(self, highlightbackground = BUTTON_BORDER)
        self.closeButton = Button(self.closeBorder, text = 'Close', command = self.close)
        for i, (w, b) in enumerate(zip([self.confirmButton, self.closeButton], [self.confirmBorder, self.closeBorder])):
            w.grid(row = 2, column = i + 1, sticky = NSEW)
            w['relief'] = FLAT
            b.grid(row = 2, column = i + 1)
            b.config(highlightthickness = 1, bd = 0)

        self.bind('<Destroy>', lambda event: self.__onClose())
        self.bind('<Return>', lambda event: self.onConfirm())

    def moveFocus(self, event):
        if event.widget == self.minEntry:
            self.maxEntry.focus()
        else:
            self.minEntry.focus()

    def setMinMax(self, minValue, maxValue):
        self.minVar.set(minValue)
        self.minEntry.select_range(0, END)
        self.maxVar.set(maxValue)

    def setOnConfirmListener(self, listener):
        '''listner should have the following arguments: dialog, min and max.'''
        self.confirmListener = listener

    def onConfirm(self):
        if self.confirmListener: self.confirmListener(self, self.minEntry.get(), self.maxEntry.get())
        self.close()

    def setOnCloseListener(self, listener):
        '''listner should have the following arguments: dialog.'''
        self.closeListener = listener

    def close(self):
        self.__onClose()
        self.withdraw()

    def __onClose(self):
        if self.closeListener: self.closeListener(self)
        self.grab_release()