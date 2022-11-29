#Johnny Biederman
#Game of Life, colorized
#Built for Automata and Complexity Theory

import random
import numpy as np
import pygame
import time
from pygame.locals import * #apparently important to do
pygame.init()

class Cell(pygame.sprite.Sprite):
    def __init__(self, r, g, b):
        super(Cell, self).__init__()
        self.surf = pygame.Surface((23, 23))
        self.surf.fill((r, g, b))
        self.rect = self.surf.get_rect()

#different colors the cell can be
CellR = Cell(255,0,0)
CellO = Cell(255,128,0)
CellY = Cell(255,255,0)
CellG = Cell(128,255,0)
CellB = Cell(0,128,255)
CellW = Cell(255,255,255)

#MATRIX SETUP AND FUNCTIONS

n = 25 #side length of our grid
choices = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

matrix = np.zeros((n,n,2), dtype = int)
matrix2 = np.zeros((n,n,2), dtype = int)


def getN(x,y):
    return matrix[(x-1)%n][y][0]

def getS(x,y):
    return matrix[(x+1)%n][y][0]

def getE(x,y):
    return matrix[x][(y+1)%n][0]

def getW(x,y):
    return matrix[x][(y-1)%n][0]
    
def getNW(x,y):
    return matrix[(x-1)%n][(y-1)%n][0]
    
def getNE(x,y):
    return matrix[(x-1)%n][(y+1)%n][0]
    
def getSW(x,y):
    return matrix[(x+1)%n][(y-1)%n][0]
    
def getSE(x,y):
    return matrix[(x+1)%n][(y+1)%n][0]

def swap():
    for x in range(n):
        for y in range(n):
            matrix[x][y][0] = matrix2[x][y][0]
            matrix[x][y][1] = matrix2[x][y][1]
            matrix2[x][y][0] = 0
            
def colorupdate(cell, status):
    #if the cell is dead
    if status == 0:
        if cell == 0:
            cell = 0
        else:
            cell -= 1
            
    #if the cell is alive
    else:
        if cell == 5:
            cell = 5
        else:
            cell += 1
    return cell

def cellpicker(z):
    if z == 0:
        background.blit(CellW.surf, (y*25, x*25))
    elif z == 1:
        background.blit(CellB.surf, (y*25, x*25))
    elif z == 2:
        background.blit(CellG.surf, (y*25, x*25))
    elif z == 3:
        background.blit(CellY.surf, (y*25, x*25))
    elif z == 4:
        background.blit(CellO.surf, (y*25, x*25))
    elif z == 5:
        background.blit(CellR.surf, (y*25, x*25))

def update():
    for x in range(n):
        for y in range(n):
            neighbors = 0
            neighbors += getN(x,y)
            neighbors += getS(x,y)
            neighbors += getE(x,y)
            neighbors += getW(x,y)
            neighbors += getNW(x,y)
            neighbors += getNE(x,y)
            neighbors += getSW(x,y)
            neighbors += getSE(x,y)
                
            if neighbors == 3:
                matrix2[x][y][0] = 1
                matrix2[x][y][1] = colorupdate(matrix2[x][y][1], 1)
                
            elif matrix[x][y][0] == 1:
                if neighbors == 2:
                    matrix2[x][y][0] = 1
                    matrix2[x][y][1] = colorupdate(matrix2[x][y][1], 1)
                
            else:
                matrix2[x][y][0] = 0
                matrix2[x][y][1] = colorupdate(matrix2[x][y][1], 0)
    swap()
                    
    
#populate the matrix
def randstart():
    for x in range(n):
        for y in range(n):
            matrix[x][y][0] = 0
            matrix[x][y][1] = 0
            
    for x in range(n):
        for y in range(n):
            matrix[x][y][0] = random.choices(choices)[0]
            if matrix[x][y][0] == 1:
                matrix[x][y][1] == 1


#set the background
background = pygame.display.set_mode((n*25, n*25)) #each square is 25 by 25 pixels
background.fill((255,255,255))

gameOn = True
paused = True
pygame.display.set_caption('Game of Life - paused')

#gameplay loop
while gameOn:
    for x in range(n):
        for y in range(n):
            #if cell is alive
            if matrix[x][y][0] == 1:
                cellpicker(matrix[x][y][1])
                
            #if cell is dead
            else:
                background.blit(CellW.surf, (y*25, x*25))
                matrix[x][y][1] = colorupdate(matrix[x][y][1], 0)#(cell number, it is dead)
    
    if not paused:
        time.sleep(.25)
        update()
        
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            gameOn = False  
        elif event.type == QUIT:
            gameOn = False
            
        elif event.type == KEYDOWN and event.key == K_r:
            randstart()
            
        elif event.type == KEYDOWN and event.key == K_SPACE:
            paused = not paused
            if paused:
                print("paused")
                pygame.display.set_caption('Game of Life - paused')
            else:
                print("resumed")
                pygame.display.set_caption('Game of Life - running')
                
        elif event.type == MOUSEBUTTONDOWN: #what happens when you click
            sqX = event.pos[0]- (event.pos[0] % 25)
            sqY = event.pos[1] - (event.pos[1] % 25)
             
            if matrix[int(sqY/25)][int(sqX/25)][0] == 0:      
                background.blit(CellB.surf, (sqX, sqY))
                matrix[int(sqY/25)][int(sqX/25)][0] = 1
                matrix[int(sqY/25)][int(sqX/25)][1] = 1
            else:
                background.blit(CellW.surf, (sqX+1, sqY+1))
                matrix[int(sqY/25)][int(sqX/25)][0] = 0
                matrix[int(sqY/25)][int(sqX/25)][1] = 0
             
    
    pygame.display.flip() #update screen
pygame.display.quit() #closes the window