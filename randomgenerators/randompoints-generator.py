#Script to generate a d-dimensional array of N random points and save this data to a text file

import numpy as np
import sys

#Input dimension and number of particles as command line arguments
d = int(sys.argv[1])
n = int(sys.argv[2])

#Generate points
points = np.random.rand(n, d)

#Create a text file and save the array to the file

#Dimension and number of particles as a string so they can be used in filename
dimension = sys.argv[1]
number = sys.argv[2]

filename =("points_" + dimension + "_" + number)
np.savetxt(filename, points, delimiter= " ")

print("File saved")