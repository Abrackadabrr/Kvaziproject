import pygame
import graphics
import math_pend
import NpendulumN
import plots
import random
import numpy as np
import fourier


def run():
    pygame.init()
    surf = pygame.Surface((1200, 800))
    menu = graphics.Menu(surf)
    N, l, angles0, full_time, time_step, first_angle, second_angle = menu.run()
    if menu.start:
        anim = graphics.Animation(surf)
        # N = 20
        # angles = np.load('rope_20_2.npy')
        # angles = angles[0:int(angles.shape[0] * (4 / 10)), :]
        # angles0 = [(np.pi/180)*30]*N
        pendulum = NpendulumN.NStickPendulum(N, 10)
        angles = pendulum.solve(list(angles0) + [0]*N, time_step, full_time)
        # plots.save("rope_20_2", angles)
        print('End of calcs')
        energy = list(map(pendulum.count_energy, angles))

        anim.run(angles[:, 0:N], l, time_step)

        # ---anaulys--- #
        plots.plot_energy(energy, full_time, time_step)
        plots.plot_angles(angles, first_angle - 1, second_angle - 1, full_time)
        plots.plot_phase_space(angles, first_angle - 1, second_angle - 1)
        # ---------- #
    pygame.quit()


run()
