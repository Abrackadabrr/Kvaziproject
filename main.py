import pygame
import graphics
import math_pend
import NpendulumN
import plots
import random
import numpy as np


def runnn():
    pygame.init()
    surf = pygame.Surface((1200, 800))
    menu = graphics.Menu(surf)
    anim = graphics.Animation(surf)
    N, l, angles0 = menu.run()

    time_step = 0.005
    full_time = 10

    pendulum = NpendulumN.NStickPendulum(N, 10)
    angles = pendulum.solve(list(angles0) + [0]*N, time_step, full_time)
    # plots.save("5_20_0_0002", angles)
    print('End of calcs')
    energy = list(map(pendulum.count_energy, angles))

    #---anaulys---#
    plots.plot_energy(energy, full_time)
    plots.plot_angles(angles, 0, N-1, full_time)
    plots.plot_phase_space(angles, 0, N-1)
    #----------#
    anim.run(angles[:, 0:N])
    pygame.quit()


runnn()
