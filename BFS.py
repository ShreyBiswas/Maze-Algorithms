import pygame
import Maze_Generator as generator
import time

#* construct maze
cellWidth = 20
grid = generator.build_blank_grid()
generator.generate_maze(grid,cellWidth,False)

parentDict = {}

def bf_search(grid):
    start = grid[0]
    target = grid[-1]
    frontier = []
    visited = []

    current = start
    frontier.append(current)
    parentDict[current] = current
    newCell = current
    #* Search until destination is found
    while len(frontier)!=0:

        time.sleep(0.001)
        newCell = frontier.pop(0)
        

        possibleFrontier = generator.find_frontier(cellWidth,current,grid,visited)
        possibleFrontier = [node[0] for node in possibleFrontier]

        overlap = list(set(possibleFrontier).intersection(frontier))
        if len(overlap) != 0:
            for i in range(len(overlap)):   #* if a node is already detected, the route to it must be 
                possibleFrontier.remove(overlap[i]) #* longer, so it is discarded

        frontier += (possibleFrontier)
        visited.append(current)
        highlight(current,newCell,cellWidth,'search')
        parentDict[current] = newCell
        current = newCell

    
    #! BUG - NEWCELL AND TARGET DO NOT MATCH UP TO PARENTDICT, PARENTDICT DOES NOT SPAN GRID
    #TODO: FIX BUG, ALIGN PARENTDICT TO GRID

    #* work backwords for optimal solution
    while True:
        newCell,current = parentDict[newCell],newCell
        highlight(current,newCell,cellWidth,'solution')

def highlight(current,newCell,cellWidth,situ):
    if situ == 'search':
        pygame.draw.rect(generator.window, generator.RED, (current[0]+1, current[1]+1, cellWidth-2, cellWidth-2),0)
        pygame.draw.rect(generator.window, generator.WHITE, (newCell[0]+1, newCell[1]+1, cellWidth-2, cellWidth-2),0)
        pygame.display.update()
    else:
        pygame.draw.rect(generator.window, generator.GREEN, (current[0]+1, current[1]+1, cellWidth-2, cellWidth-2),0)
        pygame.draw.rect(generator.window, generator.WHITE, (newCell[0]+1, newCell[1]+1, cellWidth-2, cellWidth-2),0)
        pygame.display.update()


bf_search(grid)

# ##### pygame loop #######
running = True
while running:


    # keep running at the at the right speed
    FramesPerSec = pygame.time.Clock()
    FramesPerSec.tick(60)
    pygame.display.update()


    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False



