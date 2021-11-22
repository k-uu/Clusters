
from clusters import initialize
from clusters import management
from clusters import selection

import numpy as np

# initial population
target_energy = -61.31799
n = 17
pop_size = 50

pop = initialize.make_population(pop_size, n)

operators = [management.AngularOperator(0.3), management.TwistOperator(0.4), management.ImmigrateOperator(0.3)]


# loop
while not selection.converged(pop, target_energy):

    pop = selection.remove_top_percent(pop, 20)

    prev_energy = management.mean_energy(pop)
    
    size = pop_size - len(pop)

    for i, op in enumerate(operators):
        created = op.apply(pop, size)
        rate = management.new_rate(prev_energy, created, op.rate)
        operators[i].rate = rate
        pop = np.concatenate((created, pop))

    management.normalize(operators)

    print(min(pop))
    for op in operators:
        print(op.rate)

print(pop)





