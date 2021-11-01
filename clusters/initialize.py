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

# supress printing

import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
 

###############
###test area###
###############

#input variables
    # n: number of particles
    # eq_distance: equilibrium distance between particles
    # r: radius of sphere

n = 20
eq_distance = 1.0
r = calculate_radius(n, eq_distance)

trajfile = "trajectory.xyz"

outputfile = open(trajfile,"w")
time = 0

with HiddenPrints():
    pos = populate_sphere(r, n)
    outputfile.write('{}\n'.format(n))
    outputfile.write('{:8.7g}\n'.format(time))
    for i in range(n):
        outputfile.write('LJ {:12.6g} {:12.6g} {:12.6g} \n'.format(pos[i,0], pos[i,1], pos[i,2]))
      
#Plotting initial configuration

%matplotlib inline
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection='3d')

# Create a sphere
pi = np.pi
cos = np.cos
sin = np.sin
phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0*pi:100j]
x = r*sin(phi)*cos(theta)
y = r*sin(phi)*sin(theta)
z = r*cos(phi)

xdata = pos[:,0]
ydata = pos[:,1]
zdata = pos[:,2]
ax.plot_surface(
    x, y, z,  rstride=1, cstride=1, color='c', alpha=0.6, linewidth=0)
ax.scatter(xdata,ydata,zdata,color="k",s=20)


###############
###test area###
###############
