from tkinter import *
from tkinter import filedialog, messagebox
from collections import Counter
import ez, ezs, os, threading
from eztk import setEntry, clearEntry, LoadDialog
from ocr import image_to_matrix

class sudoku:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.grid(row = 0, column = 0)
        self.entries = {}
        for i in range(1, 10):
            for j in range(1, 10):
                e = Entry(self.frame, width = 3)
                e.grid(row = i - 1, column = j - 1)
                e.bind('<KeyRelease>', self.switch)
                self.entries[i, j] = e
        self.editButton = Button(self.master, text = '编辑', command = self.edit)
        self.computeButton = Button(self.master, text = '计算', command = self.compute)
        self.clear = Button(self.master, text = '清除', command = self.clear)
        self.clearAll = Button(self.master, text = '清除全部', command = self.setup)
        self.loadButton = Button(self.master, text = '加载', command = self.load)
        self.saveButton = Button(self.master, text = '保存', command = self.save)
        buttons = [self.editButton, self.computeButton, self.clear, self.clearAll, self.loadButton, self.saveButton]
        for i, button in enumerate(buttons):
            button.grid(row = 1, column = i, sticky = NSEW)
        self.frame.grid(columnspan = len(buttons))

        self.intermediates = 'intermediates'
        if self.intermediates not in os.listdir():
            os.mkdir(self.intermediates)
        self.setup('sudoku.txt')
        for entry in self.entries.values():
            if entry['state'] == NORMAL:
                entry.focus()
                break

    def isFull(self):
        return all(self.numbers.values())

    def clear(self):
        for (i, j), entry in self.entries.items():
            if entry['state'] == NORMAL:
                clearEntry(entry)

    def reset(self):
        self.hints = {(i, j): set(range(1, 10)) for i in range(1, 10) for j in range(1, 10)}
        self.numbers = {(i, j): 0 for i in range(1, 10) for j in range(1, 10)}

    def setup(self, filename = ''):
        for i in range(1, 10):
            for j in range(1, 10):
                self.entries[i, j]['state'] = NORMAL
                clearEntry(self.entries[i, j])
        if filename:
            if filename.endswith('.txt'):
                numbers = ez.fread(filename)
                self.setNumbers(numbers)
            else:
                dialog = LoadDialog(self.master, '正在识别图像')
                dialog.setCloseEvent(self.ocr_event, (filename, ))

    def setNumbers(self, numbers: dict):
        for (i, j), number in numbers.items():
            if number == 0: continue
            setEntry(self.entries[i, j], number)
            self.entries[i, j]['state'] = DISABLED

    def ocr_event(self, filename):
        numbers = image_to_matrix(filename, self.intermediates)
        if not numbers:
            messagebox.showerror(title='错误', message="无法识别图片")
        self.setNumbers(numbers)

    def edit(self):
        if self.editButton['text'] == '编辑':
            self.editButton['text'] = '完成'
            for entry in self.entries.values():
                entry['state'] = NORMAL
        else:
            self.editButton['text'] = '编辑'
            for entry in self.entries.values():
                if entry.get():
                    entry['state'] = DISABLED

    def compute(self):
        self.reset()
        self.collectNumbers()
        if sum(number != 0 for number in self.numbers.values()) < 17:
            messagebox.showerror(title='错误', message=f'数字太少，无法计算')
            return
        valid = self.isValid()
        if valid != True:
            i, j, text = valid
            messagebox.showerror(title='错误', message=f'第{i}行第{j}列存在非法输入：{text}')
            return
        dialog = LoadDialog(self.master, '正在计算')
        dialog.setCloseEvent(self.compute_event)

    def isValid(self):
        board = []
        for i in range(1, 10):
            row = []
            counter = {}
            for j in range(1, 10):
                try:
                    text = self.entries[i, j].get()
                    number = int(text or 0)
                    assert 0 <= number < 10
                    counter[number] = counter.get(number, 0) + 1
                    if number:
                        assert counter[number] == 1
                except:
                    return i, j, text
                row.append(number)
            board.append(row)
        for j in range(1, 10):
            counter = {}
            for i in range(1, 10):
                number = board[i - 1][j - 1]
                counter[number] = counter.get(number, 0) + 1
                if number and counter[number] > 1:
                    return i, j, number
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                counter = {}
                for x in range(3):
                    for y in range(3):
                        number = board[r + x][c + y]
                        counter[number] = counter.get(number, 0) + 1
                        if number and counter[number] > 1:
                            return r + x, c + y, number
        return True

    def compute_event(self):
        for (i, j), number in self.numbers.items():
            if number:
                self.put(i, j, number)
        self.solve()
        for loc, number in self.numbers.items():
            if number:
                setEntry(self.entries[loc], number)

    def solve(self) -> bool:
        if self.isFull():
            return True
        hints = { k: v for k, v in self.hints.items() if v }
        if not hints:
            return False
        i, j = loc = ezs.argmin(hints, len)
        copy = self.hints[loc].copy()
        for number in self.hints[loc].copy():
            hints = self.put(i, j, number)
            if self.solve():
                return True
            else:
                self.numbers[loc] = 0
                for x, y in hints:
                    self.hints[x, y].add(number)
                self.hints[loc] = copy.copy()
        return False

    def put(self, i, j, number) -> set:
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
                                              title = '选择数独',
                                              filetypes = [('文件','*.txt *.png *.jpg *.bmp')])
        if filename:
            self.setup(filename)

    def save(self):
        file = filedialog.asksaveasfile(initialdir = os.getcwd(),
                                        title = '保存数独',
                                        defaultextension = True,
                                        filetype = [('文本文件', '.txt')])
        if file:
            file.write(str(self.collectNumbers()))
            file.close()

    def collectNumbers(self) -> dict:
        for loc, entry in self.entries.items():
            self.numbers[loc] = int(entry.get() or 0)
        return self.numbers

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
ez.py2pyw(__file__)