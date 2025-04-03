#Good version - actually produces right number of neighbors
#Exploded into too many functions for easier debugging - fix this

import numpy as np
import sys
import time

class KDTree:
    #Seup nd parameters
    def __init__(self, dim, points, unit_cell):
        self._dim = dim
        self._points = points.tolist()
        self._unit_cell = unit_cell
        self._root = self.build_kd_tree()
    
    def build_kd_tree(self):
        #Assign indices
        indexed_points = list(enumerate(self._points))
        return self.build_recursive(indexed_points, self._dim)
    
    #Splitting function (recursive)
    def build_recursive(self, points, dim, i=0):
        #New stopping condition
        if len(points) > 1:
            #Sort along current splitting axis, then rotate axes
            points.sort(key=lambda x: x[1][i])
            i = (i + 1) % dim
            half = len(points) >> 1
            
            #Build left and then right
            return [
                self.build_recursive(points[:half], dim, i),
                self.build_recursive(points[half+1:], dim, i),
                points[half][1],
                points[half][0]
            ]
        #Leaf nodes at the end!
        elif len(points) == 1:
            return [None, None, points[0][1], points[0][0]]
    
    #Counter function
    def neighbor_counter(self, bounds, cutoff):
        count = 0
        for i, point in enumerate(self._points):
            count += self.neighbor_search(self._root, point, bounds, i)
        return count
    
    #Tree traversal
    def neighbor_search(self, root_node, reference_point, bounds, min_index):
        #Stack - faster than the recursion version I had
        stack = [(root_node, 0)]
        count = 0
    
        #Do periodic boundaries now instead of over and over again
        periodic_bounds = []
        for i in range(self._dim):
            # Compute lower and upper bounds for the search along this axis
            dim_lower = reference_point[i] + bounds[i][0]
            dim_upper = reference_point[i] + bounds[i][1]
    
            if dim_lower < 0 or dim_upper > self._unit_cell:
                dim_lower = dim_lower % self._unit_cell
                dim_upper = dim_upper % self._unit_cell
            
            periodic_bounds.append((dim_lower, dim_upper))
    
        while stack:
            node, i = stack.pop()
            if node is None:
                continue
    
            #Get the point and its original index from the node
            current_point, current_index = node[2], node[3]
    
            #Only count when i < j
            if current_index > min_index and self.neighbor_check(current_point, reference_point, bounds):
                count += 1
    
            #Next splitting axis
            next_dim = (i + 1) % self._dim
            split_value = node[2][i]
    
            dim_lower, dim_upper = periodic_bounds[i]
    
            #Which subtree to search first?
            left_first = split_value > reference_point[i]
    
            #If the split is inside the bounding box, both subtrees might have neighbors
            if dim_lower <= split_value <= dim_upper or dim_upper < dim_lower:
                stack.append((node[0], next_dim))
                stack.append((node[1], next_dim))
            else:
                if left_first:
                    stack.append((node[0], next_dim))
                else:
                    stack.append((node[1], next_dim))
    
        return count
    
    #Explicit distance in case that was causing errors
    def neighbor_check(self, point, reference_point, bounds):
        tdistance = 0.0
    
        for i in range(self._dim):
            delta = abs(point[i] - reference_point[i])
    
            if delta > (self._unit_cell / 2):
                delta = self._unit_cell - delta
    
            #No need to perform unnecessary checks
            if delta > bounds[i][1]:
                return False
            
            tdistance += delta ** 2
    
            #Early exit: If squared distance already exceeds cutoff, stop checking
            if tdistance > cutoff:
                return False
    
        return True   #yay!

#Now we actually do it
input_file = sys.argv[1]
points = np.loadtxt(input_file)

d = points.shape[1]
N = len(points)
s = 1 / (N ** (1 / d))
unit_cell = 1.0
cutoff = float(s ** 2)
bounds = [(-s, s) for _ in range(d)]  #Bounding box 2.0

#Start the clock
tstart = time.time()

tree = KDTree(d, points, unit_cell)
pair_count = tree.neighbor_counter(bounds, cutoff)

#Stop the clock after 2 lines (work on pulling more of it inline instead of calling so many functions)
tend = time.time()
ttotal = tend - tstart

print(f"Total runtime: {ttotal} seconds")
print(f"Total neighbor pairs found: {pair_count}")
