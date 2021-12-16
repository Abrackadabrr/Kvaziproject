import numpy as np
import matplotlib.pyplot as plt
import NpendulumN


def plots_energy(energy, n_iters, step):
    energy = np.array(energy)
    time = np.arange(0, n_iters*step, step)
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


if __name__ == '__main__':
    result = np.load('5_100.npy')
    pendulum = NpendulumN.NStickPendulum(3, 10)
    energy = np.array(list(map(pendulum.count_energy, result)))
    plots_energy(energy, len(energy), 0.01)
