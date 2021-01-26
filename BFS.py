import pygame
import Maze_Generator as generator
import time

#* construct maze
cellWidth = 20
grid = generator.build_blank_grid(cellWidth)
pathDict = generator.generate_maze(grid,cellWidth,True)

parentDict = {}



def bf_search(grid, pathDict):
    start = grid[0]
    target = grid[-1]

    backDict = {}

    #* Reverse PathDict to show child->parent relationship
    for key, value in pathDict.items():
        try:
            if value in backDict:
                backDict[value].append(key)
            else:
                backDict[value]=[key]
        except:
            for child in value:
                if child in backDict:
                    backDict[child].append(key)
                else:
                    backDict[child]=[key]

    frontier = []

    current = start

    while current != target:
        try:
            frontier+=pathDict[current]
        except:
            pass

        newCell = frontier.pop(0)
        highlight(current,newCell,cellWidth,'search')

        current = newCell

        time.sleep((0.0000025*(cellWidth**3)))

    while newCell[0]!=start:
        newCell = backDict[current]
        highlight(current,newCell[0],cellWidth,'solve')
        current = newCell[0]
        time.sleep((0.000005*(cellWidth**3)))

def highlight(current,newCell,cellWidth,situ):
    if situ == 'search':
        pygame.draw.rect(generator.window, generator.RED, (current[0]+1, current[1]+1, cellWidth-1, cellWidth-1),0)
        pygame.draw.rect(generator.window, generator.WHITE, (newCell[0]+1, newCell[1]+1, cellWidth-1, cellWidth-1),0)
        pygame.display.update()
    else:
        pygame.draw.rect(generator.window, generator.GREEN, (current[0]+1, current[1]+1, cellWidth-1, cellWidth-1),0)
        pygame.draw.rect(generator.window, generator.GREY, (newCell[0]+1, newCell[1]+1, cellWidth-1, cellWidth-1),0)
        pygame.display.update()




#main
bf_search(grid,pathDict)

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



