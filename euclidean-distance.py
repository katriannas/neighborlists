import numpy as np
import sys

#This part will be part of the NNS algorithm and not part of this function but I included it here so that I could test this

infile = sys.argv[1]
#Again, NNS implementation will have loop to compare the nth point with the (n+m)th point, this is for testing
n = 0
m = 3

#Open file with array of randomly generated points
arrayin = np.loadtxt(infile, delimiter= " ")

#Figure out d and N from array
d = arrayin.ndim
N = len(arrayin)

point1 = arrayin[n]
index2 = n + m
point2 = arrayin[index2]

#End background stuff, start distance calculation
#Make the size of the unit cell into a unit vector in all directions
def distance(point1, point2):
    
    boundaries = np.repeat (1, d)

    Lsum2 = 0
    for i in range(len(point1)):
        #Simple distance along one axis
        delta = abs(point1[i] - point2[i])
        #Taking into account PBCs - this would work just as well for a cell of any size
        if delta > (boundaries[i]/2):
            delta = boundaries[i] - delta
        Lsum2 += delta ** 2

    return Lsum2

#print(np.sqrt(Lsum2))

#Basic loop which does not account for PBCs:
#Lsum2 = 0
#for i in range(len(point1)):
#    Lsum2 += (point1[i] - point2[i])**2
