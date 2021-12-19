import pygame
import graphics
import math_pend
import NpendulumN
import plots
import random
# import numpy as np


def run():
    pygame.init()
    surf = pygame.Surface((1200, 800))
    menu = graphics.Menu(surf)
    N, omega, kappa, l, angles0, full_time, time_step, first_angle, second_angle, is_saved, filename = menu.run()
    if menu.start:
        anim = graphics.Animation(surf)
        # N = 20
        # angles = np.load('rope_20_2.npy')
        # angles = angles[0:int(angles.shape[0] * (4 / 10)), :]
        # angles0 = [(np.pi/180)*30]*N
        pendulum = NpendulumN.NStickPendulum(N, omega, kappa)
        angles = pendulum.solve(list(angles0) + [0]*N, time_step, full_time)
        if is_saved:
            plots.save(str(filename), angles)
        print('End of calcs')
        energy = list(map(pendulum.count_energy, angles))

        anim.run(angles[:, 0:N], l, time_step)

        # ---anaulys--- #
        if kappa:
            plots.plot_energy_log(energy, full_time, time_step)
        else:
            plots.plot_energy(energy, full_time, time_step)
        plots.plot_angles(angles, first_angle - 1, second_angle - 1, full_time)
        plots.plot_phase_space(angles, first_angle - 1, second_angle - 1)
        # ---------- #
    pygame.quit()


run()
