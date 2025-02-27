import numpy as np
import time
import sys

infile = sys.argv[1]
arrayin = np.loadtxt(infile, delimiter=" ")

N = len(arrayin)
d = 1
s = 1 / N
cutoff = s ** 2  #Not important since distances are just absolute values

#Start time
tstart = time.time()

#Build kd-tree
def build_kdtree_indices(points):
    if len(points) == 0:
        return None

    sorted_indices = np.argsort(points)  # Sort indices
    sorted_points = points[sorted_indices]

    #Distance between the node medians
    median_idx = len(sorted_points) // 2
    median_point = sorted_points[median_idx]

    #Condition for when to stop
    if len(sorted_points) > 1:
        next_median_idx = median_idx + 1 if median_idx + 1 < len(sorted_points) else median_idx
        next_median_point = sorted_points[next_median_idx]
        if abs(median_point - next_median_point) <= s:
            return {
                'point_indices': sorted_indices.tolist(),  # Store all indices at this leaf
                'left': None,
                'right': None
            }

    #Until then, keep going!
    return {
        'point_index': sorted_indices[median_idx],
        'left': build_kdtree_indices(sorted_points[:median_idx]),
        'right': build_kdtree_indices(sorted_points[median_idx + 1:])
    }

kdtree = build_kdtree_indices(arrayin)

#Counter for total pairs and storage for ones we've checked before
neighbor_pairs = 0
unique_pairs = set()

for i in range(N):
    target = arrayin[i]  #Particle we're trying to find neighbors of
    stack = [(kdtree, 0)]  #Stack for traversing the tree
    while stack:
        node, depth = stack.pop()
        if node is None:
            continue

        #Check all particles in the same node
        if 'point_indices' in node:
            for idx1 in node['point_indices']:
                for idx2 in node['point_indices']:
                    if idx1 < idx2:
                        delta = abs(arrayin[idx1] - arrayin[idx2])
                        if delta > (1/2):
                            delta = 1 - delta
                        if delta <= s:
                            pair = (idx1, idx2)
                            if pair not in unique_pairs:
                                unique_pairs.add(pair)
                                neighbor_pairs += 1
            continue

        #What are we checking???
        current_point = arrayin[node['point_index']]
        delta = abs(current_point - target)

        #Compare and make sure they're not identical
        if delta <= s and i != node['point_index']:
            pair = tuple(sorted((i, node['point_index'])))
            if pair not in unique_pairs:
                unique_pairs.add(pair)
                neighbor_pairs += 1

        if target < current_point:
            #Visit the left branch
            stack.append((node['left'], depth + 1))
            # Check on the right branch
            if abs(current_point - target) <= s:
                stack.append((node['right'], depth + 1))
        else:
            #Visit the right branch
            stack.append((node['right'], depth + 1))
            # Check on the left branch
            if abs(current_point - target) <= s:
                stack.append((node['left'], depth + 1))

tend = time.time()
total_time = tend - tstart

#Output
print(f"Number of neighbor pairs: {neighbor_pairs}")
print(f"Total runtime: {total_time}")
