
#* **** BREADTH-FIRST SEARCH ****
#       by Shrey Biswas


#* IMPORTS
import random
import pygame
from sys import exit
from time import sleep
from Maze_Generator import *
from screen_details import *

#* PARAMETERS
maze = True
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

def Breadth_First_Search(grid):

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

        current_cell.visited = True
        if not maze:    #* maze already has 'children' with set values, non-maze is empty
            current_cell.find_neighbours(grid,diagonal)

        random.shuffle(current_cell.children)

        #* filter out cells already in frontier, blocked, or visited
        current_cell.children = list(filter(lambda cell: cell not in frontier and cell.cell_type != 'Block' and not cell.visited,current_cell.children))

        for cell in current_cell.children: # highlight parts of frontier
            cell.draw(PINK)

        frontier += current_cell.children

        try:
            next_cell = frontier.pop(0)
        except:
            print('No Solution')
            pygame.quit()
            exit()


        pygame.display.update()
        sleep(cellWidth/4000)

        if not maze:
            next_cell.connect(next_cell.parent,RED,diagonal)
        else:
            current_cell.draw(RED)

        current_cell = next_cell


    shortest_route = []
    #* Trace path back
    while current_cell != start_cell:
        shortest_route.append(current_cell)

        next_cell = current_cell.potential_parents[0] # first parent is the quickest route (earliest to be highlighted)

        next_cell.draw(TURQ)
        pygame.display.update()
        sleep(cellWidth/4000)
        current_cell.connect(next_cell,GREEN,diagonal)

        current_cell = next_cell

    return shortest_route


################################################################

#* main

Breadth_First_Search(grid)

while True:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
