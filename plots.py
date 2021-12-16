import numpy as np
import matplotlib.pyplot as plt
import NpendulumN


def plot_energy(energy, full_time):
    energy = np.array(energy)
    time = np.linspace(0, full_time, energy.size)
    rel_er = np.abs(energy/energy[0] - 1)
    convolve_param = 10000
    slide_average_er1 = np.convolve(rel_er, np.ones(convolve_param)/convolve_param)[convolve_param//2:-convolve_param+1]
    fig, ax = plt.subplots(ncols=2)
    fig.suptitle("Анализ энергии системы")
    ax[0].plot(time, energy)
    ax[0].grid()
    ax[0].set_xlabel("Время расчета")
    ax[0].set_ylabel("Полная энергия системы")
    ax[1].plot(time, rel_er, color='green', label='относительная\nошибка')
    ax[1].plot(time[:-convolve_param//2], slide_average_er1, color='red', label=f'скользящее\nсреднее {convolve_param}')
    ax[1].plot(time, np.zeros(time.size))
    ax[1].grid()
    ax[1].set_xlabel("Время расчета")
    ax[1].set_ylabel("Относительная ошибка")
    ax[1].legend()

    plt.show()


def save(name, res):
    np.save(name, res)


def plot_angles(res, k, j, full_time):
    fig, ax = plt.subplots(ncols=2)
    fig.suptitle("Зависимость углов от времени")
    k_ = res[:,k]
    j_ = res[:,j]
    time = np.linspace(0, full_time, k_.size)
    ax[0].set_title(f'{k}-й угол')
    ax[1].set_title(f'{j}-й угол')
    ax[0].plot(time, k_)
    ax[0].grid()
    ax[0].set_xlabel("Время расчета")
    ax[0].set_ylabel("Угол")
    ax[1].plot(time, j_)
    ax[1].grid()
    ax[1].set_xlabel("Время расчета")
    ax[1].set_ylabel("Угол")

    plt.show()


def plot_phase_space(res, k, j):
    fig, ax = plt.subplots(ncols=2)
    fig.suptitle("Фазовые плоскости углов")
    k_ = res[:, k]
    k_der = res[:,(res[1].size//2)+k]
    j_ = res[:, j]
    j_der = res[:,(res[1].size//2)+j]

    ax[0].set_title(f'{k}-й угол')
    ax[1].set_title(f'{j}-й угол')
    ax[0].plot(k_, k_der)
    ax[0].grid()
    ax[0].set_xlabel("Угол")
    ax[0].set_ylabel("Производная")
    ax[1].plot(j_, j_der)
    ax[1].grid()
    ax[1].set_xlabel("Угол")
    ax[1].set_ylabel("Производная")

    plt.show()


if __name__ == '__main__':
    result = np.load('5_100.npy')
    pendulum = NpendulumN.NStickPendulum(3, 10)
    energy = np.array(list(map(pendulum.count_energy, result)))
    plots_energy(energy, 0.01)
