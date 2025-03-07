import numpy as np
import time
from euclideandistance import distance
import sys

infile = sys.argv[1]
arrayin = np.loadtxt(infile, delimiter=" ")

#Figure out d and N
d = arrayin.shape[1]
N = len(arrayin)
s = 1 / (((N) ** (1 / d)))
cutoff = s ** 2

#Start the clock
tstart = time.time()

#Build our tree
class KDTree:
    def __init__(self, points, indices, depth=0):
        if len(points) == 0:
            self.points = None
            self.indices = []
            self.left = None
            self.right = None
            self.axis = None
            return

        #Sorting and finding the medians
        self.axis = depth % d
        sorted_indices = np.argsort(points[:, self.axis])
        sorted_points = points[sorted_indices]
        sorted_global_indices = indices[sorted_indices]
        median_idx = len(sorted_points) // 2
        self.point = sorted_points[median_idx]
        self.index = sorted_global_indices[median_idx]

        #Make it keep splitting the tree if the medians are farther apart than s
        stop_splitting = True
        for axis in range(d):
            if median_idx + 1 < len(sorted_points):
                next_median_point = sorted_points[median_idx + 1]
                if distance(self.point, next_median_point) > s:
                    stop_splitting = False
                    break

        if stop_splitting:
            self.points = sorted_points
            self.indices = sorted_global_indices
            self.left = None
            self.right = None
        else:
            self.left = KDTree(sorted_points[:median_idx], sorted_global_indices[:median_idx], depth + 1)
            self.right = KDTree(sorted_points[median_idx + 1:], sorted_global_indices[median_idx + 1:], depth + 1)
            self.points = None
            self.indices = []

#Bounding box - upper limit of distance (s)
def bbox_distance(point, node):
    if node.points is not None:  # Leaf node
        return 0
    delta = np.abs(point[node.axis] - node.point[node.axis])
    delta = np.where(delta > 0.5, 1.0 - delta, delta)
    diff = max(0, delta - s)
    return diff ** 2

#Figure out which nodes to check
def collect_nodes(node, target, depth=0):
    if node is None:
        return []

    #Only include leaf nodes
    if node.points is not None:
        return [node]

    axis = depth % d
    next_branch = node.left if target[axis] < node.point[axis] else node.right
    other_branch = node.right if target[axis] < node.point[axis] else node.left

    nodes = collect_nodes(next_branch, target, depth + 1)

    if bbox_distance(target, other_branch) <= cutoff:
        nodes.extend(collect_nodes(other_branch, target, depth + 1))

    return nodes

#Neighbor search. Vectorized distance calculations are faster
def search_neighbors(target, i, nodes):
    neighbor_pairs = 0
    for node in nodes:
        delta = np.abs(node.points - target)
        delta = np.where(delta > 0.5, 1.0 - delta, delta)
        distances = np.sum(delta ** 2, axis=1)
        neighbor_pairs += np.sum((i < node.indices) & (distances <= cutoff))
    return neighbor_pairs

#Call all our functions and actually do the calculations
indices = np.arange(N)
kdtree = KDTree(arrayin, indices)

neighbor_pairs = 0

for i in range(N):
    nodes_to_check = collect_nodes(kdtree, arrayin[i])
    neighbor_pairs += search_neighbors(arrayin[i], i, nodes_to_check)

#Stop the clock, print results
tend = time.time()

print(f"Number of neighbor pairs: {neighbor_pairs}")
print(f"Total runtime: {tend - tstart}")