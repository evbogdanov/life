import random
import time


################################################################################
### Cell
################################################################################

class Cell:
    DEAD = 0
    ALIVE = 1

    def __init__(self):
        self.is_alive = Cell.dead_or_alive()

    def __str__(self):
        return '*' if self.is_alive else ' '

    @staticmethod
    def dead_or_alive():
        return random.randint(Cell.DEAD, Cell.ALIVE) == Cell.ALIVE


################################################################################
### Life
################################################################################

class Life:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = {}
        for x in range(1, width+1):
            for y in range(1, height+1):
                xy = (x, y)
                self.cells[xy] = Cell()

    def __str__(self):
        s = ''
        for y in range(self.height, 0, -1):
            for x in range(1, self.width+1):
                xy = (x, y)
                cell = self.cells[xy]
                s += f'{cell}'
            s += '\n'
        return s

    def count_live_neighbours(self, x, y):
        counter = 0
        xys = ((x-1, y+1), (x, y+1), (x+1, y+1),
               (x-1,   y),           (x+1,   y),
               (x-1, y-1), (x, y-1), (x+1, y-1))
        for xy in xys:
            cell = self.cells.get(xy)
            if cell is not None and cell.is_alive:
                counter += 1
        return counter

    def step(self):
        changes = {}
        for xy in self.cells.keys():
            x, y = xy
            cell = self.cells[xy]
            counter = self.count_live_neighbours(x, y)
            if cell.is_alive:
                # Any live cell with fewer than two live neighbours dies, as if
                # caused by underpopulation.
                #
                # Any live cell with more than three live neighbours dies, as
                # if by overpopulation.
                if counter < 2 or counter > 3:
                    changes[xy] = False
            else:
                # Any dead cell with exactly three live neighbours becomes a
                # live cell, as if by reproduction.
                if counter == 3:
                    changes[xy] = True
        for xy in changes:
            self.cells[xy].is_alive = changes[xy]
        if not changes:
            return False  # No changes? No more steps.
        return True


################################################################################
### Main
################################################################################

def main():
    life = Life(40, 20)
    for _ in range(0, 300):
        time.sleep(1/30)
        print('\033[H')  # Move to the top
        print('\033[J')  # Clear screen
        more_steps = life.step()
        print(life)
        if not more_steps:
            break

if __name__ == '__main__':
    main()
