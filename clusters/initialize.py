import numpy as np


class Cluster:

    def __init__(self, n, equilibrium_distance):
        self.pos = populate_sphere(n, equilibrium_distance)
        self.size = n

    def energy(self):
        return calculate_lj_energy(self.pos, self.size)


# calculate radius to be used to initialize clusters given the number of particles and
# the equilibrium distance between them
def calculate_radius(n, equilibrium_distance):
    return equilibrium_distance * (0.5 + pow((3 * n) / (4 * np.pi * np.sqrt(2)), (1 / 3)))


# LJ potential energy in reduced units: r = r / sigma, energy = energy / epsilon
def calculate_lj_energy(pos, n):
    energy = 0.0
    for i in range(n - 1):
        for j in range(i + 1, n):
            r_ij = pos[i] - pos[j]
            r_ij2 = np.dot(r_ij, r_ij)
            r_ij6_inv = 1 / (r_ij2 ** 3)
            energy += 4 * r_ij6_inv * (r_ij6_inv - 1)
    return energy


# populate a sphere with n randomly placed points with equilibrium distance >= separation distance (0.8)
def populate_sphere(n, equilibrium_distance):
    threshold = 0.8
    if equilibrium_distance < threshold:
        raise Exception("Equilibrium distance needs to be <= {}".format(threshold))

    radius = calculate_radius(n, equilibrium_distance)
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


# return a population of clusters with given size, number of particles per cluster and particle equilibrium distance
def make_population(size, particles, equilibrium_distance):

    return [Cluster(particles, equilibrium_distance) for i in range(size)]


