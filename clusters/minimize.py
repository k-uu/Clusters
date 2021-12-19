import scipy.optimize
import numpy as np
import click


# perform local minimization of Lennard Jones potential based on current particle positions using BFGS algorithm
def optimize(positions):
    # flatten current positions array: [[x1, y1, z1], [x2, y2, z2]] -> [x1, y1, z1, x2, y2, z2]
    data = positions.flatten().tolist()
    size = len(data)

    # lennard jones potential using flattened positions array
    def lj(pos):
        energy = 0.0
        for i in range(0, size - 3, 3):
            for j in range(i + 3, size, 3):
                r_ij = pos[i:i+3] - pos[j:j+3]
                r_ij2 = np.dot(r_ij, r_ij)
                r_ij6_inv = 1 / (r_ij2 ** 3)
                energy += 4 * r_ij6_inv * (r_ij6_inv - 1)
        return energy

    # gradient of lennard jones potential using flattened positions array
    def d_lj(pos):
        gradient = np.empty(0)
        for i in range(0, size, 3):
            tmp = np.zeros(3)
            for j in range(0, size, 3):
                if i != j:
                    r_ij = pos[i:i+3] - pos[j:j+3]
                    r_ij2 = np.dot(r_ij, r_ij)
                    r_ij6_inv = 1 / (r_ij2 ** 3)
                    tmp += -24 * r_ij6_inv * (2 * r_ij6_inv - 1) * r_ij / r_ij2
            gradient = np.append(gradient, tmp)
        return gradient

    result = scipy.optimize.minimize(lj, data, method='L-BFGS-B', jac=d_lj)
    click.echo(".", nl=False)  # ui component
    positions = np.reshape(result['x'], (-1, 3))
    return lj(result['x']), positions
