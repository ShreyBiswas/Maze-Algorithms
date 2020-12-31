
#* **** MAZE GENERATOR ****
#       by Shrey Biswas


#* IMPORTS
import random
import time
import pygame


time.sleep(0)
random.randint(0,1)

#* specifications
screenWidth = 1000
screenHeight = 500
FPS = 60
cellWidth = 20

#* colours
BLUE  = pygame.Color((0, 0, 255))
RED   = pygame.Color((255, 0, 0))
GREEN = pygame.Color((0, 255, 0))
BLACK = pygame.Color((0, 0, 0))
WHITE = pygame.Color((255, 255, 255))
TURQ  = pygame.Color((0, 200, 255))

#* initialise display
# pylint: disable=no-member
pygame.init()


window = pygame.display.set_mode((screenWidth,screenHeight))
window.fill(BLACK)
pygame.display.set_caption('Maze')
FramesPerSec = pygame.time.Clock()

def build_blank_grid():
    x = 20   #* x axis co-ordinates
    y = 0   #* y axis co-ordinates
    grid = []
    cellWidth = 20

    cellsY = (screenHeight//cellWidth)-1 #* total number of cells fitting on y axis
    cellsX = (screenWidth//cellWidth)-1  #* total number of cells fitting on x axis

    for i in range(1,cellsY):
        x = cellWidth      #* reset to start of line
        y += cellWidth     #* move down to next row of cells

        for ii in range(1,cellsX):
            pygame.draw.line(window, WHITE, [x, y], [x + cellWidth, y])                           #* top of cell
            pygame.draw.line(window, WHITE, [x + cellWidth, y], [x + cellWidth, y + cellWidth])   #* right of cell
            pygame.draw.line(window, WHITE, [x + cellWidth, y + cellWidth], [x, y + cellWidth])   #* bottom of cell
            pygame.draw.line(window, WHITE, [x, y + cellWidth], [x, y])                           #* left of cell

            grid.append((x,y))                                            #* add cell to grid list

            x += cellWidth
    return grid

def find_frontier(cellWidth, cell, grid, visited):
    x,y = cell[0],cell[1]
    right = (x+cellWidth,y)
    left = (x-cellWidth,y)
    above = (x,y-cellWidth)
    below = (x,y+cellWidth)

    surrounding = [(above,'above'),(below,'below'),(right,'right'),(left,'left')]
    frontier = []
    for i in range(len(surrounding)):        
        if (surrounding[i][0] in visited) == False and (surrounding[i][0] in grid) == True:
            frontier.append(surrounding[i])

    return frontier


def move(current,direction, cellWidth):

    x = current[0]
    y = current[1]


    if direction == 'start':    #* green square fills cell
        pygame.draw.rect(window, TURQ, (x+1, y+1, cellWidth-2, cellWidth-2),0)
        pygame.display.update()
        time.sleep(0.025)
        pygame.draw.rect(window, BLUE, (x+1, y+1, cellWidth-1, cellWidth-1),0)
    elif direction == 'above':  #* blue square fills cell, white fills neighbour
        pygame.draw.rect(window, WHITE, (x+1, y-cellWidth+1, cellWidth-2, cellWidth-2),0)
        pygame.draw.rect(window, BLUE, (x+1, y, cellWidth-1, cellWidth),0)
    elif direction == 'below':
        pygame.draw.rect(window, WHITE, (x+1, y+cellWidth+1, cellWidth-2, cellWidth-2),0)
        pygame.draw.rect(window, BLUE, (x+1, y+1, cellWidth-1, cellWidth),0)
    elif direction == 'right':
        pygame.draw.rect(window, WHITE, (x+cellWidth+1, y+1, cellWidth-2, cellWidth-2),0)
        pygame.draw.rect(window, BLUE, (x+1, y+1, cellWidth, cellWidth-1),0)
    elif direction == 'left':
        pygame.draw.rect(window, WHITE, (x-cellWidth+1, y+1, cellWidth-2, cellWidth-2),0)
        pygame.draw.rect(window, BLUE, (x, y+1, cellWidth, cellWidth-1),0)


    pygame.display.update()


def generate_maze(grid, cellWidth):

    visited = []
    stack = []

    current = grid[0]
    newCell = ((0,0),'start')
    visited.append(current)
    stack.append(current)

    while len(stack)>0:

        time.sleep(0.008)


        frontier = find_frontier(cellWidth,current, grid, visited)
        if len(frontier) != 0:

            newCell = random.choice(frontier)
            move(current,newCell[1], cellWidth)

            current = newCell[0]
            visited.append(current)
            stack.append(current)

        else:
            current = stack.pop()
            move(current, 'start', cellWidth)   #move back along stack

    







grid = build_blank_grid()

generate_maze(grid,cellWidth)


# ##### pygame loop #######
running = True
while running:


    # keep running at the at the right speed
    FramesPerSec.tick(FPS)
    pygame.display.update()


    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
