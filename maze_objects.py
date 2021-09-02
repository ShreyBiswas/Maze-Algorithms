import pygame
from screen_details import *

# pylint: disable=no-member

class Node():
    '''
    NODE CLASS

    Attributes:

    surf (pygame.Surf), rect (pygame.Rect), window (pygame.display): Display management
    corner: Quick access to top-left corner co-ordinate
    children: Nodes directly created by routing through this cell
    parent: The cell which this cell emerges from
    potential_parents: Nodes which can route through this cell
    cell_type: Block, Cell, Start, Target - Defines what role this cell plays
    visited: Whether this cell has previously been the active cell
    window
    neighbours: All cells directly above, below, to the left and right of this cell

    '''

    def __init__(self,top_left,width,window) -> None: #* Create Node object with corner, children, and parent
        top_left[0]+=1 #* add buffer distances between Nodes
        top_left[1]+=1
        width-=2

        self.surf = pygame.Surface((width,width))
        self.rect = pygame.Rect(top_left,(width,width))
        self.window = window
        self.corner = top_left


        self.children = []
        self.parent = None
        self.potential_parents = []
        self.cell_type = 'Cell'
        self.visited = False
        self.weight = 1

    def draw(self,colour):
        self.surf.fill(colour)
        self.window.blit(self.surf,self.rect)

    def connect(self,node,colour,diagonal):
        if diagonal:
            pygame.draw.line(self.window,colour,self.rect.center,node.rect.center,width=2)
        else:
            pygame.draw.rect(self.window,colour,self.rect.union(node.rect)) #* join the two cells

        if self.cell_type in ('Start','Target'):
            self.draw(YELLOW)

    def find_neighbours(self,grid,diagonal):
        self.neighbours = []

        for row in range(len(grid)): #* find the row and column of the cell in the grid
            try:
                col = grid[row].index(self)
                break
            except: pass

        try:
            if bool(col): #* check if left side exists (can't use -1, as that is an index)
                self.neighbours.append(grid[row][col-1]) #left
        except: pass
        try:
            self.neighbours.append(grid[row][col+1]) #right
        except: pass
        try:
            if bool(row): # check if above exists
                self.neighbours.append(grid[row-1][col]) #top
        except: pass
        try:
            self.neighbours.append(grid[row+1][col]) #bottom
        except: pass
        if diagonal:
            try:
                if bool(col) and bool(row): #* check if top and left side exists (can't use -1, as that is an index)
                    self.neighbours.append(grid[row-1][col-1]) # top-left
            except: pass
            try:
                if bool(row):
                    self.neighbours.append(grid[row-1][col+1]) # top-right
            except: pass
            try:
                if bool(col): # check if above exists
                    self.neighbours.append(grid[row+1][col-1]) # bottom-left
            except: pass
            try:
                self.neighbours.append(grid[row+1][col+1]) # bottom-right
            except: pass

        #* Filter out any neighbours that are blocking squares, or already visited.
        self.neighbours = list(filter(lambda cell: cell.cell_type!='Block' and not cell.visited, self.neighbours))

        for cell in self.neighbours:
            cell.potential_parents.append(self)
            self.children.append(cell)



################################################################

if __name__ == '__main__':
    from screen_details import *

    #* PARAMETERS
    x = 20   #* x axis co-ordinates of the top left cell
    y = 0   #* y axis co-ordinates of the top left cell
    cellWidth = 20

    def test(x,y,cellWidth):

        grid = []

        cellsY = (screenHeight//cellWidth)-1 #* total number of cells fitting on y axis
        cellsX = (screenWidth//cellWidth)-1  #* total number of cells fitting on x axis

        for _row in range(1,cellsY):
            #* begins at top left corner, works horizontally and moves down in line

            x = cellWidth      #* reset to start of line
            y += cellWidth     #* move down to next row of cell
            row = []

            for _col in range(1,cellsX):
                cell = Node([x,y],cellWidth,window) #* create cell, add to row and draw
                row.append(cell)

                cell.draw(WHITE)
                x += cellWidth  #* move to next cell in row

            grid.append(row)
            #* [a],[b],[c]
            #* [d],[e],[f]
            #* [g],[h],[i]

            for row in range(len(grid)-1):
                for col in range(len(grid[0])-1):
                    grid[row][col].find_neighbours(grid)    #* finds neighbouring cell to all cells



        #* Display Loop
        while True:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #* check where click is
                    for row in grid:
                        for cell in row:
                            if cell.rect.collidepoint(event.pos):
                                cell.to_block()


    test(x,y,cellWidth)