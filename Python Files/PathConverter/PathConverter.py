from tkinter import *
import ez

class Converter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

root = Tk()
app = Converter(root)
app.pack()
root.title('Path Converter')
ez.py2pyw(__file__)
root.mainloop()
