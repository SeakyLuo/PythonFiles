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
    def __init__(self, parent, grid: list = None, interval: float = 0.05, cell_size: int = 5):
        Frame.__init__(self, parent)
        self.grid = [list(map(bool, row)) for row in grid] if grid else LifeGame.randomGrid()
        self.interval = interval
        self.cell_size = cell_size
        self.hcells = len(self.grid[0])
        self.vcells = len(self.grid)
        self.cells = {}
        self.canvas = Canvas(self,
                             height = self.vcells * self.cell_size,
                             width = self.hcells * self.cell_size)
        self.canvas.pack()
        self.start()

    def draw_cell(self, x, y, alive: bool):
        loc_x = x * self.cell_size
        loc_y = y * self.cell_size
        if alive:
            cell = self.canvas.create_rectangle(loc_x, loc_y,
                                                loc_x + self.cell_size,
                                                loc_y + self.cell_size,
                                                fill = 'black')
            self.cells[(x, y)] = cell
        else:
            self.canvas.delete(self.cells[(x, y)])
            del self.cells[(x, y)]

    def start(self):
        self.cells.clear()
        self.pause = False
        self.running = True
        def func():
            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    if cell:
                        self.draw_cell(i, j, cell)
            print('Done Initing')
            while self.running:
                time.sleep(self.interval)
                if self.pause:
                    pass
                elif self.running:
                    self.endOfTurn()
                    print('End of turn')
            print('Stopped.')
        self.thread = threading.Thread(target=func)
        self.thread.start()

    def endOfTurn(self):
        newGrid = []
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
                if new != cell: self.draw_cell(i, j, new)
                newRow.append(new)
            newGrid.append(newRow)
        self.grid = newGrid

    def resume(self):
        self.pause = False

    def pause(self):
        self.pause = True

    def stop(self):
        self.running = False

    def getNewGrid(grid):
        hmax = len(grid[0])
        vmax = len(grid)
        newGrid = []
        for i, row in enumerate(grid):
            newRow = []
            for j, cell in enumerate(row):
                surrounding = []
                up = i > 0
                left = j > 0
                down = i + 1 < hmax
                right = j + 1 < vmax
                if left:
                    surrounding.append(row[j - 1])
                    if up:
                        surrounding.append(grid[i - 1][j - 1])
                if up:
                    surrounding.append(grid[i - 1][j])
                    if right:
                        surrounding.append(grid[i - 1][j + 1])
                if right:
                    surrounding.append(row[j + 1])
                    if down:
                        surrounding.append(grid[i + 1][j + 1])
                if down:
                    surrounding.append(grid[i + 1][j])
                    if left:
                        surrounding.append(grid[i + 1][j - 1])
                alive = surrounding.count(True)
                new = alive == 3 or (alive == 2 and cell)
                newRow.append(new)
            newGrid.append(newRow)
        return newGrid

    def print(grid):
        for row in grid:
            print(list(map(int, row)))

    def randomGrid():
        grid = [[0] * 300 for _ in range(300)]
        rand = random.randint(0, 2)
        num = 2 # rand
        if num == 0:
            grid[50][50] = grid[51][51] = grid[49][52] = grid[50][52] = grid[51][52] = 1
        elif num == 1:
            grid[30][30] = grid[31][30] = grid[32][30] = grid[36][30] = grid[37][30] = grid[38][30] = 1
            grid[34][26] = grid[34][27] = grid[34][28] = grid[34][32] = grid[34][33] = grid[34][34] = 1
        elif num == 2:
            for i in range(10):
                grid[30][30 + i] = 1
        return grid

if __name__=='__main__':
    root = Tk()
    game = LifeGame(root)
    game.pack()
    root.mainloop()
    game.stop()
