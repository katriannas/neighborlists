import numpy as np
import sys
from euclideandistance import distance
import time

infile = sys.argv[1]

#Open file, read in parameters
arrayin = np.loadtxt(infile, delimiter=" ")
d = arrayin.shape[1]
N = len(arrayin)
sigma = 1 / (((N) ** (1 / d)))
cutoff = sigma ** 2

#Counter for the total number of neighbor pairs
neighbor_pairs = 0

tstart = time.time()

#Looping over n
for n in range(N):
    #Looping over m
    for m in range(n + 1, N):
        point1 = arrayin[n]
        point2 = arrayin[m]

        #Call Euclidean distance function
        dist = distance(point1, point2)

        #Compare to cutoff
        if dist <= cutoff:
            neighbor_pairs += 1

#Print the total number of pairs
print(f"Total neighbor pairs found: {neighbor_pairs}")

tend = time.time()
ttotal = tend - tstart

print(f"Total runtime: {ttotal:.6f} seconds")
