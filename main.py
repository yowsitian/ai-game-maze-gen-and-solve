from maze_gen.maze import Maze
from maze_gen.cellular_gen import CellularAutomaton
from maze_gen.backtracking_gen import BacktrackingGenerator
from maze_solv import aStar_solver
from maze_solv import bfs_solver
from maze_solv import dfs_solver
import matplotlib.pyplot as plt
import pandas as pd
import pygame

levels = [10,15,20,25,30]
maze_generator = [CellularAutomaton, BacktrackingGenerator]
# maze_solver = [aStar_solver, bfs_solver, dfs_solver]
maze_solver = [aStar_solver]

def showPNG(grid, img_name):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.axis('off')
    plt.savefig(img_name, bbox_inches='tight',pad_inches=0)
    plt.close()

def displayGenerator(generator):
    title = "Maze Generator: "
    if(generator == 0):
        title += "Cellular Automaton"
    else:
        title += "Recursive Backtracking"
    return title

def displaySolver(solver):
    title = "Maze Solver: "
    if(solver == 0):
        title += "A Star"
    elif(solver == 1):
        title += "BFS"
    else:
        title += "DFS"
    return title

# initialize pygame
pygame.init()

# congiguration of the window
WINDOW_SIZE = [550, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock() # to manage how fast the screen updates
pygame.display.set_caption(f"Pathfinder. Solving maze.")
my_font = pygame.font.SysFont('Comic Sans MS', 18)
# define colors of the grid RGB
black = (0, 0, 0) # grid == 0
white = (255, 255, 255) # grid == 1
green = (50,205,50) # grid == 2
red = (255,99,71) # grid == 3
grey = (211,211,211) # for background
blue = (153,255,255) # grid == 4, where current position is
magenta = (255,0,255) # grid == 5 solution

interrupt = False
finish = False
# main painting loop
while not interrupt:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            interrupt = True
            
        # wait for user to press RETURN key to start    
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                run = True
    
    for mazeCounter, maze in enumerate(maze_generator):
        text_surface_gen = my_font.render(displayGenerator(mazeCounter), False, (0, 0, 0))  
        if interrupt:
            break
        for solverCounter, solver in enumerate(maze_solver):
            text_surface_sol = my_font.render(displaySolver(solverCounter), False, (0, 0, 0))            
            if interrupt:
                break
            for levelCounter, level in enumerate(levels):
                text_surface_level = my_font.render(f'Level {levelCounter+1}', False, (0, 0, 0))    
                if interrupt:
                    break
                # generate maze
                m = Maze()
                # level indicates the size of the map, eg. 20 x 20
                maze_width = level
                maze_height = level

                m.generator = CellularAutomaton(maze_width, maze_height)
                m.generate()

                Maze.set_seed(123)
                png_maze_file = f'mazes/maze_{mazeCounter}_solver_{solverCounter}.png'
                csv_maze_file = f'mazes/maze_{mazeCounter}_solver_{solverCounter}.csv'
                showPNG(m.grid, png_maze_file)

                # convert maze to csv without changing the image quality
                # convert array into dataframe
                maze_grid = 1 - m.grid
                DF = pd.DataFrame(maze_grid)
 
                # save the dataframe as a csv file
                DF.to_csv(csv_maze_file, header=False, index=False)

                # solve maze
                interrupt = solver.playMaze(text_surface_gen, text_surface_sol, text_surface_level, f'maze_{mazeCounter}_solver_{solverCounter}.csv', screen, clock)
    break

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
pygame.quit() # so that it doesnt "hang" on exit

exit(0)

            