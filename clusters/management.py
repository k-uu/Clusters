import math

import numpy as np
from clusters import initialize


# represents an abstract operator used to create new clusters from existing ones where rate is its creation rate
class Operator:
    def __init__(self, rate):
        self.rate = rate

    # apply operator to clusters and produce new individuals based on the population size
    def apply(self, clusters, size):
        pass


# selected particles in a cluster are displaced randomly over the surface of a sphere of radius
# equal to to there distance from cluster center
class AngularOperator(Operator):
    def apply(self, clusters, size):
        rng = np.random.default_rng()
        targets = get_targets(self, clusters, size)
        percent = 0.05  # 5% of the particles are moved
        p_count = targets[0].size
        for t in targets:

            # take a random sample from the list of particle positions
            index_p = rng.choice(np.arange(0, p_count), int(math.ceil(p_count * percent)), replace=False)
            for p in index_p:
                r = np.sqrt(np.dot(t.pos[p], t.pos[p]))
                pi = np.pi
                phi = rng.uniform(0, 1) * pi
                theta = rng.uniform(0, 2) * pi

                # displace in spherical coordinates and then convert to cartesian
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


# produces individuals by rotating a half of the cluster about a random axis by [0.1-0.5] radians
class TwistOperator(Operator):
    def apply(self, clusters, size):
        rng = np.random.default_rng()
        targets = get_targets(self, clusters, size)
        index_p = targets[0].size
        for t in targets:
            rot = rng.uniform(0.1, 0.5) * np.pi
            point = initialize.get_point(1)
            ax = point / np.linalg.norm(point)  # convert random point to unity to be used as axis of rotation
            cos = np.cos(rot)
            sin = np.sin(rot)

            # matrix that represents a rotation of rot radians about ax
            rot_mat = cos * np.identity(3) + sin * np.cross(ax, np.identity(3) * -1) + (1 - cos) * np.outer(ax, ax)
            for p in range(index_p):
                if np.dot(t.pos[p], ax) >= 0:
                    t.pos[p] = np.matmul(rot_mat, t.pos[p])
        return targets


def mean_energy(clusters):
    return sum(clusters) / len(clusters)


# returns a random selection from clusters based on the operator creation rate and
# final size of new population. Returns at least one selection
def get_targets(op, clusters, size):
    target_count = math.ceil(size * op.rate)
    rng = np.random.default_rng()
    targets = rng.choice([c.duplicate() for c in clusters], target_count, replace=False)
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


# updates the creation rate for a given operator given the previous population average energy compared
# to it's newly created individuals
# CONSTRAINT: returns >= 0.01
def new_rate(e_prev, created, rate_prev):
    if not len(created):
        return 0.01

    variance = 0.0
    for cluster in created:
        delta_e = cluster - e_prev
        variance += creation_variance(delta_e)

    rate = rate_prev + variance / len(created)

    if rate <= 0:
        return 0.01
    else:
        return rate


# given a list of operators, normalize their creation rates to unity
def normalize(operators):
    total = 0.0
    count = 0
    for o in operators:
        total += o.rate
        count += 1

    for i in range(count):
        operators[i].rate = operators[i].rate / total

    return operators
