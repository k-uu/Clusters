import math

import numpy as np
import initialize


# represents an operator used to create new clusters where rate is its creation rate
class Operator:
    def __init__(self, rate):
        self.rate = rate

    # apply operator to clusters and produce new individuals based on the population size
    def apply(self, clusters, size):
        pass


# selected atoms are displaced randomly over the surface of a sphere of radius equal to to there distance from cluster
# center
class AngularOperator(Operator):
    def apply(self, clusters, size):
        target_count = int(size * self.rate)
        rng = np.random.default_rng()
        targets = rng.choice(clusters, target_count, replace=False)
        percent = 0.05
        for t in targets:
            index_p = rng.choice(np.arange(0, t.size), int(math.ceil(t.size * percent)), replace=False)
            for p in index_p:
                r = np.sqrt(np.dot(t.pos[p], t.pos[p]))
                pi = np.pi
                phi = rng.uniform(0, 1) * pi
                theta = rng.uniform(0, 2) * pi

                tmp = r * np.sin(phi)
                x = tmp * np.cos(theta)
                y = tmp * np.sin(theta)
                z = r * np.cos(phi)
                t.pos[p] = [x, y, z]
        return targets


def mean_energy(clusters):
    return sum(clusters) / len(clusters)


# piece-wise function that determines the variance to a operator creation rate based off of previous average energy
def creation_variance(delta_e):
    e_max = 2.0
    v_max = 0.9
    if delta_e < -e_max:
        return v_max
    elif delta_e > e_max:
        return -v_max
    else:
        return v_max / e_max * delta_e


# determines the new creation rate for a given operator given the previous population average energy, its newly created
# individuals and previous creation rate
def new_rate(e_prev, created, rate_prev):
    variance = 0.0
    for cluster in created:
        delta_e = cluster - e_prev
        variance += creation_variance(delta_e)

    return rate_prev + variance


# given a list of operators, normalize their creation rates to unity
def normalize(operators):
    total = 0.0
    for o in operators:
        total += o.rate

    for o in operators:
        o.rate = o.rate / total
    return


# op = AngularOperator(0.5)
# pop = initialize.make_population(2, 5)
# print(pop[0].pos)
# print(pop[1].pos)
# print(res := op.apply(pop, 2))
# print(res[0].pos)



