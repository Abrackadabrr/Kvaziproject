import matplotlib.pyplot as plt
import numpy as np
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
        n_iters = int(full_time / time_step)
        return it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)

    def psi(self, state, time):
        A = np.array([[1, (3 / 8) * np.cos(state[1] - state[0])],
                      [(3 / 2) * np.cos(state[1] - state[0]), 1]])

        b1 = (3 / 8) * state[3] * (state[3] - state[2]) * np.sin(state[1] - state[0]) + (3 / 8) * state[3] * state[
            2] * np.sin(state[1] - state[0]) - (9 / 8) * np.sin(state[0]) * self.omega  # g/l
        b2 = (3 / 2) * state[2] * (state[3] - state[2]) * np.sin(state[1] - state[0]) - (3 / 2) * state[3] * state[
            2] * np.sin(state[1] - state[0]) - (3 / 2) * np.sin(state[1]) * self.omega  # g/l
        b = np.array([b1, b2])
        x = np.linalg.solve(A, b)
        # print(A@x - b)
        return x


class NStickPendulum:
    def __init__(self, n, g, l, m):
        """
        Model of n-stick-pendulum
        :param n: number of sticks
        :param g: free fall acceleration
        :param l: length of stick
        :param m: mass of stick
        """
        self.g = g
        self.l = l
        self.m = m
        self.n = n

    def func(self, state, time):
        psi = self.psi(state)
        xi = state[self.n:2 * self.n]
        return np.concatenate((xi, psi))

    def solve(self, in_state, time_step, full_time):
        n_iters = int(full_time / time_step)
        return it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)

    def sum1(self, state, stop):
        if stop <= 0:
            return np.zeros(self.n + 1)
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        return np.array([0] * self.n + [-(self.l * np.sin(ans[0:stop]) * ders[0:stop]).sum()])

    def sum2(self, state, stop):
        if stop <= 0:
            return np.array([0] * (self.n + 1))
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        return np.array([0] * self.n + [(self.l * np.cos(ans[0:stop]) * ders[0:stop]).sum()])

    def sqrt(self, state, stop):
        return np.sqrt(self.sum1(state, stop)[self.n] ** 2 + self.sum2(state, stop)[self.n] ** 2)

    def derSum1(self, state, stop):
        if stop <= 0:
            return np.zeros(self.n + 1)

        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        second_part = np.array([0] * self.n + [((self.l * np.cos(ans[0:stop]) * ders[0:stop] * ders[0:stop]).sum())])
        first_part = np.concatenate((self.l * np.sin(ans[0:stop]), np.array([0] * (self.n - stop + 1))))
        return (-1)*(first_part + second_part)

    def derSum2(self, state, stop):
        if stop <= 0:
            return np.zeros(self.n + 1)

        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        second_part = np.array([0] * self.n + [(-1)*((self.l * np.sin(ans[0:stop]) * ders[0:stop] * ders[0:stop]).sum())])
        first_part = np.concatenate((self.l * np.cos(ans[0:stop]), np.array([0] * (self.n - stop + 1))))
        return first_part + second_part

    def d_dt_dTj_dphik(self, state, j, k):
        """
        Counting of ders by time in special format
        :return: np.ndarray of koef phi_k_2der
        """
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        derSum1 = self.derSum1(state, j)
        derSum2 = self.derSum2(state, j)
        sum1 = self.sum1(state, j)
        sum2 = self.sum2(state, j)
        sqrt = self.sqrt(state, j)

        if sum1[self.n] == 0 and sum2[self.n] == 0:
            if k == j:
                return np.array([0]*j + [(self.l**2) / 3] + [0]*(self.n - j))
            if k != j:
                return np.zeros(self.n + 1)
        else:
            assert j != 0
            if k < j:
                # -------------------------------------------first line-------------------------------#
                first_part = derSum1 * (-self.l * np.sin(ans[k])) + (-self.l * np.cos(ans[k]) * ders[k]) * sum1 + \
                             derSum2 * (self.l * np.cos(ans[k])) + (-self.l * np.sin(ans[k]) * ders[k]) * sum2

                second_part = ((sum1[self.n]) * (-self.l * np.sin(ans[k])) + (sum2[self.n]) * (
                            self.l * np.cos(ans[k]))) * (np.array(
                    [0] * j + [np.cos(ans[j] - ans[j - 1])] + [0] * (self.n - j)) + np.concatenate((np.zeros(self.n),
                                            np.array([ders[j] * (-np.sin(ans[j] -ans[j - 1]) * (ders[j] -ders[j - 1]))])))) / sqrt

                second_part = self.l * second_part / 2
                first_line = first_part + second_part
                # ----------------------------------------------------------------------------#

                koef = (np.cos(ans[j] - ans[j - 1]) * ders[j]) / (sqrt**2)
                fig_skobka = derSum1 * (-self.l * np.sin(ans[k])) + (-self.l * np.cos(ans[k]) * ders[k]) * sum1 + \
                             derSum2 * (self.l * np.cos(ans[k])) + (-self.l * np.sin(ans[k]) * ders[k]) * sum2  # as a first part in first line

                fig_skobka = fig_skobka * sqrt

                next_part = (sum1[self.n] * (-self.l * np.sin(ans[k])) + sum2[self.n] * (self.l * np.cos(ans[k])))

                next_part = ((sum1[self.n] * derSum1 + sum2[self.n] * derSum2) / sqrt) * next_part

                second_line = koef * (fig_skobka - next_part) * (self.l / 2)

                return first_line + second_line
        if k > j:
            return np.zeros(self.n + 1)

        if k == j:
            return np.array([0] * j + [(self.l ** 2) / 3] + [0] * (self.n - j)) + (self.l / 2) * (
                        ((sum1[self.n] * derSum1 + sum2[self.n] * derSum2) / (sqrt)) * np.cos(
                    ans[j] - ans[j - 1]) + np.array([0] * self.n + [sqrt * (-np.sin(ans[j] - ans[j - 1]) * (ders[j] - ders[j - 1]))]))

    def dTj_dphik(self, state, j, k):
        ans = state[0:self.n]
        ders = state[self.n:2 * self.n]
        sum1 = self.sum1(state, j)
        sum2 = self.sum2(state, j)
        sqrt = self.sqrt(state, j)

        if sum1[self.n] == 0 and sum2[self.n] == 0:
            return np.zeros(self.n + 1)

        assert j != 0

        if k < j - 1:
            first_part = ((-1)*self.l * np.cos(ans[k]) * ders[k]) * sum1 + ((-1)*self.l * np.sin(ans[k]) * ders[k]) * sum2
            second_part = ((self.l / 2) * ders[j] * np.cos(ans[j] - ans[j - 1]) * first_part) / sqrt

            return first_part + second_part

        if k == j - 1:
            first_part = ((-1)*self.l * np.cos(ans[k]) * ders[k]) * sum1 + ((-1)*self.l * np.sin(ans[k]) * ders[k]) * sum2
            second_part = ((self.l / 2) * ders[j] * np.cos(ans[j] - ans[j - 1]) * first_part) / sqrt
            third_part = np.array([0] * self.n + [(self.l / 2) * ders[j] * sqrt * (np.sin(ans[j] - ans[j - 1]))])
            return first_part + second_part + third_part

        if k == j:
            first_part = np.array([0] * self.n + [(-1)*(self.l / 2) * ders[j] * sqrt * (np.sin(ans[j] - ans[j - 1]))])
            return first_part
        if k > j:
            return np.zeros(self.n + 1)

    def dPi_dphik(self, state, j, k):
        ans = state[0:self.n]

        if k < j:
            return np.array([0] * self.n + [self.l * np.sin(ans[k]) * self.g])
        if k == j:
            return np.array([0] * self.n + [(self.l * np.sin(ans[k]) * self.g) / 2])
        if k > j:
            return np.zeros(self.n + 1)

    def count_d_dt_dT_dphik(self, state, k):
        a = np.array([0] * (self.n + 1), dtype=np.float64)
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

    def psi(self, state):
        a = []
        for k in range(self.n):
            a_ = self.get_k_matrix_line(state, k)
            a.append(a_)
        a = np.array(a)
        b = -a[:, self.n]
        a = a[:, 0:self.n]
        return np.linalg.solve(a, b)


if __name__ == "__main__":
    a = TwoStickPendulum(10)
    b = NStickPendulum(10, 3, 1, 1)
    # fi = a.solve(np.array([3.14, 0, 0, 0]), 0.0001, 10)[:, 0:2]
    # fig, ax = plt.subplots(ncols=2)
    # ax[0].plot(np.arange(0, 10+0.0001, 0.0001), fi[:,0])
    # ax[1].plot(np.arange(0, 10+0.0001, 0.0001), fi[:,1])
    # ax[1].grid(True)
    # ax[0].grid(True)
    print(b.psi(np.array([0.3, -1, 2, 2, 6, 5])))
    # plt.show()
