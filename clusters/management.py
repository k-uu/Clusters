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
        rng = np.random.default_rng()
        targets = get_targets(self, clusters, size)
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


# produces new individuals in the same manner the initial population was created
class ImmigrateOperator(Operator):
    def apply(self, clusters, size):
        particles = clusters[0].size
        target_count = int(size * self.rate)
        return initialize.make_population(target_count, particles)


# produces individuals by rotating half the cluster about the x-axis by a random amount
class TwistOperator(Operator):
    def apply(self, clusters, size):
        rng = np.random.default_rng()
        targets = get_targets(self, clusters, size)
        index_p = len(targets[0].pos)
        for t in targets:
            rot = rng.uniform(0.1, 0.5) * np.pi
            cos = np.cos(rot)
            sin = np.sin(rot)
            rot_x_mat = np.array([[1, 0, 0],
                                  [0, cos, -sin],
                                  [0, sin, cos]])
            for p in range(index_p):
                if np.dot(t.pos[p], [1, 0, 0]) >= 0:
                    t.pos[p] = np.matmul(rot_x_mat, t.pos[p])
        return targets


def mean_energy(clusters):
    return sum(clusters) / len(clusters)


# returns a random selection from clusters based on the operator creation rate and
# final size of new population
def get_targets(op, clusters, size):
    target_count = int(size * op.rate)
    rng = np.random.default_rng()
    targets = rng.choice(clusters, target_count, replace=False)
    return targets


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


# op = TwistOperator(0.5)
# pop = initialize.make_population(2, 5)
# print(pop[0].pos)
# print(pop[1].pos)
# print(res := op.apply(pop, 2))
# print("After")
# print(res[0].pos)



