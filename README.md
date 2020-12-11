# White Star Line
Assignment 2 for the module GEOG5995M Programming for Social Scientists: Core Skills (Python), delivered at the University of Leeds.

## License
This code is licensed under the [Unlicense](https://unlicense.org) (see LICENCE file).

## Project Description
The project addresses the hypothetical need (and more from historical paranoia than anything else) for shipping companies to send out iceberg-towing tugs with all their ships. In order to use these iceberg-towing tugs, the companies need an application that can locate icebergs and assess their towability. This is the aim of this project.

The application I have built uses satellite radar data, and airborn lidar (LIght Detection and Ranging) data from an area of sea to locate the icebergs. With this information we can both locate the icebergs and approximate their mass. The functionality of the app is as follows:

1. Identifies the individual icebergs and their locations.
2. Calculates the mass of each iceberg.
3. Displays map of towable/non-towable icebergs, marking them as either green or red respectively.
4. Outputs the total mass, the total volume and whether you can pull the berg on the GUI, with option to save data to file.

## Repository Contents
Files included in the repository are as follows.
* `whitestarMain.py` : This is the main file of the programme.
* `icebergidentifier.py` : Builds the IcebergIdentifier() class, that uses the radar and lidar data to identify the icebergs on the map and calculate their volumes/masses. Uses the [depth first search algorithm](https://en.wikipedia.org/wiki/Depth-first_search) to identify positions of the icebergs.
* `ice.py` : Builds a simple class: Iceberg(). Each Iceberg() instance stores data for a single iceberg, assesses whether it is towable or not, and creates a map that highlights towable icebergs as green, red otherwise.
* `radar2.txt` : The radar file has per m2 values of between 0 and 255. A value of 100 or above is ice. The area will be 300m by 300m. 
* `lidar2.txt` : The radar file has per m2 values of between 0 and 255. One Lidar unit equals 10cm height. The area will be 300m by 300m. 

The following files are created after running the programme if we choose to export the data from the GUI.
* `towability_map.jpg` : JPG image of towability map, where green icebergs are towable, and red ones are not.
* `iceberg_data.txt` : Saved to this file are total mass, the total volume, iceberg identifier number and towability.
* `loc_array.txt`: Map of icebergs locations as a text file. The location of each iceberg is represented using its unique iceberg identifier number.

## Code execution and output
Install the repository files to your computer. Open up Terminal and navigate into the project folder. The program can now be run as follows.

Example:
`python whitestarMain.py radar2.txt lidar2.txt`

<img align="right" width="300" height="300" src="towability_map.jpg">

Here, the command line arguments are the radar and lidar data files respectively. They **must** be inputed in this order. The user can choose other radar and lidar files of their preference as long as they stick to the same units used in the files provided (see [Repository Contents](#repository-contents)). If too many/ too few command line arguments are inputted, the program will throw an error message and force the program to quit.

Upon running the programme, a new window should appear called "Towability Map". 
This is our GUI, and from the "Options" menu bar we can choose the following.
1. **Save image** : Saves the towability map as a jpg file `towability_map.jpg`.
2. **Print iceberg data** : Prints the iceberg data (total mass, the total volume, iceberg identifier number and towability) to the console.
3. **Save iceberg data to file** : Saves the iceberg data to `iceberg_data.txt`
4. **Save location array to file** : Saves the array of locations to `loc_array.txt`
5. **Quit** : Quits program and closes all windows.


## Further improvements
* Could display the information of each iceberg (mass, volume, towability) on the map, instead of printing it on the console.
