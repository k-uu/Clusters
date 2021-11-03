from clusters import initialize

# creates file in xyz format with initial population

# input variables
# pop_size: population size
# n: number of particles
# eq_distance: equilibrium distance between particles

pop_size = 10
n = 5
eq_distance = 1.0

# create initial population
pop_list = initialize.make_population(10, 5, 1.0)

# create xyz file where each frame is cluster in the population
file = "initial_population.xyz"
outputfile = open(file, "w")

for i in range(pop_size):
    outputfile.write('{}\n'.format(n))
    outputfile.write('Energy: {}\n'.format(pop_list[i].energy()))
    p = pop_list[i].pos
    for j in range(n):
        outputfile.write('LJ {:12.6g} {:12.6g} {:12.6g} \n'.format(*p[j]))
