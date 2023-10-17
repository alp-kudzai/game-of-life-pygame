import pygame as pg
from entities import Grid
import sys
import math


BLACK = (0,0,0)
WHITE = (200,200,200)
GREY = (127,127,127)
# WIN_WIDTH = 760
# WIN_HEIGHT = 760
GRID_SIZE = 100 # i.e GRID_SIZE * GRID_SIZE are the dimensions
CELL_SIZE = 2 # height and width of cell
MARGIN = 1 # dont go below 1

def calc_res():
    d = (GRID_SIZE * (CELL_SIZE + MARGIN)) + MARGIN
    return [d, d]

DIMENISION = calc_res()

class Game:
    def __init__(self):
        pg.init()

        pg.display.set_caption('Conway\'s Game of Life')

        self.screen = pg.display.set_mode(DIMENISION)

        self.clock = pg.time.Clock()

        self.screen.fill('black')

        self.grid = Grid(self, GRID_SIZE, CELL_SIZE, MARGIN)

        self.clicked = {}

        self.mouseDown = False

        self.font = pg.font.SysFont('Verdana', 20)

        self.fpsText = self.font.render(str(round(self.clock.get_fps())), True, (0,0,0))

    def renderFPStext(self):
        self.fpsText = self.font.render(str(round(self.clock.get_fps(),2)), True, (0,0,0))
        self.screen.blit(self.fpsText, (0,0))

    def mouseHeld(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        #print(event.pos)
        if self.mouseDown and not (mouse_x, mouse_y) in self.clicked: #if mouse pos is not in clicked
            x = mouse_x //(self.grid.cellSize + self.grid.margin)
            y = mouse_y //(self.grid.cellSize + self.grid.margin)
            #print(f'Clicked: {x},{y}')
            self.clicked[(mouse_x, mouse_y)] = True
            self.grid.toggleCell(x,y)

            
    def run(self):
        self.grid.intialise()
        
        running = True
        cycle = False

        while running:
            #User input
            self.screen.fill('black')
            if cycle:
                self.grid.cycle()
            self.grid.renderGrid()
            self.renderFPStext()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    left, mid, right = pg.mouse.get_pressed()
                    if left or right:
                        self.mouseDown = True
                if event.type == pg.MOUSEBUTTONUP:
                    self.mouseDown = False
                    self.clicked = {}
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        print('Space pressed!')
                        cycle = not cycle
                    if event.key == pg.K_r:
                        print('Randomising')
                        self.grid.randomInit()
                    if event.key == pg.K_c:
                        self.grid.clear()
                        print('clearing')
                    
                    #neighbors = self.grid.getNeighbors(x,y)
                    #print(neighbors)
                    # for c in neighbors:
                    #     self.grid.toggleCell(c[0],c[1])
                
            self.mouseHeld()      
            #self.screen.fill('black')
            
            pg.display.update()
            self.clock.tick(30)

Game().run()


