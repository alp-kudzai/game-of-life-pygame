import pygame as pg
from collections import defaultdict
import copy
import random
import numpy as np

##TODO
# Explore a longer history with different color
# if numpy isnt any faster change back to a normal 2d array
# explore color based on popu. density (heat map)

class Cell:
    state = 0
    history = 0

class Grid:
    def __init__(self, game, gridSize, cellSize, margin):
        self.game = game
        self.cellSize = cellSize
        self.margin = margin
        self.gridSize = gridSize
        #self.gridmapArr = []
        self.gridmapArr = []
        self.npGrid = False

    def intialise(self):
        for y in range(self.gridSize):
            #x_container = []
            x_container = []
            for x in range(self.gridSize):
                x_container.append(Cell())
            self.gridmapArr.append(x_container)
        self.npGrid = np.array(self.gridmapArr)
        #self.gridmapArr[1][5] = 1
                
        #print(self.gridmap)

    def clear(self):
        newGrid = []
        for y in range(self.gridSize):
            x_container = []
            for x in range(self.gridSize):
                x_container.append(Cell())
            newGrid.append(x_container)
        self.npGrid = newGrid

    def randomInit(self):
        choices = [1,0]
        weights = [47, 50]
        newGridmapArr = []
        for y in range(self.gridSize):
            x_container = []
            for x in range(self.gridSize):
                st = random.choices(choices, weights, k=1)
                cell = Cell()
                cell.state = st[0]
                x_container.append(cell)
            newGridmapArr.append(x_container)
        self.npGrid = np.array(newGridmapArr)
        

    def toggleCell(self,x: int,y: int):
        try:
            cell = self.npGrid[y][x].state
            if cell == 1:
                self.npGrid[y][x].state = 0
            else:
                self.npGrid[y][x].state = 1
        except IndexError:
            pass

    def getNeighbors(self,x: int,y: int):
        '''
        Returns neighbors of a given cell, left to right, top to bottom.
        '''
        right, x_middle, left = x+1, x, x-1
        top, y_middle, bottom = y-1, y, y+1
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
        return neighbors

    def processNeighbors(self, neighbors: list):
        n_states = defaultdict(int)
        for c in neighbors:
            try:
                cell = self.npGrid[c[1]][c[0]].state
                if cell == 1:
                    n_states['alive'] += 1
            except IndexError:
                #print('processNeighbors IndexError!')
                pass
        return n_states

    def cycle(self):
        newGridmapArr = []
        for y in range(self.gridSize):
            x_container = []
            for x in range(self.gridSize):
                cell = self.npGrid[y][x].state
                #cell = x,y
                neighbors = self.getNeighbors(x, y)
                n_states = self.processNeighbors(neighbors)
                #if cell is alive and 2 or 3 neighs are alive
                newCell = Cell()
                if cell and (n_states['alive'] >= 2) and (n_states['alive'] <= 3):
                    newCell.state = 1
                    newCell.history = 1
                    x_container.append(newCell)
                elif not cell and (n_states['alive'] == 3):
                    newCell.state = 1
                    newCell.history = 0
                    x_container.append(newCell)
                else:
                    if cell:
                        newCell.history = 1
                    newCell.state = 0
                    newCell.history = 0
                    x_container.append(newCell)
            newGridmapArr.append(x_container)
        #self.gridmapArr.clear()
        self.npGrid = np.array(newGridmapArr)



    def renderGrid(self):
        for y in range(self.gridSize):
            for x in range(self.gridSize):
                arrCell = self.npGrid[y][x]
                color = 'purple'
                if arrCell.state == 1 and arrCell.history == 0:
                    color = 'orange'
                    #neighbors = self.getNeighbors(x,y)
                elif arrCell.state == 1 and arrCell.history == 1:
                    color = 'grey'
                cell = pg.Rect(((self.margin + self.cellSize) * x + self.margin), ((self.margin + self.cellSize) * y + self.margin), self.cellSize, self.cellSize)
                pg.draw.rect(self.game.screen, color, cell)

    
        


