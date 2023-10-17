import random
import pprint
class Cell:
    __slots__ = 'pos', 'state', 'age'
    def __init__(self, pos:tuple|list, state=0, age=0):
        self.pos = pos
        self.state = state
        self.age = age

    def set_state(self, state:int):
        self.state = state

    def inc_age(self):
        self.age += 1

    def copy(self):
        return Cell(self.pos, self.state, self.age)


    #Works
    def my_neighbors(self, lim):
        pos_x, pos_y = self.pos
        right, x_middle, left = pos_x+1, pos_x, pos_x-1
        top, y_middle, bottom = pos_y-1, pos_y, pos_y+1
        neighbors = [
            (left, top),
            (x_middle, top),
            (right, top),
            (left, y_middle),
            (right, y_middle),
            (left, bottom),
            (x_middle, bottom),
            (right, bottom)
        ]
        clean_neighbors = []
        for n in neighbors:
            n_x, n_y = n
            if n_x < 0 or n_x > lim or n_y < 0 or n_y > lim:
                continue
            else:
                clean_neighbors.append(n)
        return clean_neighbors

    def __str__(self):
        return '[Positon: '+ str(self.pos) + ', State: ' + str(self.state) + ', Age: ' + str(self.age) + ' ]'

    def __repr__(self):
        res = '[Positon: '+ str(self.pos) + ', State: ' + str(self.state) + ', Age: ' + str(self.age) + ' ]'
        return res

class World_Manager:
    def __init__(self, size:int):
        self.world = {}
        self.SIZE = size
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                self.world[(x,y)] = Cell((x,y))

    def toggleCell(self, pos:tuple):
        try:
            state = int(not self.world[pos].state)
            if state == 1:
                self.world[pos].inc_age()
            self.world[pos].set_state(state)
        except KeyError:
            raise KeyError(pos)

    def random_init(self, weights:list|tuple):
        choices = [1,0]
        for k, v in self.world.items():
            state = random.choices(choices, weights, k=1)
            self.world[k].set_state(state[0])
            if state == 1:
                self.world[k].inc_age()

    def judge(self):
        new_cells = {}
        for pos, cell in self.world.items():
            neigh_pos = cell.my_neighbors(self.SIZE-1)
            match cell.state:
                case 1:
                    neigh_alive = 0
                    for c in neigh_pos:
                        neigh_cell = self.world[c]
                        if neigh_cell.state == 1:
                            neigh_alive += 1
                    if 2 <= neigh_alive <= 3:
                        cell.inc_age()
                        new_cells[pos] = cell.copy()
                    else:
                        new_cells[pos] = Cell(pos)
                case 0:
                    neigh_alive = 0
                    for c in neigh_pos:
                        neigh_cell = self.world[c]
                        if neigh_cell.state == 1:
                            neigh_alive += 1
                    if neigh_alive == 3:
                        new_cells[pos] = Cell(pos, state=1, age=1)
                    else:
                        new_cells[pos] = cell.copy()
        self.world = new_cells.copy()





if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    w = World_Manager(5)
    w.toggleCell((2,1))
    w.toggleCell((2,2))
    w.toggleCell((2,3))
    #w.toggleCell((2,4))
    pp.pprint(w.world)
    w.judge()
    print()
    pp.pprint(w.world)
    w.judge()
    print()
    pp.pprint(w.world)
    
   
