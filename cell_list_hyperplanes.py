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
s = 1 / (N ** (1 / d))  #Cutoff distance
cutoff = s ** 2
num_hyp_per_dim = int(np.ceil(1 / s))  #Number of hyperplanes per dimension

#Function to create the structure of hyperplanes (regions)
def create_hyperplane_structure(num_hyp_per_dim, d):
    #Generate all possible region indices
    region_indices = list(product(range(num_hyp_per_dim), repeat=d))
    regions = {index: [] for index in region_indices}
    return regions

#Function to assign particles to regions
def assign_to_regions(arrayin, s, d, regions):
    for idx, pos in enumerate(arrayin):
        #Determine the region index for each dimension with periodic boundary conditions
        region_index = tuple((np.floor(pos / s) % num_hyp_per_dim).astype(int))
        regions[region_index].append((idx, pos))
    return regions

tstart = time.time()

regions = create_hyperplane_structure(num_hyp_per_dim, d)

regions = assign_to_regions(arrayin, s, d, regions)

p = 0  #Counter for number of neighbor pairs

#Loop over each region
for region_index, particles in regions.items():
    if not particles:  
        continue

    #Generate neighboring region indices with periodic boundary conditions
    neighbor_regions = []
    offsets = [-1, 0, 1]  #Check current and adjacent regions in each dimension

    #Use itertools.product to generate all combinations of offsets for d dimensions
    for offset in product(offsets, repeat=d):
        neighbor_index = tuple((region_index[i] + offset[i]) % num_hyp_per_dim for i in range(d))
        neighbor_regions.append(neighbor_index)

    #Check for neighbors in the current and adjacent regions
    for nregion in neighbor_regions:
        if nregion in regions:
            for i, (idx1, p1) in enumerate(particles):
                for idx2, p2 in regions[nregion]:
                    if idx1 < idx2:
                        #Calculate the minimum image distance considering periodic boundary conditions
                        delta = distance(p1, p2)

                        if delta <= cutoff:
                            p += 1

#End timing
tend = time.time()
ttotal = tend - tstart

print(f"Total neighbors found: {p}")
print(f"Total runtime: {ttotal:.6f} seconds")