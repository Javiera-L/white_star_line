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

RADAR_ICE = 100
ICE_DENSITY = 900 # kg/m^3

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


class IcebergIdentifier:
    
    def __init__(self, radar_map, lidar_map):
        self.radar_map = radar_map
        self.lidar_map = lidar_map
        #self.num_icebergs, self.volumes, self.loc_array = self.iceberg_data()

    @property
    def iceberg_map(self):
        iceberg_map = self.radar_map >= RADAR_ICE
        #returns bool array in 1s and 0s instead of True/False
        return iceberg_map * 1

    def iceberg_data(self):
        graph = self.iceberg_map
        if not graph.any():
            return NameError('Error: empty graph.')
        weighted_graph = self.lidar_map
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
                    self.dfs(graph, weighted_graph, num_rows, num_cols, row, col, height_list, loc_array, count)
                    count +=1
                    tot_vol = sum(height_list) * 0.1 #times  the heights by 0.1 to convert to metres
                    volumes.append(tot_vol) # total volume of that iceberg
                    height_list.clear()
        return count, volumes, loc_array
        
    def dfs(self, graph, weighted_graph, num_rows, num_cols, y, x, height_list, loc_array, count):
        #recursive algorithm
        #if this vertex has been visited, remove it from the stack-> return
        if graph[y][x] == 0:                
            return
        #otherwise mark it as visited by making it zero
        graph[y][x] = 0
        
        height_list.append(weighted_graph[y][x])
        loc_array[y][x] = count + 1
        
        if y != 0:
            self.dfs(graph, weighted_graph, num_rows, num_cols, y - 1, x, height_list, loc_array, count)
        
        if y != num_rows - 1:
            self.dfs(graph, weighted_graph, num_rows, num_cols, y + 1, x, height_list, loc_array, count)
        
        if x != 0:
            self.dfs(graph, weighted_graph, num_rows, num_cols, y, x - 1, height_list, loc_array, count)
        
        if x != num_cols - 1:
            self.dfs(graph, weighted_graph, num_rows, num_cols, y, x + 1, height_list, loc_array, count)



class Iceberg:
    
    def __init__(self, volume, num, loc_map, colour_map):

        self.volume = volume
        self.num = num
        self.loc_map = (loc_map == num) * 1
        self.colour_map = colour_map

    @property
    def mass(self):
        # calculates total mass given that only 10% of mass is above water
        return self.volume * 900 / 0.1

    @property
    def is_towable(self):
        if self.mass <= 36*10**6:
            return True
        else:
            return False
    
    def tow_map(self):
        if self.is_towable == True:
            # green
            return self.colour((0,255,0))
        else:
            # red
            return self.colour((255,0,0))
            
    def colour(self, colour):
        row = len(self.loc_map)
        col = len(self.loc_map[0])
        for i in range(row):
            for j in range(col):
                if self.loc_map[i][j] == 1:
                    self.colour_map[i][j] = colour
                else:
                    pass
        return

radar = open_file('radar2.txt')
lidar = open_file('lidar2.txt')

#plt.plot(radar)
#plt.plot(lidar)
#plt.imshow(radar)


print(np.all(lidar==0))

#plt.imshow(radar)

identifier = IcebergIdentifier(radar, lidar)

count, volumes, loc_array = identifier.iceberg_data()
#plt.imshow(loc_array)
row = len(loc_array)
col = len(loc_array[0])
# empty map full of zeroes, same size as loc_array with each entry having 
# 3 more entries for each RGB value
colour_map = np.zeros((row, col, 3)) 
icebergs = []

for i in range(count):
    print(i)
    icebergs.append(Iceberg(volumes[i], i + 1, loc_array, colour_map))
    #need num to be i +1 to distinguish from 0, the background

# print(np.all(icebergs[0].loc_map==0))
# print(icebergs[0].is_towable)

# fig = plt.figure(frameon=False)
for i in range(count):
    icebergs[i].tow_map()
#     plt.axis('off')
plt.imshow(colour_map)
# plt.show()