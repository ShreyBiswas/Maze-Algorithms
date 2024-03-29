
#* **** MAZE GENERATOR ****
#       by Shrey Biswas


#* IMPORTS
import random
import pygame
from time import sleep
from maze_objects import *
from screen_details import *

# pylint: disable=no-member

def build_blank_grid():
    x = 20   #* x axis co-ordinates of the top left cell
    y = 0   #* y axis co-ordinates of the top left cell
    grid = []

    cellsY = (screenHeight//cellWidth)-1 #* total number of cells fitting on y axis
    cellsX = (screenWidth//cellWidth)-1  #* total number of cells fitting on x axis

    for row_num in range(1,cellsY):
        #* begins at top left corner, works horizontally and moves down in line

        x = cellWidth      #* reset to start of line
        y += cellWidth     #* move down to next row of cell
        row = []

        for col_num in range(1,cellsX):
            cell = Node([x,y],cellWidth,window) #* create cell, add to row and draw
            row.append(cell)

            cell.draw(WHITE)
            cell.position = (row_num,col_num)


            x += cellWidth  #* move to next cell in row

        grid.append(row)
        #* [a],[b],[c]
        #* [d],[e],[f]
        #* [g],[h],[i]


    return grid

def add_blocks(grid):
    setup = True
    setup_stage = iter(['Start','Target','Block']) # weight1, weight2
    setup_action = next(setup_stage)
    print(setup_action)
    selecting = False

    while setup:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and setup_action in ('Weight1','Block'):
                try:
                    setup_action = next(setup_stage)
                    print(setup_action)
                except:
                    return grid

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if setup_action in ('Start','Target'): #* Selecting 'Start' or 'Target'
                    for row in grid:
                        for cell in row:
                            if cell.rect.collidepoint(event.pos):
                                cell.draw(YELLOW)
                                cell.cell_type = setup_action

                                setup_action = next(setup_stage) # advance if cell is clicked
                                print(setup_action)
                    continue


                selecting = True #* if blocking or weighting, lets you hold down


            elif event.type == pygame.MOUSEBUTTONUP:
                selecting = False

            elif event.type == pygame.MOUSEMOTION:
                if selecting:
                    #* check where click is
                    for row in grid:
                        for cell in row:
                            if cell.rect.collidepoint(event.pos):
                                if setup_action == 'Block':
                                    cell.draw(BLACK)
                                    cell.cell_type = 'Block'
                                elif setup_action == 'Weight1':
                                    cell.draw(GREY)
                                    cell.weight += 1




def generate_maze(grid,animate=True): #* Depth-First Generation

    for row in grid: # find start cell
        for cell in row:
            cell.children = [] # reset
            cell.visited = False

            if cell.cell_type == 'Start':
                current_cell = cell

    frontier = []

    while True:

        current_cell.visited = True
        current_cell.children=[] # empty children, to rebuild in maze
        current_cell.find_neighbours(grid,False) # maze cannot be diagonal

        random.shuffle(current_cell.neighbours)

        frontier = list(filter(lambda cell: cell not in current_cell.neighbours, frontier)) #* if neighbour is in frontier, move it to the end

        frontier+=current_cell.neighbours


        try:
            next_cell = frontier.pop(-1)
        except:
            break # if frontier is empty, maze is complete

        current_cell = backtrack(current_cell,next_cell,animate) #* if next_cell is not next to current_cell, finds proper parent
        next_cell.parent = current_cell
        current_cell.children.append(next_cell)

        next_cell.draw(CYAN)

        if animate:
            pygame.display.update()
            sleep(cellWidth/4000)

        current_cell.connect(next_cell,pygame.Color((202, 230, 255)),False) #diagonal not true
        current_cell = next_cell

        if animate:
            pygame.display.update()
            sleep(cellWidth/2000)

    pygame.display.update()
    return grid

def backtrack(current_cell, next_cell,animate):
    while current_cell not in next_cell.potential_parents: #* backtracks current_cell towards next_cell
            if animate:
                current_cell.draw(BLUE)
                current_cell.parent.draw(CYAN)
                sleep(cellWidth/3000)
                pygame.display.update()

            current_cell = current_cell.parent
    return current_cell

#* main
if __name__ == '__main__':
    grid = build_blank_grid()
    grid = add_blocks(grid)
    grid = generate_maze(grid,animate=True)

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()