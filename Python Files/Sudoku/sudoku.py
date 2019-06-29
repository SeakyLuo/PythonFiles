from tkinter import *
from tkinter import filedialog, messagebox
import ez, ezs, os, threading
from eztk import setEntry, clearEntry
from ocr import image_to_matrix

class sudoku:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.grid(row = 0, column = 0)
        self.entries = {}
        for i in range(1, 10):
            for j in range(1, 10):
                e = Entry(self.frame, width = 5)
                e.grid(row = i - 1, column = j - 1)
                e.bind('<KeyRelease>', self.switch)
                self.entries[i, j] = e
        self.computeButton = Button(self.master, text = '计算', command = self.compute)
        self.clear = Button(self.master, text = '清除', command = lambda: self.setup(self.currentPuzzle))
        self.clearAll = Button(self.master, text = '清除全部', command = self.setup)
        self.loadButton = Button(self.master, text = '加载', command = self.load)
        buttons = [self.computeButton, self.clear, self.clearAll, self.loadButton]
        for i, button in enumerate(buttons):
            button.grid(row = 1, column = i, sticky = NSEW)
        self.frame.grid(columnspan = len(buttons))

        self.intermediates = 'intermediates'
        if self.intermediates not in os.listdir():
            os.mkdir(self.intermediates)
        self.currentPuzzle = 'puzzle.txt'
        self.setup(self.currentPuzzle)
        for entry in self.entries.values():
            if entry['state'] == NORMAL:
                entry.focus()
                break

    def isFull(self):
        return all(self.numbers.values())

    def setup(self, filename = ''):
        self.hints = {(i, j): set(range(1, 10)) for i in range(1, 10) for j in range(1, 10)}
        self.numbers = {(i, j): 0 for i in range(1, 10) for j in range(1, 10)}
        for i in range(1, 10):
            for j in range(1, 10):
                self.entries[i, j]['state'] = NORMAL
                clearEntry(self.entries[i, j])
        if filename:
            numbers = {}
            if filename.endswith('.txt'):
                numbers = ez.fread(filename)
            else:
                matrix = image_to_matrix(filename, self.intermediates)
                if matrix:
                    numbers = { (x, y): matrix[x - 1][y - 1] for x, y in self.numbers }
                else:
                    messagebox.showerror(title="Error", message="Invalid Image!")
            for (i, j), number in numbers.items():
                if number:
                    setEntry(self.entries[i, j], number)
                    self.entries[i, j]['state'] = DISABLED
                    self.put(i, j, number)
        self.currentPuzzle = filename
        self.full = self.isFull()

    def compute(self):
        if self.full or all(number == 0 for number in self.numbers.values()):
            return
        self.solve() # create a thread to do it
        for i in range(1, 10):
            for j in range(1, 10):
                if self.numbers[i, j]:
                    setEntry(self.entries[i, j], self.numbers[i, j])
        self.full = True

    def solve(self):
        if self.isFull():
            return True
        hints = { k: v for k, v in self.hints.items() if v }
        if not hints:
            return False
        i, j = ezs.argmin(hints, len)
        copy = self.hints[i, j].copy()
        for number in self.hints[i, j].copy():
            hints = self.put(i, j, number)
            self.put(i, j, number)
            if self.solve():
                return True
            else:
                self.numbers[i, j] = 0
                for x, y in hints:
                    self.hints[x, y].add(number)
                self.hints[i, j] = copy.copy()
        return False

    def put(self, i, j, number):
        self.numbers[i, j] = number
        self.hints[i, j].clear()
        hints = set()
        for n in range(1, 10):
            for loc in [(n, j), (i, n), (3*((i-1)//3)+(n-1)//3+1, 3*((j-1)//3)+(n-1)%3+1)]:
                if number in self.hints[loc]:
                    self.hints[loc].remove(number)
                    hints.add(loc)
        return hints

    def load(self):
        filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                              title = 'Select a Puzzle',
                                              filetypes = [('Files','*.txt *.png *.jpg')])
        if filename:
            self.setup(filename)

    def switch(self, event):
        key = event.keysym
        move = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        if key not in move: return
        x, y = move[key]
        info = event.widget.grid_info()
        r = (info['row'] + x) % 9
        c = (info['column'] + y) % 9
        while self.entries[r + 1, c + 1]['state'] == DISABLED:
            r = (r + x) % 9
            c = (c + y) % 9
        self.entries[r + 1, c + 1].focus()

root = Tk()
s = sudoku(root)
root.title('Sudoku Solver')
root.mainloop()
