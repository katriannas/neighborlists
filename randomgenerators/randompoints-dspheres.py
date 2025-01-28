#Script to generate random configuration of N monodisperse d-spherical particles within a unit cell

import numpy as np
import sys

#Input dimension, number of particles, and radius of particles as command-line arguments
d = int(sys.argv[1])
n = int(sys.argv[2])
r = float(sys.argv[3])

#Create an array of points for particle centers
points = np.random.rand(n, d)

#Create an array to store these points and the radius around each point
#The "radii" vector extends in all directions around the center of the particle, creating a d-sphere
radii = np.full((n, d), r)
particles = np.hstack((points, radii))

#Save all of this to a text file
#Dimension, number of particles, and radius as strings for the filename
dimension = sys.argv[1]
number = sys.argv[2]
radius = sys.argv[3]

filename =("points_d" + dimension + "_n" + number + "_r" radius)
np.savetxt(filename, particles, delimiter=" ")

print("File saved")
