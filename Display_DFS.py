
#* **** DEPTH-FIRST SEARCH ****
#       by Shrey Biswas


#* IMPORTS
import random
import pygame
from sys import exit
from time import sleep
from Display_Maze_Generator import *
from screen_details import *

#* PARAMETERS
maze = True
if not maze: # maze cannot be diagonal
    diagonal = False

# pylint: disable=no-member

grids = []
n = 1
for i in range(n):
    window.fill(BLACK)
    print(f'Grid {i} of {n} prepared.')
    grid = build_blank_grid()
    start = (random.choice(list(range(8))+list(range(15,23))),random.choice(list(range(20))+list(range(28,48))))
    end = ((start[0]+random.randint(8,14))%23,(start[1]+random.randint(15,25))%48)
    try:
        start = grid[start[0]][start[1]]
        end = grid[end[0]][end[1]]
    except:
        print(start,end)

    grid = add_blocks(grid,start,end)

    for row in grid: # reset
        for cell in row:
            cell.visited = False

    grids.append(grid)
print('Done')



def Depth_First_Search(grid):

    for row in grid: # find start and target cells, display correct board
        for cell in row:
            if not maze:
                cell.draw(WHITE)

            if cell.cell_type == 'Start':
                start_cell = cell
                start_cell.draw(RED)
            elif cell.cell_type == 'Target':
                target_cell = cell
                target_cell.draw(YELLOW)
            elif cell.cell_type == 'Block':
                print(cell.cell_type)
                cell.draw(BLACK)
    print(start_cell.corner)
    print([cell.corner for cell in start_cell.children])
    pygame.display.update()
    sleep(1)
    start_cell.draw(BLUE)
    sleep(3)

    frontier = []
    current_cell = start_cell

    #* Search

    while current_cell != target_cell:
        sleep(1)
        current_cell.visited = True

        if not maze:    #* maze cells already have 'children' with set values, non-maze is empty
            current_cell.find_neighbours(grid,diagonal)
        else:
            print([cell.corner for cell in current_cell.children])

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

        while current_cell not in next_cell.potential_parents: #* backtracks current_cell towards next_cell if dead end

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
for grid in grids:
    window.fill(BLACK)
    if maze:
        grid = generate_maze(grid,animate=False)
    pygame.display.update()
    sleep(1)
    Depth_First_Search(grid)
    sleep(2)

while True:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
