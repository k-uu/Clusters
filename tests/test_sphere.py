from clusters import initialize
from clusters import management
import numpy as np
import matplotlib.pyplot as plt


# plot a sphere on a pyplot axis
def plot_sphere(cluster, axis):

    r = initialize.calculate_radius(cluster.size)

    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0 * pi:100j]
    x = r * sin(phi) * cos(theta)
    y = r * sin(phi) * sin(theta)
    z = r * cos(phi)

    axis.plot_surface(
        x, y, z, rstride=1, cstride=1, color='c', alpha=0.4, linewidth=0)


# plot 3D vectors on axis
def plot_vectors(vectors, ax, color):
    x_data = vectors[:, 0]
    y_data = vectors[:, 1]
    z_data = vectors[:, 2]
    ax.scatter(x_data, y_data, z_data, color=color, s=20)


# plot the particles in a cluster confined in a sphere with radius defined by cluster
def plot_cluster(cluster, axis, color):
    plot_sphere(cluster, axis)
    plot_vectors(cluster.pos, axis, color)


# plot the results from applying a given Operator on a cluster with n particles
def test_operator(operator, n):

    pop = initialize.make_population(1, n)
    fig, axes = plt.subplots(1, subplot_kw={'projection': '3d'})

    plot_sphere(pop[0], axes)
    pos = pop[0].pos
    plot_vectors(pos, axes, 'k')
    result = operator.apply(pop, 1)[0].pos
    pos = np.array([after.tolist() for before, after in zip(pos, result) if not np.array_equal(before, after)])
    plot_vectors(pos, axes, 'red')

    plt.show()
