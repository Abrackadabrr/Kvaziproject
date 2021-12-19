import numpy as np
from math import sin, cos
import integrators as it
import matplotlib.pyplot as plt


class NStickPendulum:
    def __init__(self, n, omega):
        """
        Model of n-stick-pendulum
        :param n: number of sticks
        :param omega: free fall acceleration/length
        """
        self.omega = omega
        self.n = int(n)

    def func(self, state, time):
        psi = self.psi(state)
        xi = np.array(state[self.n:2 * self.n])
        return np.concatenate((xi, psi))

    def solve(self, in_state, time_step, full_time):
        in_state = np.array(in_state)
        n_iters = int(full_time / time_step)
        result = it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)
        return result

    def sum1(self, state, stop):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        return np.array([0] * self.n + [(ders[0:stop] * np.cos(ans[0:stop])).sum()])

    def sum2(self, state, stop):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        return np.array([0] * self.n + [(ders[0:stop] * np.sin(ans[0:stop])).sum()])

    def derSum1(self, state, stop):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]

        first_part = np.concatenate((np.cos(ans[0:stop]), np.array([0] * (self.n - stop + 1))))
        assert type(self.n) == int
        second_part = np.array([0] * self.n + [((ders[0:stop] * ders[0:stop] * np.sin(ans[0:stop])).sum())])

        return first_part - second_part

    def derSum2(self, state, stop):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]

        first_part = np.concatenate((np.sin(ans[0:stop]), np.array([0] * (self.n - stop + 1))))

        second_part = np.array([0] * self.n + [(ders[0:stop] * ders[0:stop] * np.cos(ans[0:stop])).sum()])

        return first_part + second_part

    def A(self, state, stop, k):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        cos_k = cos(ans[k])
        sin_k = sin(ans[k])
        ders_k = ders[k]

        s1 = self.derSum1(state, stop) * cos_k
        s2 = self.sum1(state, stop) * ((-1) * sin_k * ders_k)
        s3 = self.derSum2(state, stop) * sin_k
        s4 = self.sum2(state, stop) * (cos_k * ders_k)

        return s1 + s2 + s3 + s4

    def d_dt_dTj_dphik(self, state, j, k):
        """
        Counting of ders by time in special format
        :return: np.ndarray of koef phi_k_2der
        """
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]

        ans_k = ans[k]
        ans_j = ans[j]
        ders_k = ders[k]
        ders_j = ders[j]

        A = self.A(state, j, k)

        if k > j:
            return np.zeros(self.n + 1)

        if k == j:
            s1 = (1 / 2) * A
            s2 = np.array([0] * j + [(1 / 3)] + [0] * (self.n - j))
            return s1 + s2

        if k < j:
            s1 = A
            s2 = np.array([0] * j + [(1 / 2) * cos(ans_j - ans_k)] + [0] * (self.n - j))
            s3 = np.array([0] * self.n + [(1 / 2) * (ders_j * sin(ans_j - ans_k) * (ders_k - ders_j))])
            return s1 + s2 + s3

    def dTj_dphik(self, state, j, k):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]

        sum1 = self.sum1(state, j)
        sum2 = self.sum2(state, j)

        ans_k = ans[k]
        ans_j = ans[j]
        ders_k = ders[k]
        ders_j = ders[j]

        if k > j:
            return np.zeros(self.n + 1)

        if k == j:
            s1 = sum1 * ((-1) * ders_k * sin(ans_k))
            s2 = sum2 * (ders_k * cos(ans_k))
            return (1 / 2) * (s1 + s2)

        if k < j:
            s1 = sum1 * ((-1) * ders_k * sin(ans_k))
            s2 = sum2 * (ders_k * cos(ans_k))
            s3 = np.array([0] * self.n + [ders_k * cos(ans_k) * ders_j * sin(ans_j)])
            s4 = np.array([0] * self.n + [ders_k * sin(ans_k) * ders_j * cos(ans_j)])
            return s1 + s2 + (1 / 2) * (s3 - s4)

    def dPi_dphik(self, state, j, k):
        ans_k = state[k]

        if k < j:
            return np.array([0] * self.n + [np.sin(ans_k) * self.omega])
        if k == j:
            return np.array([0] * self.n + [np.sin(ans_k) * self.omega / 2])
        if k > j:
            return np.zeros(self.n + 1)

    def count_d_dt_dT_dphik(self, state, k):
        a = np.zeros(self.n + 1, dtype=np.float64)
        for j in range(self.n):
            a += self.d_dt_dTj_dphik(state, j, k)
        return a

    def count_dP_dphik(self, state, k):
        a = np.array([0] * (self.n + 1), dtype=np.float64)
        for j in range(self.n):
            a += self.dPi_dphik(state, j, k)
        return a

    def count_dT_dphik(self, state, k):
        a = np.array([0] * (self.n + 1), dtype=np.float64)
        for j in range(self.n):
            a += self.dTj_dphik(state, j, k)
        return a

    def get_k_matrix_line(self, state, k):
        return self.count_d_dt_dT_dphik(state, k) - self.count_dT_dphik(state, k) + self.count_dP_dphik(state, k)

    def get_k_matrix_line2(self, state, k):
        a = np.zeros(self.n + 1, dtype=np.float64)
        for j in range(self.n):
            a += self.d_dt_dTj_dphik(state, j, k)
            a -= self.dTj_dphik(state, j, k)
            a += self.dPi_dphik(state, j, k)
        return a

    def psi(self, state):
        a = []
        for k in range(self.n):
            a_ = self.get_k_matrix_line2(state, k)
            a.append(a_)
        a = np.array(a)
        b = -a[:, self.n]
        a = a[:, 0:self.n]
        x = np.linalg.solve(a, b)
        return x

    def count_kinen_j(self, state, stop):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        s1 = (1/2)*(self.sum1(state, stop)[-1]**2 + self.sum2(state, stop)[-1]**2)
        s2 = (1/6)*(ders[stop]**2)
        s3 = (1/2)*((self.sum1(state, stop)[-1])*ders[stop]*cos(ans[stop]) + (self.sum2(state, stop)[-1])*ders[stop]*sin(ans[stop]))
        return s1 + s2 + s3

    def count_poten_j(self, state, stop):
        ans = state[0:self.n]
        s1 = np.cos(ans[0:stop]).sum()
        s2 = cos(ans[stop])/2
        return (-1)*self.omega*(s1+s2)

    def count_energy(self, state):
        energy = 0
        for j in range(self.n):
            energy += self.count_poten_j(state, j)
            energy += self.count_kinen_j(state, j)
        return energy


if __name__ == '__main__':
    print('Make sure you do all right')
