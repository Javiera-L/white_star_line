#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:49:30 2020

@author: Javi
"""

import numpy as np
import sys
sys.setrecursionlimit(100000)

RADAR_ICE = 100

class IcebergIdentifier:

    def __init__(self, radar_map, lidar_map):
        """
        Identify icebergs using  radar and lidar data.

        Parameters
        ----------
        radar_map : np.array
            array of radar data
        lidar_map : np.array
            array of lidar data

        Returns
        -------
        None.

        """
        self.radar_map = radar_map
        self.lidar_map = lidar_map

    @property
    def iceberg_map(self):
        """
        Use radar data to locate where ice is found. Return boolean array
        of marking these locations.

        Returns
        -------
        np.array
            Returns boolean array (1s and 0s instead of True/False)
            of where we find ice on the map.

        """
        iceberg_map = self.radar_map >= RADAR_ICE
        return iceberg_map * 1

    def mass(self, vol):
        """
        Calculate the total mass of the iceberg.

        Returns
        -------
        int
            Total volume of the iceberg accounting that only 10% of mass is
            above water.

        """
        # calculates total mass given that only 10% of mass is above water
        return vol* 900 / 0.1


    def collect_data(self):
        """
        Locate the icebergs on the map and find their volume.

        Returns
        -------
        int
            Variable "count" registers the number of iceberg that have been found.
        list
            The list "volumes" contains the volumes of each iceberg respectively.
        list
            The list "masses" contains the mass of each ieberg respectively
        np.array
            "loc_array" is a numpy array marking the location of each iceberg.
            Each iceberg has its own unique number, for the order in which they were
            found, and can be identified in this way.

        """
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
        masses = []

        for row in range(num_rows):
            for col in range(num_cols):
                if graph[row][col] == 1:
                    self.__dfs(graph, weighted_graph, num_rows, num_cols,
                             row, col, height_list, loc_array, count)
                    count += 1
                    tot_vol = sum(height_list) * 0.1  # x the heights by .1
                    volumes.append(tot_vol)  # total volume of that iceberg
                    masses.append(self.mass(tot_vol))
                    height_list.clear()
        return count, volumes, masses, loc_array

    def __dfs(self, graph, weighted_graph, num_rows, num_cols, y, x,
            height_list, loc_array, count):
        """
        Depth first search algorithm.
        Recursive implementation to find connected components.

        Parameters
        ----------
        graph : np.array
            The array represents the locations of the ice (1/0 values).
        weighted_graph : np.array
            The heights of each m^2 of ice.
        num_rows : int
            Number of rows in the graph.
        num_cols : int
            Number of columns in the graph.
        y : int
            Used as an index for the 2D array.
        x : int
            Used as an index for the 2D array.
        height_list : list
            List of the heights of each m^2 of the iceberg.
        loc_array : array
            Array that tracks the location of each iceberg, using a unique
            number to identify each one.
        count : int
            Unique identifier for each iceberg. Keeps track of the iceberg
            number we are on .

        Returns
        -------
        None.

        """
        # recursive algorithm
        # if this vertex has been visited, remove it from the stack-> return
        if graph[y][x] == 0:
            return
        # otherwise mark it as visited by making it zero
        graph[y][x] = 0

        height_list.append(weighted_graph[y][x])
        loc_array[y][x] = count + 1

        if y != 0:
            self.__dfs(graph, weighted_graph, num_rows, num_cols, y - 1, x,
                     height_list, loc_array, count)

        if y != num_rows - 1:
            self.__dfs(graph, weighted_graph, num_rows, num_cols, y + 1, x,
                     height_list, loc_array, count)

        if x != 0:
            self.__dfs(graph, weighted_graph, num_rows, num_cols, y, x - 1,
                     height_list, loc_array, count)

        if x != num_cols - 1:
            self.__dfs(graph, weighted_graph, num_rows, num_cols, y, x + 1,
                     height_list, loc_array, count)
