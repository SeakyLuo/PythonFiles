from tkinter import *
from tkinter import messagebox

UP = 'Up'
DOWN = 'Down'

class FindDialog(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Find Value')

        ## Variables
        self.initialValue = ''
        self.findNextListner = None
        self.closeListener = None

        self.findLabel = Label(self, text = 'Find:')
        self.findEntry = Entry(self)
        self.findEntry.select_range(0, END)
        for i, w in enumerate([self.findLabel, self.findEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)
        self.findEntry.grid(columnspan = 3)
        self.directionLabel = Label(self, text = 'Direction:')
        self.directionVar = StringVar(self)
        self.upRadio = Radiobutton(self, text = UP, value = UP, variable = self.directionVar)
        self.downRadio = Radiobutton(self, text = DOWN, value = DOWN, variable = self.directionVar)
        self.directionVar.set(DOWN)
        for i, w in enumerate([self.directionLabel, self.upRadio, self.downRadio]):
            w.grid(row = 1, column = i, sticky = NSEW)
        self.findNextButton = Button(self, text = 'Find Next', command = self.findNext)
        self.closeButton = Button(self, text = 'Close', command = self.close)
        for i, w in enumerate([self.findNextButton, self.closeButton]):
            w.grid(row = 2, column = i + 1, sticky = NSEW)

        self.bind('<Destroy>', lambda event: self.__onClose())
        self.show()

    def setInitialValue(self, initialValue):
        self.findEntry.insert(0, initialValue)
        if not self.initialValue and initialValue:
            self.findEntry.select_range(0, END)
        self.initialValue = initialValue

    def setOnFindNextListner(self, listener):
        '''listner should have exactly 2 arguments: target and direction'''
        self.findNextListner = listener

    def findNext(self):
        if self.findNextListner:
            self.findNextListner(self.findEntry.get(), self.getDirection())

    def setOnCloseListener(self, listener):
        self.closeListener = listener

    def close(self):
        self.__onClose()
        self.destroy()

    def __onClose(self):
        if self.closeListener:
            self.closeListener()

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
        self.findLabel = Label(self, text = 'Find:')
        self.findEntry = Entry(self)
        for i, w in enumerate([self.findLabel, self.findEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)