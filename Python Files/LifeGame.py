import random
from tkinter import *
import time
import threading

class LifeGame(Frame):
    # Rules:
    # 1. A life dies when the number of surrounding lives is less than 2
    # 2. A life dies when the number of surrounding lives is greater than 3
    # 3. A dead revives when the number of surrounding lives is 3
    # 4. A life stays the same when the number of surrounding lives is 2 or 3
    def __init__(self, parent, grid: list = None, interval: float = 1, cell_size: int = 5):
        Frame.__init__(self, parent)
        self.grid = [list(map(bool, row)) for row in grid]
        self.interval = interval
        self.cell_size = cell_size
        self.hcells = len(self.grid[0])
        self.vcells = len(self.grid)
        self.canvas = Canvas(self,
                             height = self.vcells * self.cell_size,
                             width = self.hcells * self.cell_size)
        self.canvas.pack()
        self.start()

    def draw_cell(self, x, y, alive: bool):
        loc_x = x * self.cell_size
        loc_y = y * self.cell_size
        self.canvas.create_rectangle(loc_x, loc_y,
                                     loc_x + self.cell_size,
                                     loc_y + self.cell_size,
                                     fill = [None, 'black'][alive])

    def start(self):
        self.running = True
        def func():
            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    if cell:
                        self.draw_cell(i, j, cell)
            print('Done Initing')
            while self.running:
                time.sleep(self.interval)
                if self.running:
                    self.endOfTurn()
                    print('End of turn')
            print('Stopped.')
        self.thread = threading.Thread(target=func)
        self.thread.start()

    def endOfTurn(self):
        newCells = []
        for i, row in enumerate(self.grid):
            newRow = []
            for j, cell in enumerate(row):
                surrounding = []
                up = i > 0
                left = j > 0
                down = i + 1 < self.hcells
                right = j + 1 < self.vcells
                if left:
                    surrounding.append(row[j - 1])
                    if up:
                        surrounding.append(self.grid[i - 1][j - 1])
                if up:
                    surrounding.append(self.grid[i - 1][j])
                    if right:
                        surrounding.append(self.grid[i - 1][j + 1])
                if right:
                    surrounding.append(row[j + 1])
                    if down:
                        surrounding.append(self.grid[i + 1][j + 1])
                if down:
                    surrounding.append(self.grid[i + 1][j])
                    if left:
                        surrounding.append(self.grid[i + 1][j - 1])
                alive = surrounding.count(True)
                new = alive == 3 or (alive == 2 and cell)
                if new != cell:
                    self.draw_cell(i, j, new)
                newRow.append(new)
            newCells.append(newRow)
        self.grid = newCells

    def stop(self):
        self.running = False

if __name__=='__main__':
    grid = [[0] * 300 for _ in range(300)]
    grid[50][50] = grid[50][51] = grid[51][51] = 1
    root = Tk()
    game = LifeGame(root, grid)
    game.pack()
    root.mainloop()
    game.stop()
