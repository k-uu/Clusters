import numpy as np

from clusters import initialize
from clusters import minimize
from tests.test_sphere import plot_cluster
from matplotlib import pyplot as plt


fig, ax = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
size = 26
c = initialize.Cluster(size)
radius = initialize.calculate_radius(size)
print(c.energy())
plot_cluster(c, ax[0], 'r')
res, steps = minimize.minimize(c)
c.pos = res
print("minima of {} in {} steps".format(c.energy(), steps))
plot_cluster(c, ax[1], 'g')

for i in range(len(res)):
    p = res[i]
    if np.sqrt(np.dot(p, p)) > radius:
        print("Point outside of sphere")
print("all good")

plt.show()
