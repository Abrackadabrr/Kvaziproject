import matplotlib.pyplot as plt
import numpy as np
from math import *
import integrators as it


class MathPendulum:
    def __init__(self, omega):
        self.omega = omega

    def func(self, state, time):
        psi = -self.omega * np.sin(state[0])
        xi = state[1]
        return np.array([xi, psi])

    def solve(self, in_state, time_step, full_time):
        n_iters = int(full_time / time_step)
        return it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)


class TwoStickPendulum:
    def __init__(self, omega):
        self.omega = omega
        pass

    def func(self, state, time):
        state = np.array(state)
        psi = self.psi(state, time)
        xi = state[2:4]
        return np.concatenate((xi, psi))

    def solve(self, in_state, time_step, full_time):
        in_state = np.array(in_state)
        n_iters = int(full_time / time_step)
        result = it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)
        energy = np.array(map(self.count_energy, result))
        plt.plot(np.arange(0, 10.00001, 0.01), energy)
        plt.show()
        return result

    def psi(self, state, time):
        A = np.array([[1, (3 / 8) * np.cos(state[1] - state[0])],
                      [(3 / 2) * np.cos(state[1] - state[0]), 1]])

        b1 = (3 / 8) * state[3] * (state[3] - state[2]) * np.sin(state[1] - state[0]) + (3 / 8) * state[3] * state[
            2] * np.sin(state[1] - state[0]) - (9 / 8) * np.sin(state[0]) * self.omega  # g/l
        b2 = (3 / 2) * state[2] * (state[3] - state[2]) * np.sin(state[1] - state[0]) - (3 / 2) * state[3] * state[
            2] * np.sin(state[1] - state[0]) - (3 / 2) * np.sin(state[1]) * self.omega  # g/l
        b = np.array([b1, b2])
        x = np.linalg.solve(A, b)

        return x

    def sum1(self, state, stop):
        if stop <= 0:
            return np.zeros(3)

        ans = state[0:2]
        ders = state[2:4]
        return np.array([0] * 2 + [(ders[0:stop] * np.cos(ans[0:stop])).sum()])

    def sum2(self, state, stop):
        if stop <= 0:
            return np.zeros(3)

        ans = state[0:2]
        ders = state[2:4]
        return np.array([0] * 2 + [(ders[0:stop] * np.sin(ans[0:stop])).sum()])

    def count_kinen_j(self, state, stop):
        ans = state[0:2]
        ders = state[2:4]

        s1 = (1/2)*(self.sum1(state, stop)[-1]**2 + self.sum2(state, stop)[-1]**2)
        s2 = (1/6)*(ders[stop]**2)
        s3 = (1/2)*((self.sum1(state, stop)[-1])*ders[stop]*cos(ans[stop]) + (self.sum2(state, stop)[-1])*ders[stop]*sin(ans[stop]))
        return s1 + s2 + s3

    def count_poten_j(self, state, stop):
        ans = state[0:2]
        s1 = np.cos(ans[0:stop]).sum()
        s2 = cos(ans[stop])/2
        return (-1)*self.omega*(s1+s2)

    def count_energy(self, state):
        energy = 0
        for j in range(2):
            energy += self.count_poten_j(state, j)
            energy += self.count_kinen_j(state, j)
        return energy
