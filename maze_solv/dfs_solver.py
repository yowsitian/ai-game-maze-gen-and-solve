# -*- coding: utf-8 -*-
import pygame, time, csv
import numpy as np
from time import sleep
from numpy.random import randint

def is_in_map(pos, grid_dim):
    """
    Parameters
    ----------
    pos : tuple of 2 ints 
        x, y coordinates in the grid system of current
        position
    grid_dim : tuple of ints
        x, y dimension of the grid system
    Returns
        true if pos in map
        false if not in map
    """
    (max_x, max_y) = grid_dim # unroll the dimensions
    (x, y) = pos # unroll the position coordinates
    
    x_in = (x <= max_x) & (x >= 0) # logical x in map
    y_in = (y <= max_y) & (y >= 0) # logical y in map
    return bool(x_in*y_in) # only true if both true

# ===========================

class Node:
    def __init__(self, pos, parent):
        self.x = pos[0]
        self.y = pos[1]
        self.parent = parent

    def __getitem__(self):
          return (self.x, self.y)

    def position(self):
        return (self.x, self.y)


class Queue:
    def __init__(self):
        self.Queue = []

    def __len__(self):
        return len(Queue)

    def append(self, node):
        self.Queue.append(node)

    def get_node(self):
        return self.Queue[-1]

    def get_node_position(self):
        node = self.Queue[-1]
        return node.position()

    def remove(self):
        self.Queue = self.Queue[0:len(self.Queue)-1]

class DFS:
    def __init__(self, start_pos, goal_pos, grid_dim):
        self.grid_dim = grid_dim
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.explored = Queue()
        self.frontier = Queue()
        node = Node(pos=start_pos, parent=None)
        self.frontier.append(node)

    def backtrack_solution(self, grid, curr_node):
        solution = []
        while curr_node.parent != None:
            solution.append(curr_node.position())
            curr_node = curr_node.parent

        return solution

    def compute_successors(self, grid):
        curr_node = self.frontier.get_node()
        x, y = curr_node.position()

        buffer_nodes = []
        for movement in [(1,0), (-1,0), (0,1), (0,-1)]:
            dx, dy = movement
            new_pos = (x+dx, y+dy)

            if (is_in_map(new_pos, self.grid_dim)) and (grid[new_pos[0], new_pos[1]] in [1, 3]) :
                new_node = Node(pos=new_pos, parent=curr_node)
                buffer_nodes.append(new_node)
                

                if set(new_pos) == set(self.goal_pos):
                    self.explored.append(self.frontier.get_node())
                    self.frontier.remove()
                    done = True
                    solution = self.backtrack_solution(grid, curr_node=new_node)
                    return solution, done

        self.explored.Queue.append(curr_node)
        self.frontier.remove()

        [self.frontier.Queue.append(new_node) for new_node in buffer_nodes]
        done = False
        return [], done

def playMaze(text_surface_gen, text_surface_sol, text_surface_level, mazeFile, screen, clock):

    start_t0 = time.time()

    address = "mazes/" + mazeFile
    grid = np.genfromtxt(address, delimiter=',', dtype=int)
    original_empty_space  = np.count_nonzero(grid == 1)

    num_rows = len(grid)
    num_columns = len(grid[0])

    # define start, define goal
    start_pos = (1,1)
    goal_pos = (num_rows-2, num_columns-2)

    # define start and goal
    grid[1, 1] = 2
    grid[-2, -2] = 3

    grid_dim = (num_rows-1, num_columns-1)

    black = (0,0,0)
    white = (255, 255, 255)
    green = (50,205,50)
    red = (255,99,71)
    grey = (211,211,211)
    blue = (153,255,255)
    magenta = (255,0,255)

    idx_to_color = [black, white, green, red, blue, magenta]

    # set the height/width of each location on the grid
    height = 7
    width = height # i want the grid square
    margin = 1 # sets margin between grid locations

    # loop until done
    done = False
    run = True
    close = False

    dfs = DFS(start_pos=start_pos, goal_pos=goal_pos, grid_dim=grid_dim)

    # main program
    while not done and not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True

        screen.fill(grey) # fill background in grey
        screen.blit(text_surface_gen, (5,500))
        screen.blit(text_surface_sol, (5,530))
        screen.blit(text_surface_level, (5,560)) 
        for row in range(num_rows):
            for column in range(num_columns):
                color = idx_to_color[grid[row, column]]
                pygame.draw.rect(screen, color, 
                                  [(margin + width) * column + margin, 
                                  (margin + height) * row + margin,
                                  width, height])
        
        
        clock.tick(60) # set limit to 60 frames per second
        pygame.display.flip() # update screen
        
        if run == True:

            sleep(0.01)
            solution, done = dfs.compute_successors(grid=grid)
        
            explored = [node.position() for node in dfs.explored.Queue]

            for pos in explored:
                grid[pos[0], pos[1]] = 4

    if done == True:
        for pos in solution:
            grid[pos[0], pos[1]] = 5
        grid[0, 0] = 2
        grid[-2, -2] = 3

        screen.fill(grey) # fill background in grey
        screen.blit(text_surface_gen, (5,500))
        screen.blit(text_surface_sol, (5,530))
        screen.blit(text_surface_level, (5,560))        
        for row in range(num_rows):
            for column in range(num_columns):
                color = idx_to_color[grid[row, column]]
                pygame.draw.rect(screen, color, 
                                [(margin + width) * column + margin, 
                                (margin + height) * row + margin,
                                width, height])
        
        image_name = "dfs"+ mazeFile[:-4] + ".png"
        pygame.image.save(screen, image_name)
        clock.tick(60) # set limit to 60 frames per second
        pygame.display.flip() # update screen
    
    sleep(0.50)

    # export maze to .csv file
    with open(f"mazes_solutions/dfs_{mazeFile}", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)

    area_explored = round(100 - np.count_nonzero(grid == 1) / original_empty_space * 100, 2)
    shortest_path = np.count_nonzero(grid == 5)
    maze_filename = "dfs_" + mazeFile
    result = [maze_filename, round(time.time()-start_t0, 3), shortest_path, area_explored]
    with open(f"mazes_solutions/result.csv", "a", newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(result)
        f_object.close()

    print(f"-- finished dfs_{mazeFile} {time.time()-start_t0:.3f} s | Shortest Path Count: {shortest_path} | Area Explore: {area_explored:.2f} % -- ")
    return close