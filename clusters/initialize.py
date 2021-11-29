import numpy as np

from clusters import minimize


# Represents a cluster made up of n particles
class Cluster:

    def __init__(self, n):
        self.pos = populate_sphere(n)
        self.size = n
        self.e = None

    def energy(self):
        if not self.e:
            self.e, self.pos = minimize.minimize(self.pos)
        return self.e

    def duplicate(self):
        copy = Cluster(1)
        copy.size = self.size
        copy.pos = self.pos.copy()  # >:(
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


# calculate radius to be used to initialize clusters given the number of particles
def calculate_radius(n):
    equilibrium_distance = 2 ** (1 / 6)  # minimum energy (equilibrium) distance given LJ reduced units
    return equilibrium_distance * (0.5 + pow((3 * n) / (4 * np.pi * np.sqrt(2)), (1 / 3)))


# populate a sphere with n randomly placed but separated points
def populate_sphere(n):
    threshold = 0.8

    radius = calculate_radius(n)
    pos = np.zeros((n, 3))
    count = 0
    while count < n:
        point = get_point(radius)
        if check_threshold(pos, point, threshold):
            pos[count] = point
            count += 1
    return pos


# generate a random point within a sphere with radius
def get_point(radius):
    rng = np.random.default_rng()
    vec = rng.standard_normal(3)
    r = (rng.uniform(0, 1)) ** (1 / 3) * radius

    mag = np.sqrt(np.dot(vec, vec))

    return vec * r / mag


# given current positions and the new position, returns true if the new position does not lie
# within certain distance between any current positions
def check_threshold(pos, p, distance):
    for i in pos:
        diff = i - p
        if np.dot(diff, diff) < distance ** 2:
            return False
    return True


# return a population of clusters with given size, number of particles per cluster
def make_population(size, particles):

    return np.array([Cluster(particles) for i in range(size)])


