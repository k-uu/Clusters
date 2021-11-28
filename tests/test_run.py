
from clusters import initialize
from clusters import management
from clusters import selection
from tests import test_sphere
from matplotlib import pyplot as plt

import numpy as np

# initial population
target_energy = -108.315616
n = 26
pop_size = 40

pop = initialize.make_population(pop_size, n)

operators = [management.AngularOperator(0.3), management.TwistOperator(0.4), management.ImmigrateOperator(0.3)]

# loop
while not selection.converged(pop, target_energy):

    pop = selection.remove_top_percent(pop, 25)

    prev_energy = management.mean_energy(pop)
    
    size = pop_size - len(pop)

    for i, op in enumerate(operators):
        created = op.apply(pop, size)
        rate = management.new_rate(prev_energy, created, op.rate)
        operators[i].rate = rate
        pop = np.concatenate((created, pop))

    management.normalize(operators)

    print(min(pop))

result = pop[np.argmin(pop)]
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
test_sphere.plot_cluster(result, ax, 'r')
plt.show()

with open("structure.xyz", 'w') as f:
    f.write('{}\n'.format(n))
    f.write('Energy: {}\n'.format(result.energy()))
    for j in range(n):
        f.write('LJ {:12.6g} {:12.6g} {:12.6g} \n'.format(*result.pos[j]))






