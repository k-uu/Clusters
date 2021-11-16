import numpy as np


# sorts from low to high and removes the percent% highest energy Clusters from the list of Clusters
def remove_top_percent(clusters, percent):
    size = len(clusters)
    count = int(percent * size / 100)
    clusters.sort()
    return np.delete(clusters, np.s_[(size - count): size])


# return true if at least of the the clusters has reached the energy minima
def converged(clusters, energy):
    for c in clusters:
        if c.energy() <= energy:
            return True
    return False

