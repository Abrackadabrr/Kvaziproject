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
    N, l, angles0 = menu.run()
    if menu.start:
        anim = graphics.Animation(surf)
        time_step = 0.005
        full_time = 10

        pendulum = NpendulumN.NStickPendulum(N, 10)
        angles = pendulum.solve(list(angles0) + [0]*N, time_step, full_time)
        # plots.save("5_20_0_0002", angles)
        print('End of calcs')
        energy = list(map(pendulum.count_energy, angles))

        # ---anaulys--- #
        plots.plot_energy(energy, full_time)
        plots.plot_angles(angles, 0, N-1, full_time)
        plots.plot_phase_space(angles, 0, N-1)
    # ---------- #
        anim.run(angles[:, 0:N], l)
    pygame.quit()


pygame.init()

surf = pygame.Surface((1200, 800))

menu = graphics.Menu(surf)
anim = graphics.Animation(surf)
N, ls0, angles0, n = fourier.data()
angles0 += 1.57
print(ls0)
ls0 *= ls0 * 10 / max(ls0)
sequence = [0]
for i in range(n):
    sequence += [i + 1, - i - 1]

dt0 = np.array(sequence) / 200
ls1 = []
angles1 = []
for i in range(2 * n + 1):
    ls1.append(ls0[sequence[i] + n])
    angles1.append(angles0[sequence[i] + n])

angles = np.array(angles1)
for i in range(3000):
    angles = np.vstack([angles, angles1 + i * dt0])
    
anim.run(angles, ls1)
pygame.quit()


# run()
