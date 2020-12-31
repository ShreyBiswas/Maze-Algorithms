import Maze_Generator as generator

#* construct maze
cellWidth = 20
grid = generator.build_blank_grid()
generator.generate_maze(grid,cellWidth,False)


