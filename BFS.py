import pygame
import Maze_Generator as generator
import time

#* construct maze
cellWidth = 20
grid = generator.build_blank_grid()
pathDict = generator.generate_maze(grid,cellWidth,False)

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

        time.sleep(0.01)

    while newCell[0]!=start:
        newCell = backDict[current]
        highlight(current,newCell[0],cellWidth,'solve')
        current = newCell[0]
        time.sleep(0.05)

    
    
    
    
    
    
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    current = start
    frontier.append(current)
    parentDict[current] = [current]
    newCell = current
    #* Search until destination is found
    while len(frontier)>0:

        #time.sleep(0.001)
        newCell = frontier.pop(0)

        possibleFrontier = generator.find_frontier(cellWidth,newCell,grid,visited)
        possibleFrontier = [node[0] for node in possibleFrontier]
        
        for node in possibleFrontier:
            try:
                parentDict[newCell].append[node]
            except:
                parentDict[newCell] = [node]
            frontier.append(node)
        
        frontier = list(dict.fromkeys(frontier))


        visited.append(current)
        highlight(current,newCell,cellWidth,'search')
        current = newCell
       '''

    #TODO: MAKE SURE TARGET CELL IS SCANNED, STOPS ABOVE. ADD REVERSING DICTIONARY FOR SOLUTION
'''
    print(list(parentDict.keys())[-5:])
    print(list(parentDict.values())[-5:])

    #* work backwords for optimal solution
    while True:
        newCell,current = parentDict[newCell],newCell
        highlight(current,newCell,cellWidth,'solution')
'''
def highlight(current,newCell,cellWidth,situ):
    if situ == 'search':
        pygame.draw.rect(generator.window, generator.RED, (current[0]+1, current[1]+1, cellWidth-1, cellWidth-1),0)
        pygame.draw.rect(generator.window, generator.WHITE, (newCell[0]+1, newCell[1]+1, cellWidth-1, cellWidth-1),0)
        pygame.display.update()
    else:
        pygame.draw.rect(generator.window, generator.GREEN, (current[0]+1, current[1]+1, cellWidth-1, cellWidth-1),0)
        pygame.draw.rect(generator.window, generator.WHITE, (newCell[0]+1, newCell[1]+1, cellWidth-1, cellWidth-1),0)
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



