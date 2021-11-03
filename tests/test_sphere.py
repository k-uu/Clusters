from clusters import initialize
import numpy as np
import matplotlib.pyplot as plt

# input variables
# n: number of particles
# eq_distance: equilibrium distance between particles >= 0.8
# r: radius of sphere
# p: population size

p = 10
n = 100
eq_distance = 0.8
r = initialize.calculate_radius(n, eq_distance)
pop = initialize.make_population(p, n, eq_distance)
pos = pop[0].pos


fig = plt.figure()
ax = plt.axes(projection='3d')

# plot a sphere containing points
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

plt.show()
