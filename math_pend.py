import matplotlib.pyplot as plt
import numpy as np
import integrators as it


class MathPEndulum:
    def __init__(self, omega):
        self.omega = omega

    def func(self, state, time):
        psi = -self.omega * np.sin(state[0])
        xi = state[1]
        return np.array([xi, psi])

    def solve(self, in_state, time_step, full_time):
        n_iters = int(full_time/time_step)
        return it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)


class TwoStickPendulum:
    def __init__(self, omega):
        self.omega = omega
        pass

    def func(self, state, time):
        psi = self.psi(state, time)
        xi = state[2:4]
        return np.concatenate((xi, psi))

    def solve(self, in_state, time_step, full_time):
        n_iters = int(full_time/time_step)
        return it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)

    def psi1(self, state, time):
        fi2_2 = 0
        return -(3/8)*fi2_2*np.cos(state[1] - state[0]) + (3/8)*state[3]*(state[3] - state[2])*np.sin(state[1] - state[0]) + (3/8)*state[3]*state[2]*np.sin(state[1] - state[0]) - (9/8)*np.sin(state[0])*10  # g/l

    def psi2(self, state, time):
        fi1_2 = 0
        return -(3/2) * (fi1_2*np.cos(state[1] - state[0]) - state[2]*(state[3] - state[2])*np.sin(state[1] - state[0])) - (3/2)*state[3]*state[2]*np.sin(state[1] - state[0]) - (3/2)*np.sin(state[1])*10  # g/l

    def psi(self, state, time):
        """
        System solution
        :param state:
        :param time:
        :return:
        """
        A = np.array([[1, (3/8)*np.cos(state[1] - state[0])],
                      [1, (3/2)*np.cos(state[1] - state[0])]])

        b1 = (3/8)*state[3]*(state[3] - state[2])*np.sin(state[1] - state[0]) + (3/8)*state[3]*state[2]*np.sin(state[1] - state[0]) - (9/8)*np.sin(state[0])*self.omega # g/l
        b2 = (3/2)*state[2]*(state[3] - state[2])*np.sin(state[1] - state[0]) - (3/2)*state[3]*state[2]*np.sin(state[1] - state[0]) - (3/2)*np.sin(state[1])*self.omega  # g/l
        b = np.array([b1, b2])
        x = np.linalg.solve(A, b)
        # print(A@x - b)
        return x


class NStickPendulum:
    def __init__(self, omega, n):
        self.omega = omega
        self.n = n

    def func(self, state, time):
        psi = -self.omega * np.sin(state[0:self.n])
        xi = state[self.n:2*self.n]
        return np.concatenate((xi, psi))

    def solve(self, in_state, time_step, full_time):
        n_iters = int(full_time/time_step)
        return it.integrator_method(it.hune, self.func, in_state, 0, time_step, n_iters)


if __name__ == "__main__":
    a = TwoStickPendulum(10)
    fi = a.solve(np.array([1, 0, 0, 0]), 0.0001, 100)[:, 0:2]

    plt.plot(np.arange(0, 100+0.0001, 0.0001), fi[:,0])
    plt.plot(np.arange(0, 10+0.0001, 0.0001), fi[:,1])
    plt.grid(True)
    plt.show()
