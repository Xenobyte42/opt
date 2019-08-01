import numpy as np


def sphere_function(x_vec):
    F = 0
    for i in range(len(x_vec)):
        F += np.power(x_vec[i], 2)
    return F


def rozenbrock_function(x_vec):
    x_0 = 0
    F = 0
    for i in range(len(x_vec) - 1):
        zi = x_vec[i] - x_0
        zi1 = x_vec[i + 1] - x_0
        F += 100 * (np.power(np.power(zi, 2) - zi1, 2) + np.power(zi - 1, 2))
    return F


def rastr_function(x_vec):
    F = 0
    x_0 = 0
    for i in range(len(x_vec)):
        z = x_vec[i] - x_0
        F += np.power(z, 2) - 10 * np.cos(2 * z * np.pi) + 10
    return F
