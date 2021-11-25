import scipy.optimize as optimize
import numpy as np


def minimize(cluster):
    data = cluster.pos.flatten().tolist()
    size = len(data)

    def lj(pos):
        energy = 0.0
        for i in range(0, size - 3, 3):
            for j in range(i + 3, size, 3):
                r_ij = pos[i:i+3] - pos[j:j+3]
                r_ij2 = np.dot(r_ij, r_ij)
                r_ij6_inv = 1 / (r_ij2 ** 3)
                energy += 4 * r_ij6_inv * (r_ij6_inv - 1)
        return energy

    def d_lj(pos):
        arr = np.empty(0)
        for i in range(0, size, 3):
            tmp = np.zeros(3)
            for j in range(0, size, 3):
                if i != j:
                    r_ij = pos[i:i+3] - pos[j:j+3]
                    r_ij2 = np.dot(r_ij, r_ij)
                    r_ij6_inv = 1 / (r_ij2 ** 3)
                    tmp += -24 / r_ij2 * r_ij6_inv * (2 * r_ij6_inv - 1) * r_ij
            arr = np.append(arr, tmp)
        return arr

    result = optimize.minimize(lj, data, method='BFGS', jac=d_lj)
    print(result['message'], result['x'])
    return np.reshape(result['x'], (-1, 3)), result['nfev']



