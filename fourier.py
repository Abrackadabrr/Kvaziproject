import numpy as np
from scipy.fft import fft
import cmath


def data():
    N = 1000
    t_s = np.linspace(0, 100, N)
    # data = np.array([complex(np.cos(i), np.sin(i)) for i in t * 6.28])
    # data = "0,4 1,6 2,8 4,10 5,12 6,14 7,16 10,18 12,19 13,20 15,21 14,22 14,24 15,25 18,27 20,30 22,31"
    # data = data.split(" ")
    # points = [i.split(",") for i in data]
    # print(points)
    # points = [int(i[0]) + int(i[1])*1j for i in points]
    # print(points)
    # points = [cmath.exp(np.absolute(i)+np.angle(i)*1j) for i in points]
    k = 3
    # points = [(2 * 1j ** t - 1j ** (-t)) * (np.cos(5 * np.pi * (k + t / 2)) + 0.5 * np.cos(11 * np.pi * (k + t / 2)))
    #           + 8 * 1j ** t + 2 * 1j ** (-t) for t in t_s]
    # points = [1j * (1j ** -t + 1.9*1j ** (2*t/3) + 1j**(-2*t)) for t in t_s]
    points = [(3 * np.cos(np.pi * t) + 2j * np.sin(np.pi * t)) * (3 * np.cos(11 * np.pi * (k + t)) + np.cos(7 * np.pi * (k + t))) +
              9 * (4 * np.cos(np.pi * t) + 2j) for t in t_s]

    f_s = []
    M = 100
    n = len(points)
    dt = 1 / n
    for j in range(-M, M + 1):
        f = 0
        for i in range(n):
            f += (points[i] * cmath.exp(-2 * cmath.pi * i * dt * j * 1j) * dt)
        f_s.append(f)

    angles = np.angle(f_s)
    norms = np.absolute(f_s)
    return len(norms), norms, angles, M
