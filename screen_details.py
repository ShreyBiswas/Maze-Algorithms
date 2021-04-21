import pygame

#* colour key
BLUE  = pygame.Color((0, 0, 255)) # unsearched maze cell, #0000ff
RED   = pygame.Color((255, 0, 0)) # searched maze cell, #ff0000
GREEN = pygame.Color((0, 255, 0)) # route solution, #00ff00

CYAN = pygame.Color((0,255,255)) # next building cell #00ffff
MAGENTA = pygame.Color((255,0,255)) # backtracking search cell #ff00ff
YELLOW = pygame.Color((255,255,0)) # start and target cells #ffff00

PINK = pygame.Color((255,20,147)) # next searching cell #ff1493

TURQ  = pygame.Color((8, 232, 222)) # next route cell #08e8de
GREY = pygame.Color((222, 222, 222)) # #dedede
BLACK = pygame.Color((0, 0, 0)) # blocking cell #000000
WHITE = pygame.Color((255, 255, 255)) # unsearched empty cell #ffffff



#* display specifications
screenWidth = 1000
screenHeight = 500
cellWidth = 20
FPS = pygame.time.Clock()
FPS.tick(10)

#* initialise display
# pylint: disable=no-member
pygame.init()
window = pygame.display.set_mode((screenWidth,screenHeight))
window.fill(BLACK)
pygame.display.set_caption('Maze')