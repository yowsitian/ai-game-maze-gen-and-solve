# -*- coding: utf-8 -*-
import pygame, time, csv
import numpy as np
from time import sleep
from maze_solv.aStar_helper import generate_step, pick_node_from_list, Node

def playMaze(text_surface_gen, text_surface_sol, text_surface_level, mazeFile, screen, clock):

  start_t0 = time.time()

  address = "mazes/" + mazeFile
  grid = np.genfromtxt(address, delimiter=',', dtype=int)
  original_empty_space  = np.count_nonzero(grid == 1)

  # define goal and start
  num_rows = len(grid)
  num_columns = len(grid[0])
  goal = (num_rows-2, num_columns-2)
  start = (1,1)

  # define start node
  start_node = Node(None, 0, start)

  # initialize seen, frontier list
  seen = [] # starts empty
  frontier = [start_node] # starts with the start node

  # define colors of the grid RGB
  black = (0, 0, 0) # grid == 0
  white = (255, 255, 255) # grid == 1
  green = (50,205,50) # grid == 2
  red = (255,99,71) # grid == 3
  grey = (211,211,211) # for background
  blue = (153,255,255) # grid == 4, where current position is
  magenta = (255,0,255) # grid == 5 solution

  # set the height/width of each location on the grid
  height = 7
  width = height # i want the grid square
  margin = 1 # sets margin between grid locations

  idx_to_color = [black, white, green, red, blue, magenta]
  
  # loop until done
  interrupt = False # when user clicks exit
  run = True
  last_iter = False
  current_node = Node(None, np.inf, (0,0)) 

  while not interrupt and not last_iter:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        interrupt = True
    
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
      
    # set limit to 60 frames per second
    clock.tick(60)
      
    # update screen
    pygame.display.flip()
      
    if last_iter == True:
        run = False
    elif run == True:
        
        # pick a node from the frontier
        current_node = pick_node_from_list(frontier)
        grid, frontier, seen, current_node = generate_step(grid, frontier, seen, current_node)

        if current_node.position == goal: # if ai is at goal then finish
            last_iter = True

        sleep(0.01) # control speed of the update

  if(last_iter == True):
    ### follow the parents back to the origin
    while current_node.parent != None:
        x, y = current_node.position
        grid[x,y] = 5
        current_node = current_node.parent

    grid[1, 1] = 2
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
        
    image_name = "aStar_"+ mazeFile[:-4] + ".png"
    pygame.image.save(screen, image_name)   
    clock.tick(60) # set limit to 60 frames per second
    pygame.display.flip() # update screen
          
  
  sleep(0.50)
  # export maze to .csv file
  with open(f"mazes_solutions/aStar_{mazeFile}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(grid)

  area_explored = round(100 - np.count_nonzero(grid == 1) / original_empty_space * 100, 2)
  shortest_path = np.count_nonzero(grid == 5)
  maze_filename = "aStar_" + mazeFile
  result = [maze_filename, round(time.time()-start_t0, 3), shortest_path, area_explored]
  with open(f"mazes_solutions/result.csv", "a", newline='') as f_object:
    writer_object = csv.writer(f_object)
    writer_object.writerow(result)
  
  print(f"-- finished aStar_{mazeFile} {time.time()-start_t0:.3f} s | Shortest Path Count: {shortest_path} | Area Explore: {area_explored} % -- ")
  return interrupt