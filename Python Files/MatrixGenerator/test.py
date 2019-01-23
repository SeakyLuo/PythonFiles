from tkinter import *

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

        self.findLabel = Label(self, text = 'Find:')
        self.findEntry = Entry(self)
        self.findEntry.focus()
        self.findEntry.select_range(0, END)
        for i, w in enumerate([self.findLabel, self.findEntry]):
            w.grid(row = 0, column = i, sticky = NSEW)
        self.findEntry.grid(columnspan = 5)
        self.findButton = Button(self, text = 'Find Next', command = self.find)
        self.findButton.grid(row = 1, column = i + 1, sticky = NSEW)
        self.bind('<Return>', lambda event: self.find())

    def setOnFindListner(self, listener):
        '''listner should have the following arguments: dialog, target, direction.'''
        self.findListner = listener

    def find(self):
        if not self.findListner: return
        self.findListner(self, self.findEntry.get())

def find():
    dialog = FindDialog(root)
    dialog.setOnFindListner(onFind)
    root.wait_window(dialog)

def onFind(*args):
    e.focus_set()
    e.select_range(0, END)
    e.icursor(END)

root = Tk()
e = Entry(root)
e.pack()
e.focus()
e.insert(0, 'HelloWorld')
root.bind('<Control-f>', lambda event: find())
root.mainloop()