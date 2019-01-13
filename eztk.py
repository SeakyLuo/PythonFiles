from tkinter import END

def gettxt(text):
    return text.get(1.0, END).strip()

def deltxt(text):
    text.delete(1.0, END)

def instxt(textwidget, text):
    textwidget.insert(1.0, text)

def setEntry(entry, text):
    entry.delete(0, END)
    entry.insert(0, text)

def clearEntry(entry):
    entry.delete(0, END)

def setEntryHint(entry, hint, hintTextColor = 'grey39'):
    def focusIn(event):
        clearEntry(entry)
        entry['fg'] = color
    def focusOut(event):
        if not entry.get():
            setEntry(entry, hint)
            entry['fg'] = hintTextColor
    color = entry['fg']
    entry.bind('<FocusIn>', focusIn)
    entry.bind('<FocusOut>', focusIn)
    setEntry(entry, hint)
