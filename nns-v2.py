import numpy as np
import sys
from euclideandistance import distance
import time

tstart = time.time()

infile = sys.argv[1]

#Open file with randomly generated array
arrayin = np.loadtxt(infile, delimiter=" ")

#Figure out d and N from array
#txt variables for naming the output file later
d = arrayin.ndim
dtxt = str(d)
N = len(arrayin)
Ntxt = str(N)
sigma = (1/((N)**(1/d)))
cutoff = sigma ** 2
sigmatxt = str(sigma)

#Open file to store pairs
pairfilename = ("neighbors_d" + dtxt + "N" + Ntxt + "sigma" + sigmatxt)
with open(pairfilename, "w") as outfile:
    outfile.write("Index1 Index2 Coordinates1 Coordinates2 Distance\n")

    #Start loop over n
    for n in range(N):
        #Start loop over m
        for m in range(n + 1, N):
            point1 = arrayin[n]
            point2 = arrayin[m]

            #Call Euclidean distance function
            dist = distance(point1, point2)

            #Compare to cutoff
            if dist < cutoff:
                #Write to the output file
                coord1_str = " ".join(map(str, point1))
                coord2_str = " ".join(map(str, point2))
                outfile.write(f"{n} {m} {coord1_str} {coord2_str} {dist:.6f}\n")

print("All pairs found. Results saved to " + pairfilename)

tend = time.time()

ttotal = tend - tstart
totaltime = str(ttotal)

print("Execution complete. Total time elapsed: " + totaltime + " seconds")
