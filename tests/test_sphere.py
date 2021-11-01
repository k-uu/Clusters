from clusters import initialize
import numpy as np
import matplotlib.pyplot as plt
import os
import sys


# suppress printing
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


# input variables
# n: number of particles
# eq_distance: equilibrium distance between particles
# r: radius of sphere

n = 20
eq_distance = 1.0
r = initialize.calculate_radius(n, eq_distance)

trajfile = "trajectory.xyz"

outputfile = open(trajfile, "w")
time = 0

with HiddenPrints():
    pos = initialize.populate_sphere(r, n)
    outputfile.write('{}\n'.format(n))
    outputfile.write('{:8.7g}\n'.format(time))
    for i in range(n):
        outputfile.write('LJ {:12.6g} {:12.6g} {:12.6g} \n'.format(pos[i, 0], pos[i, 1], pos[i, 2]))

# Plotting initial configuration

# %matplotlib inline

fig = plt.figure()
ax = plt.axes(projection='3d')

# Create a sphere
pi = np.pi
cos = np.cos
sin = np.sin
phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0 * pi:100j]
x = r * sin(phi) * cos(theta)
y = r * sin(phi) * sin(theta)
z = r * cos(phi)

xdata = pos[:, 0]
ydata = pos[:, 1]
zdata = pos[:, 2]
ax.plot_surface(
    x, y, z, rstride=1, cstride=1, color='c', alpha=0.6, linewidth=0)
ax.scatter(xdata, ydata, zdata, color="k", s=20)
