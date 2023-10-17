import pygame as pg
import sys
from new_entities import World_Manager

class Game:
    def __init__(self):
        pg.init()
        #world setup
        self.world_size = 150
        self.cell_size = 2
        self.World = World_Manager(self.world_size)
        #FOR TESTING##################
        # self.World.toggleCell((2,1))
        # self.World.toggleCell((2,2))
        # self.World.toggleCell((2,3))
        self.World.random_init((40,60))
        ##############################

        self.FPS = 60
        self.DIMENSIONS = [self.world_size*self.cell_size]*2
        self.clock = pg.time.Clock()
        pg.display.set_caption('Conway\'s game of life')
        self.screen = pg.display.set_mode(self.DIMENSIONS)
        self.font = pg.font.SysFont('Verdana', 20)
        #self.fpsText = self.font.render(str(round(self.clock.get_fps())), True, (0,255,0))

    def renderWorld(self, surf):
        COLORS = ('black', 'white')
        for pos, cell in self.World.world.items():
            if cell.state == 0:
                cell_color = COLORS[0]
            else: cell_color = COLORS[1]
            cell_rect = pg.Rect((self.cell_size*pos[0], self.cell_size*pos[1]), (self.cell_size, self.cell_size))
            pg.draw.rect(surf, cell_color, cell_rect)

    def renderFPStext(self):
        self.fpsText = self.font.render(str(round(self.clock.get_fps(),2)), True, (0,255,0))
        self.screen.blit(self.fpsText, (0,0))

    def processInput(self):
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                    pg.quit()
                    sys.exit()
                

    def run(self):
        running = True
        while running:
            #check input
            self.processInput()

            self.screen.fill('black')
            self.World.judge()

            #Render here
            self.renderWorld(self.screen)
            self.renderFPStext()

            pg.display.flip()
            self.clock.tick(self.FPS)

Game().run()


