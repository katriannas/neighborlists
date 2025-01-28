#Generate random configuration of N monodisperse d-spherical particles

import numpy as np
import sys

# Input dimension, number of particles, and radius of particles as command-line arguments
d = int(sys.argv[1])
n = int(sys.argv[2])
r = float(sys.argv[3])

# Generate points (centers of the spheres)
points = np.random.rand(n, d)

# Create an array to store point locations and the radius around each point
# The surface of each particle is represented as a vector in d dimensions
radii = np.full((n, d), r)
particles = np.hstack((points, radii))

# Create a text file and save the array to the file
# Dimension, number of particles, and radius as strings for use in the filename
dimension = sys.argv[1]
number = sys.argv[2]
radius = sys.argv[3]

filename =("points_d" + dimension + "_n" + number + "_r" radius)
np.savetxt(filename, particles, delimiter=" ")

print("File saved")
