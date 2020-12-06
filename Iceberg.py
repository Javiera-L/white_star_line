#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:49:59 2020

@author: Javi
"""

ICE_DENSITY = 900 # kg/m^3

class Iceberg:

    def __init__(self, volume, num, loc_map, colour_map):
        """
        

        Parameters
        ----------
        volume : TYPE
            DESCRIPTION.
        num : TYPE
            DESCRIPTION.
        loc_map : TYPE
            DESCRIPTION.
        colour_map : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        self.volume = volume
        self.num = num
        self.loc_map = (loc_map == num) * 1
        self.colour_map = colour_map

    @property
    def mass(self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # calculates total mass given that only 10% of mass is above water
        return self.volume * 900 / 0.1

    @property
    def is_towable(self):
        """
        

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if self.mass <= 36*10**6:
            return True
        else:
            return False

    def tow_map(self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if self.is_towable == True:
            # green
            return self.colour((0,255,0))
        else:
            # red
            return self.colour((255,0,0))

    def colour(self, colour):
        """
        

        Parameters
        ----------
        colour : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        row = len(self.loc_map)
        col = len(self.loc_map[0])
        for i in range(row):
            for j in range(col):
                if self.loc_map[i][j] == 1:
                    self.colour_map[i][j] = colour
                else:
                    pass
        return