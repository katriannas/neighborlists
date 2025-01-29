#Generate random configuration of N monodisperse d-spherical particles

import numpy as np
import sys

#Input dimension, number of particles, and radius of particles as command-line arguments
d = int(sys.argv[1])
n = int(sys.argv[2])
r = float(sys.argv[3])

#Generate points (centers of the spheres)
points = np.random.rand(n, d)

#Combine points and radius into a single array for saving
radii = np.full((n, 1), r)  # Single radius per particle
particles = np.hstack((points, radii))

#Save the points to a text file
#Arguments as strings for the filename
dimension = sys.argv[1]
number = sys.argv[2]
radius = sys.argv[3]

filename =("points_d" + dimension + "_n" + number + "_r" radius)
np.savetxt(filename, particles, delimiter=" ")

print("File saved")
