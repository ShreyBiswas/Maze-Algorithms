
#* **** A* SEARCH ****
#       by Shrey Biswas


#* IMPORTS
import random
import pygame
from sys import exit
from time import sleep
from Maze_Generator import build_blank_grid, add_blocks, generate_maze
from screen_details import *

# pylint: disable=no-member
#* PARAMETERS
maze = False
if not maze: # maze cannot be diagonal
    diagonal = False



grid = build_blank_grid()
grid = add_blocks(grid)
if maze:
    grid = generate_maze(grid,animate=False)


for row in grid: # reset
    for cell in row:
        cell.visited = False
        cell.cost = float('inf') #* placeholder infinite cost, will be replaced
        cell.start_cost = float('inf')

def cost(cell,target_cell):
    if cell.weight != 1:
        print('a')
    start_cost = cell.parent.start_cost + 1

    #* Pythagorean Theorem to estimate cost
    end_cost = (((target_cell.position[0]-cell.position[0]))**2+((target_cell.position[1]-cell.position[1]))**2)**0.5


    cost = start_cost + end_cost + cell.weight

    if start_cost<cell.start_cost:
        cell.start_cost = start_cost
    if cost<cell.cost:
        cell.cost = cost

    return cell.cost



def A_Star_Search(grid):

    for row in grid: # find start and target cells
        for cell in row:
            if cell.cell_type == 'Start':
                start_cell = cell
            elif cell.cell_type == 'Target':
                target_cell = cell

    frontier = []
    current_cell = start_cell
    current_cell.start_cost = 0
    current_cell.cost = ((target_cell.corner[0]-current_cell.corner[0])**2+(target_cell.corner[1]-current_cell.corner[1])**2)**1/2


    #* Search

    while current_cell != target_cell:

        current_cell.visited = True

        if not maze:    #* maze cells already have 'children' with set values, non-maze is empty
            current_cell.find_neighbours(grid,diagonal)

        for cell in current_cell.children:
            cell.parent = current_cell

        #* filter out cells already in frontier, blocked, or visited
        frontier = list(filter(lambda cell: cell not in current_cell.children and cell.cell_type != 'Block' and not cell.visited,frontier))

        frontier += current_cell.children
        random.shuffle(frontier)

        frontier.sort(key=lambda cell: cost(cell,target_cell))
        try:
            next_cell = frontier.pop(0)
        except:
            print('No Solution')
            pygame.quit()
            exit()


        next_cell.draw(PINK)

        pygame.display.update()
        sleep(cellWidth/1500)

        current_cell.draw(RED)

        current_cell = next_cell


    route = []
    #* Trace path back
    while current_cell != start_cell:
        route.append(current_cell)

        next_cell = current_cell.potential_parents[0] # first parent is the quickest route (earliest to be highlighted)

        next_cell.draw(TURQ)

        current_cell.connect(next_cell,GREEN,diagonal)

        pygame.display.update()
        sleep(cellWidth/4000)


        current_cell = next_cell

    return route

################################################################

#* main

A_Star_Search(grid)

while True:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
