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
    pendulum = NpendulumN.NStickPendulum(N, 10)
    angles = pendulum.solve(list(angles0) + [0]*N, 0.0002, 20)
    # plots.save("5_20_0_0002", angles)
    # energy = list(map(pendulum.count_energy, angles))
    # plots.plots_energy(energy, len(energy), 0.01)
    anim.run(angles[:, 0:N])
    pygame.quit()
