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
s = 1 / (((N) ** (1 / d)))
cutoff = s ** 2
num_bins_per_dim = int(np.ceil(1 / s))
bin_length = 1 / num_bins_per_dim

#Start the clock
tstart = time.time()

#Create bins
def partition(num_bins_per_dim, d):
    bins = {}
    #Index the bins
    for bin_index in product(range(num_bins_per_dim), repeat=d):
        bins[bin_index] = []
    return bins

bins = partition(num_bins_per_dim, d)

#Assign particles to bins
def assign_particles_to_bins(arrayin, bins, bin_length, num_bins_per_dim):
    for index, position in enumerate(arrayin):
        bin_index = tuple((np.floor(position / bin_length) % num_bins_per_dim).astype(int))
        if bin_index not in bins:
            bins[bin_index] = []
        bins[bin_index].append((index, position))
        
assign_particles_to_bins(arrayin, bins, bin_length, num_bins_per_dim)

#Create neighboring bins
def generate_neighbor_bins(bin_index, num_bins_per_dim, d):
    neighbor_bins = []
    offsets = list(product([-1, 0, 1], repeat=d))
    for offset in offsets:  # Iterate over all offsets
        neighbor_index = tuple((bin_index[i] + offset[i]) % num_bins_per_dim for i in range(d))
        neighbor_bins.append(neighbor_index)
    return neighbor_bins

#Actual neighbor search
def count_neighbor_pairs(bins, cutoff):
    neighbor_pairs = 0  #Set neighbor counter to 0 originally
    for bin_index, particles in bins.items():
        if not particles:
            continue
        #Figure out which ones are nearby
        neighbor_bins = generate_neighbor_bins(bin_index, num_bins_per_dim, d)
        for nbin in neighbor_bins:
            if nbin in bins:
                for i, (index1, p1) in enumerate(particles):
                    for index2, p2 in bins[nbin]:
                        if index1 < index2:
                            #Make sure a particle can't count itself as a neighbor
                            if index1 == index2 and nbin == bin_index:
                                continue
                            dist = distance(p1, p2)
                            if dist <= cutoff:
                                neighbor_pairs += 1
    return neighbor_pairs

neighbor_pairs = count_neighbor_pairs(bins, cutoff)

#Stop the clock, print results
tend = time.time()
ttotal = tend - tstart

print(f"Total neighbor pairs found: {neighbor_pairs}")
print(f"Total runtime: {ttotal:.6f} seconds")
