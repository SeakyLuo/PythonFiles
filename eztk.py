from tkinter import END

def getText(text):
    return text.get(1.0, END).strip()

def clearText(text):
    text.delete(1.0, END)

def setText(text, content):
    text.insert(1.0, content)

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
    entry.bind('<FocusOut>', focusOut)
    setEntry(entry, hint)
    entry['fg'] = hintTextColor
