import numpy as np

from clusters import minimize


# Represents a Lennard Jones (LJ) cluster made up of n particles
class Cluster:

    # instantiate a cluster made up of n particles randomly distributed within an enclosing sphere
    def __init__(self, n):
        self.pos = populate_sphere(n)
        self.size = n
        self.e = None

    # returns the optimized LJ potential of self
    def energy(self):
        if not self.e:
            self.e, self.pos = minimize.optimize(self.pos)
        return self.e

    # duplicate the particle positions and size of an existing cluster into a new cluster (allows for the energy to
    # be calculated again)
    def duplicate(self):
        copy = Cluster(1)
        copy.size = self.size
        copy.pos = self.pos.copy()
        return copy

    def __lt__(self, other):
        return self.energy() < other.energy()

    def __repr__(self):
        return "Particles: {}, Energy: {}".format(self.size, self.energy())

    def __add__(self, other):
        if isinstance(other, Cluster):
            return self.energy() + other.energy()
        else:
            return self.energy() + other

    def __sub__(self, other):
        if isinstance(other, Cluster):
            return self.energy() - other.energy()
        else:
            return self.energy() - other

    def __rsub__(self, other):
        if isinstance(other, Cluster):
            return other.energy() - self.energy()
        else:
            return other - self.energy()

    __radd__ = __add__


# calculate n-dependent radius to be used to create the spherical boundary used in generating new clusters
def calculate_radius(n):
    equilibrium_distance = 2 ** (1 / 6)  # minimum energy (equilibrium) distance using LJ reduced units
    return equilibrium_distance * (0.5 + pow((3 * n) / (4 * np.pi * np.sqrt(2)), (1 / 3)))


# populate a sphere with n randomly placed but separated points
def populate_sphere(n):
    threshold = 0.8  # chosen to be smaller than the distance corresponding to reduced units LJ potential minimum

    radius = calculate_radius(n)
    pos = np.zeros((n, 3))
    count = 0
    while count < n:
        point = get_point(radius)
        if check_threshold(pos, point, threshold):
            pos[count] = point
            count += 1
    return pos


# generate a random point (x, y, z) within a sphere with radius
def get_point(radius):
    rng = np.random.default_rng()
    vec = rng.standard_normal(3)
    r = (rng.uniform(0, 1)) ** (1 / 3) * radius

    mag = np.sqrt(np.dot(vec, vec))

    return vec * r / mag


# given a list of points, returns true if the given new point does not lie
# within certain distance between any point in the list of points
def check_threshold(pos, new, distance):
    for i in pos:
        diff = i - new
        if np.dot(diff, diff) < distance ** 2:
            return False
    return True


# return a population of clusters with the given size and number of particles per cluster
def make_population(size, particles):

    return np.array([Cluster(particles) for i in range(size)])


