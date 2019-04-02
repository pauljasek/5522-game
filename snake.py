'''
Created by Channing Jacobs
3/28/19
'''

from enum import Enum
import random
import keyboard as kb
import time

class Cell:
    def __init__(self, x, y, cell_type):
        self.x = x
        self.y = y
        self.cell_type = cell_type

class Snake:
    def __init__(self, start_pos):
        self.head = start_pos
        self.body = list()
        self.body.append(self.head)
    
    # check
    def grow(self, nextCell):
        self.head = nextCell
        self.body.append(self.head)

    
    def move(self, nextCell):
        tail = self.body.pop()
        tail.cell_type = " "
        self.head = nextCell
        self.body.insert(0, self.head)
        self.head.cell_type = "s"

    def checkCrash(self, nextCell):
        for cell in self.body:
            if cell == nextCell:
                return True
        return False

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = [[Cell(x,y," ") for x in range(rows)] for y in range(cols)]
    
    def generateFood(self):
        while True:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            #self.matrix[row][col].cell_type = "f"
            cell = self.matrix[row][col]
            if(cell.cell_type == " "):
                cell.cell_type = "f"
                self.matrix[row][col] = cell
                break

class Direction(Enum):
    NONE = 0,
    UP = 1,
    RIGHT = 2,
    DOWN = 3,
    LEFT = 4

class Game:
    def __init__(self, snake, grid):
        self.score = 0
        self.snake = snake
        self.grid = grid
        self.game_over = False
        self.direction = Direction.RIGHT

    def update(self):
        if self.game_over == False:
            if self.direction != Direction.NONE:
                nextCell = self.getNextCell(self.snake.head)
                if (nextCell == "crash") or self.snake.checkCrash(nextCell):
                    self.direction = Direction.NONE
                    self.game_over = True
                    self.score -= 10
                else:
                    if nextCell.cell_type == "f":
                        self.score += 1
                        self.snake.grow(nextCell)
                        self.grid.generateFood()
                    self.snake.move(nextCell)
  
    def getNextCell(self, current_cell):
        row = current_cell.y
        col = current_cell.x
        if self.direction == Direction.RIGHT:
            col += 1
        elif self.direction == Direction.LEFT:
            col -= 1
        elif self.direction == Direction.UP:
            row -= 1
        elif self.direction == Direction.DOWN:
            row += 1
        if (row > self.grid.rows - 1) or (row < 0) or (col > self.grid.cols - 1) or (col < 0):
            return "crash"
        return self.grid.matrix[row][col]

def getPressedKey(prev_direction):
    if kb.is_pressed('up'):
        return Direction.UP
    if kb.is_pressed('left'):
        return Direction.LEFT
    if kb.is_pressed('right'):
        return Direction.RIGHT
    if kb.is_pressed('down'):
        return Direction.DOWN
    return prev_direction
    

if __name__ == "__main__":
    grid = Grid(10,10)
    snake = Snake(Cell(5,5,"s"))
    game = Game(snake, grid)
    game.direction = Direction.RIGHT
    game.grid.generateFood()

    t = 1
    i = 0
    #time = time.time()
    while game.game_over == False:
        #time = time - time.time()
        #print(time)
        t = (t + 1) % 4000
        game.direction = getPressedKey(game.direction)
        if t == 0:
            i += 1
            #print(i)
            game.update()
            s = ""
            for row in game.grid.matrix:
                s = ""
                for entry in row:
                    s += entry.cell_type
                print(s)