import numpy as np
import time
from euclideandistance import distance
import sys
from itertools import product

#Read in file
infile = sys.argv[1]  
arrayin = np.loadtxt(infile, delimiter=" ")

#Figure out d and N
d = arrayin.shape[1]  
N = len(arrayin)  
s = 1 / (N ** (1 / d))  
cutoff = s ** 2 
num_bins_per_dim = int(np.ceil(1 / s))  

#print(f"Dimensions: {d}, Particles: {N}, Cutoff: {s:.6f}, Cells per dim: {num_bins_per_dim}")

tstart = time.time()

#Function to create empty bins for arbitrary dimensions
def partition(num_bins_per_dim, d):
    bins = {}
    #Generate all possible bin indices using itertools.product
    for bin_index in product(range(num_bins_per_dim), repeat=d):
        bins[bin_index] = []
    return bins

#Create spatial bins
bins = partition(num_bins_per_dim, d)

#Assign particles to bins
for idx, pos in enumerate(arrayin):
    bin_index = tuple((np.floor(pos / s) % num_bins_per_dim).astype(int))  #Compute bin index with wrapping
    if bin_index not in bins:
        bins[bin_index] = []
    bins[bin_index].append((idx, pos))

    #print(f"Particle {idx} at {pos} assigned to bin {bin_index}")

#print(f"Bins with particles: {[k for k, v in bins.items() if v]}")

p = 0  #Counter for number of neighbor pairs
#output_filename = f"cell_list_neighbors_d{d}_N{N}_sigma{s:.6f}.txt"

#with open(output_filename, "w") as outfile:
#    outfile.write("Index1 Index2 Pos1 Pos2 Distance\n")

#Loop over each bin
for bin_index, particles in bins.items():
    if not particles:  
        continue

    #Generate neighboring bin indices with wrapping
    neighbor_bins = []
    offsets = [-1, 0, 1]  

    #Use itertools.product to generate all combinations of offsets for d dimensions
    for offset in product(offsets, repeat=d):
        neighbor_index = tuple((bin_index[i] + offset[i]) % num_bins_per_dim for i in range(d))
        neighbor_bins.append(neighbor_index)

    #print(f"Checking bin {bin_index}, Neighbor bins: {neighbor_bins}")

    #Check for neighbors in the current and adjacent bins
    for nbin in neighbor_bins:
        if nbin in bins:
            for i, (idx1, p1) in enumerate(particles):
                for idx2, p2 in bins[nbin]:
                    if idx1 < idx2:
                        dist = distance(p1, p2)

                        #print(f"Comparing {idx1} ↔ {idx2}, Distance: {dist:.6f}, Cutoff: {s:.6f}")

                        if dist <= cutoff:
                            p += 1
                            #outfile.write(f"{idx1} {idx2} {p1} {p2} {dist:.6f}\n")

tend = time.time()
ttotal = tend - tstart

print(f"Total neighbors found: {p}")
#print(f"Results saved to {output_filename}")
print(f"Total runtime: {ttotal:.6f} seconds")