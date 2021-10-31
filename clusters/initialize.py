import numpy as np

# calculate radius to be used to initialize clusters given the number of particles and
# the equilibrium distance between them
def calculate_radius(n, equilibrium_distance):
    return equilibrium_distance * (0.5 + pow((3 * n) / (4 * np.pi * np.sqrt(2)), (1 / 3)))


# TODO: this may get stuck in a loop
# populate a sphere with a n randomly placed points within a distance threshold
def populate_sphere(radius, n):
    pos = np.zeros((n, 3))
    count = 0
    while count < n:
        point = get_point(radius)
        if check_threshold(pos, point, 0.8):
            pos[count] = point
            count += 1
    return pos


# generate a random point within a sphere with radius
def get_point(radius):
    rng = np.random.default_rng()
    vec = rng.standard_normal(3)
    r = (rng.uniform(0, 1)) ** (1 / 3) * radius

    mag = np.sqrt(np.dot(vec, vec))

    print(vec * r / mag)
    return vec * r / mag


# given current positions and the new position, returns true if the new position does not lie
# within certain distance between any current positions
def check_threshold(pos, p, distance):
    for i in pos:
        v = i - p
        if np.dot(v, v) < distance ** 2:
            return False
    return True

