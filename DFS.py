
#* **** DEPTH-FIRST SEARCH ****
#       by Shrey Biswas


#* IMPORTS
import random
import pygame
from sys import exit
from time import sleep
from Maze_Generator import *
from screen_details import *

#* PARAMETERS
maze = False
diagonal = False
if not maze: # maze cannot be diagonal
    diagonal = True

# pylint: disable=no-member


grid = build_blank_grid()
grid = add_blocks(grid)
if maze:
    grid = generate_maze(grid,animate=False)


for row in grid: # reset
    for cell in row:
        cell.visited = False

def Depth_First_Search(grid):

    for row in grid: # find start and target cells
        for cell in row:
            if cell.cell_type == 'Start':
                start_cell = cell
            elif cell.cell_type == 'Target':
                target_cell = cell

    frontier = []
    current_cell = start_cell

    #* Search

    while current_cell != target_cell:
        #sleep(1)
        current_cell.visited = True

        if not maze:    #* maze cells already have 'children' with set values, non-maze is empty
            current_cell.find_neighbours(grid,diagonal)

        random.shuffle(current_cell.children)

        #* filter out cells already in frontier, blocked, or visited
        frontier = list(filter(lambda cell: cell not in current_cell.children and cell.cell_type != 'Block' and not cell.visited,frontier))

        frontier += current_cell.children

        try:
            next_cell = frontier.pop(-1)
        except:
            print('No Solution')
            pygame.quit()
            exit()


        while current_cell not in next_cell.potential_parents: #* backtracks current_cell towards next_cell

            current_cell.draw(RED)
            current_cell.parent.draw(MAGENTA)
            sleep(cellWidth/1000)
            pygame.display.update()

            current_cell = current_cell.parent

        next_cell.draw(PINK)

        pygame.display.update()
        sleep(cellWidth/1500)

        current_cell.draw(RED)
        next_cell.parent = current_cell
        current_cell = next_cell


    route = []
    #* Trace path back
    while current_cell != start_cell:
        route.append(current_cell)

        next_cell = current_cell.potential_parents[0] # first parent is the quickest route (earliest to be highlighted)

        next_cell.draw(TURQ)
        pygame.display.update()
        sleep(cellWidth/4000)
        current_cell.connect(next_cell,GREEN,diagonal)

        current_cell = next_cell

    return route

################################################################

#* main

Depth_First_Search(grid)

while True:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
