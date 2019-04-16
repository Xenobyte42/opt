import math


def sphere_function(x_vec):
    F = 0
    for i in range(len(x_vec)):
        F += pow(x_vec[i], 2)
    return F


def rozenbrock_function(x_vec):
    x_0 = 0
    F = 0
    for i in range(len(x_vec) - 1):
        zi = x_vec[i] - x_0
        zi1 = x_vec[i + 1] - x_0
        F += 100 * (pow(pow(zi, 2) - zi1, 2) + pow(zi - 1, 2))
    return F


def rastr_function(x_vec):
    F = 0
    x_0 = 0
    for i in range(len(x_vec)):
        z = x_vec[i] - x_0
        F += pow(z, 2) - 10 * math.cos(2 * z * math.pi) + 10
    return F
