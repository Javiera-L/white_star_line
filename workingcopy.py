#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 10:31:53 2020

@author: Javi
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 18:25:49 2020

@author: Javi
"""
import matplotlib
import matplotlib.pyplot as plt
import csv
import numpy as np
import sys
sys.setrecursionlimit(100000)


def open_file(file):
    list_data = []
    #note that "in.txt" needs to be a square matrix (same number of rows as cols)
    f = open(file, newline='')
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: # A list of rows
        rowlist = []
        for value in row: # A list of value
            rowlist.append(value)
        list_data.append(rowlist)
    f.close() # Don't close until you are done with the reader;
            # the data is read on request.
    print("Loading file...")
    return(np.array(list_data))

def num_icebergs(graph, weighted_graph):
   # if not graph:
   #     return NameError('Error: empty graph.')
    
    num_rows = len(graph)
    num_cols = len(graph[0])
    count = 0
    height_list = []
    loc_array = np.zeros((num_rows, num_cols))
    tot_vol = 0
    volumes = []
    
    for row in range(num_rows):
        for col in range(num_cols):
            if graph[row][col] == 1:
                dfs(graph, weighted_graph, num_rows, num_cols, row, col, height_list, loc_array, count)
                count +=1
                tot_vol = sum(height_list)
                volumes.append(tot_vol)
                height_list.clear()
    return count, volumes, loc_array
    
def dfs(graph, weighted_graph, num_rows, num_cols, y, x, height_list, loc_array, count):
    #recursive algorithm
    #if this vertex has been visited, remove it from the stack-> return
    if graph[y][x] == 0:
        #if height_list > max height for towability:
            #colour = 'red'
        #else:
            #colour = 'green'
            
        return
    #otherwise mark it as visited by making it zero
    graph[y][x] = 0
    #coloured_graph[y][x] = colour
    
    height_list.append(weighted_graph[y][x])
    loc_array[y][x] = count + 1
    
    if y != 0:
        dfs(graph, weighted_graph, num_rows, num_cols, y - 1, x, height_list, loc_array, count)
    
    if y != num_rows - 1:
        dfs(graph, weighted_graph, num_rows, num_cols, y + 1, x, height_list, loc_array, count)
    
    if x != 0:
        dfs(graph, weighted_graph, num_rows, num_cols, y, x - 1, height_list, loc_array, count)
    
    if x != num_cols - 1:
        dfs(graph, weighted_graph, num_rows, num_cols, y, x + 1, height_list, loc_array, count)
        
def is_iceberg(radar_data):
    is_iceberg = radar_data >= 100
    #returns bool array in 1s and 0s instead of True/False
    return is_iceberg * 1


radar = open_file('radar2.txt')
lidar = open_file('lidar2.txt')

#plt.plot(radar)
#plt.plot(lidar)
#plt.imshow(radar)

iceberg_map = is_iceberg(radar)

print(np.all(lidar==0))

count, volumes, loc_array = num_icebergs(iceberg_map, lidar)

plt.imshow(radar)
#plt.imshow(loc_array)
    
