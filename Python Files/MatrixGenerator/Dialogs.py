from tkinter import *
from tkinter import messagebox

UP = 'Up'
DOWN = 'Down'

class FindDialog(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Search Dialog')

        ## Variables
        self.findText = ''
        self.findListner = None
        self.closeListener = None

        self.findLabel = Label(self, text = 'Find:')
        self.findEntry = Entry(self)
        self.findEntry.select_range(0, END)
        for i, w in enumerate([self.findLabel, self.findEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)
        self.findEntry.grid(columnspan = 5)
        self.directionLabel = Label(self, text = 'Direction:')
        self.directionVar = StringVar(self)
        self.upRadio = Radiobutton(self, text = UP, value = UP, variable = self.directionVar)
        self.downRadio = Radiobutton(self, text = DOWN, value = DOWN, variable = self.directionVar)
        self.directionVar.set(DOWN)
        for i, w in enumerate([self.directionLabel, self.upRadio, self.downRadio]):
            w.grid(row = 1, column = i, sticky = NSEW)
        self.findButton = Button(self, text = 'Find Next', command = self.find)
        self.closeButton = Button(self, text = 'Close', command = self.close)
        for i, w in enumerate([self.findButton, self.closeButton]):
            w.grid(row = 2, column = i + 1, sticky = NSEW)

        self.bind('<Destroy>', lambda event: self.__onClose())
        self.bind('<Return>', lambda event: self.find())
        self.show()

    def setFind(self, find):
        self.findEntry.insert(0, find)
        if not self.findText and find:
            self.findEntry.focus()
            self.findEntry.select_range(0, END)
        self.findText = find

    def setOnFindListner(self, listener):
        '''listner should have exactly 2 arguments: target and direction.'''
        self.findListner = listener

    def find(self):
        if self.findListner: self.findListner(self.findEntry.get(), self.getDirection())

    def setOnCloseListener(self, listener):
        '''listner should have no arguments.'''
        self.closeListener = listener

    def close(self):
        self.__onClose()
        self.withdraw()

    def __onClose(self):
        if self.closeListener: self.closeListener()

    def show(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.findEntry.focus()

    def getDirection(self):
        return self.directionVar.get()

class ReplaceDialog(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Replace Dialog')

        ## Variables
        self.findText = ''
        self.replaceText = ''
        self.findListner = None
        self.replaceListener = None
        self.replaceFindListener = None
        self.replaceAllListener = None
        self.closeListener = None

        self.findLabel = Label(self, text = 'Find:')
        self.findEntry = Entry(self)
        self.findEntry.select_range(0, END)
        for i, w in enumerate([self.findLabel, self.findEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)
        self.findEntry.grid(columnspan = 5)
        self.replaceLabel = Label(self, text = 'Replace With:')
        self.replaceEntry = Entry(self)
        for i, w in enumerate([self.replaceLabel, self.replaceEntry]):
            w.grid(row = 1, column = i, sticky = NSEW)
        self.replaceEntry.grid(columnspan = 5)
        self.directionLabel = Label(self, text = 'Direction:')
        self.directionVar = StringVar(self)
        self.upRadio = Radiobutton(self, text = UP, value = UP, variable = self.directionVar)
        self.downRadio = Radiobutton(self, text = DOWN, value = DOWN, variable = self.directionVar)
        self.directionVar.set(DOWN)
        for i, w in enumerate([self.directionLabel, self.upRadio, self.downRadio]):
            w.grid(row = 2, column = i, sticky = NSEW)
        self.findButton = Button(self, text = 'Find', command = self.find)
        self.replaceButton = Button(self, text = 'Replace', command = self.replace)
        self.replaceFindButton = Button(self, text = 'Replace+Find', command = self.replaceFind)
        self.replaceAllButton = Button(self, text = 'Replace All', command = self.replaceAll)
        self.closeButton = Button(self, text = 'Close', command = self.close)
        for i, w in enumerate([self.findButton, self.replaceButton, self.replaceFindButton, self.replaceAllButton, self.closeButton]):
            w.grid(row = 3, column = i + 1, sticky = NSEW)

        self.bind('<Destroy>', lambda event: self.__onClose())
        self.bind('<Return>', lambda event: self.replaceFind())
        self.show()

    def setFind(self, find):
        self.findEntry.insert(0, find)
        if not self.findText and find:
            self.findEntry.focus()
            self.findEntry.select_range(0, END)
        self.findText = find

    def setReplace(self, replace):
        self.replaceEntry.insert(0, replace)
        if not self.replaceText and replace:
            self.replaceEntry.select_range(0, END)
        self.replaceText = replace

    def setOnFindListner(self, listener):
        '''listner should have exactly 2 arguments: find and direction.'''
        self.findListner = listener

    def find(self):
        if self.findListner: self.findListner(self.findEntry.get(), self.getDirection())

    def setOnReplaceListener(self, listener):
        '''listner should have exactly 3 arguments: find, replace and direction.'''
        self.onReplaceListener = listener

    def replace(self):
        if self.onReplaceListener: self.onReplaceListener(self.findEntry.get(), self.replaceEntry.get(), self.getDirection())

    def setOnReplaceFindListener(self, listener):
        self.onReplaceFindListener = listener

    def replaceFind(self):
        '''listner should have exactly 3 arguments: find, replace and direction.'''
        if self.onReplaceFindListener: self.onReplaceFindListener(self.findEntry.get(), self.replaceEntry.get(), self.getDirection())

    def setOnReplaceAllListener(self, listener):
        self.onReplaceAllListener = listener

    def replaceAll(self):
        '''listner should have exactly 3 arguments: find and replace.'''
        if self.onReplaceAllListener: self.onReplaceAllListener(self.findEntry.get(), self.replaceEntry.get())

    def setOnCloseListener(self, listener):
        '''listner should have no arguments.'''
        self.closeListener = listener

    def close(self):
        self.__onClose()
        self.withdraw()

    def __onClose(self):
        if self.closeListener: self.closeListener()

    def show(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.findEntry.focus()

    def getDirection(self):
        return self.directionVar.get()

class SliderDialog(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Adjust Width')

        self.sliderListener = None
        self.ENTRY_WIDTH = 'Entry Width'
        self.slider = Scale(self, label = self.ENTRY_WIDTH, from_ = 5, to = 50, orient = HORIZONTAL,\
                        showvalue = 0, command = lambda event: self.onSliderChange())
        self.slider.pack()
        self.bind('<Destroy>', lambda event: self.__onDestroy())
        self.show()

    def setSliderValue(self, value):
        self.slider.set(value)
        self.__setSliderText(value)

    def setOnSliderChangeListener(self, listener):
        self.sliderListener = listener

    def onSliderChange(self):
        sliderValue = self.slider.get()
        if self.sliderListener: self.sliderListener(sliderValue)
        self.__setSliderText(sliderValue)

    def __setSliderText(self, text):
        self.slider['label'] = f'{self.ENTRY_WIDTH}: {text}'

    def __onDestroy(self):
        if self.destroyListener: self.destroyListener()

    def setOnDestroyListener(self, listener):
        self.destroyListener = listener

    def show(self):
        self.deiconify()
        self.lift()
        self.focus_force()