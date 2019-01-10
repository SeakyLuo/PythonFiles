def gettxt(text):
    return text.get(1.0, 'end').strip()

def deltxt(text):
    text.delete(1.0, 'end')

def instxt(textwidget, text):
    textwidget.insert(1.0, text)

def setEntry(entry, text):
    entry.delete(0, 'end')
    entry.insert(0, text)

def clearEntry(entry):
    entry.delete(0, 'end')
