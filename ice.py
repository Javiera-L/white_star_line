#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:49:59 2020

@author: Javi
"""

ICE_DENSITY = 900  # kg/m^3
MAX_TOW = 36*10**6

class Iceberg:

    def __init__(self, volume, mass, num, loc_map, colour_map):
        """
        Record description of an iceberg, including its volume, mass and
        location on the map. Also works out whether the iceberg is towable or
        not and colours it green or red accordingly.

        Parameters
        ----------
        volume : int
            Volume of the iceberg above surface level.
        num : int
            The unique identifier of the iceberg.
        loc_map : np.array
            An array that marks the location of the iceberg using the num
            (unique).
        colour_map : np.array
            A map that identifies icebergs as red if not towable, or green if
            they are towable.

        Returns
        -------
        None.

        """
        self.volume = volume
        self.mass = mass
        self.num = num
        self.loc_map = (loc_map == num) * 1
        self.colour_map = colour_map

    def __repr__(self):
        """
        Return a string containing a nicely printable representation of
        iceberg object. Useful for debugging and also for saving data to file.

        Returns
        -------
        str
            Prints out mass, volume, number and is_towable data from the
            iceberg.

        """
        return "Mass: %s, Volume: %s, Number: %s, is_towable = %s \n"\
            % (self.mass, self.volume, self.num, self.is_towable)

    @property
    def is_towable(self):
        """
        Calculate whether condition is fulfilled for towability. That is,
        mass must be less than MAX_TOW.

        Returns
        -------
        bool
            True if mass is less than MAX_TOW.
            False otherwise.

        """
        if self.mass <= MAX_TOW:
            return True
        else:
            return False

    def tow_map(self):
        """
        Call the colour function, telling it what colour it should use to
        identify each iceberg, depending on whether it is towable (green) or
        not (red).
        This updates the global array colour_map to then display all the map
        with all the icebergs coloured in.

        Returns
        -------
        None.

        """
        if self.is_towable == True:
            # green
            self.colour((0,255,0))
        else:
            # red
            self.colour((255,0,0))

    def colour(self, colour):
        """
        Colour the global array colour_map either green or red depending on
        towability.

        Parameters
        ----------
        colour : tuple
            Either (0,255,0) to denote green or (255,0,0) to denote red.

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
