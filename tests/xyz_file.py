from clusters import initialize
import numpy as np

# creates file in xyz format with initial population

#input variables
    # pop_size: population size
    # n: number of particles
    # eq_distance: equilibrium distance between particles

pop_size = 10
n = 5
eq_distance = 1.0

# create initial population

pop_list = initialize.make_population(10, 5, 1.0)

#create xyz file

file = "initial_population.xyz"
outputfile = open(file,"w")

for i in range(pop_size):
    pos = pop_list[0].position()
    outputfile.write('{}\n'.format(pop_size))
    outputfile.write('{:8.7g}\n'.format(i))
    for i in range(n):
        outputfile.write('LJ {:12.6g} {:12.6g} {:12.6g} \n'.format(pos[i,0], pos[i,1], pos[i,2]))
