import pygame
import graphics
import math_pend
import random
import numpy as np

pygame.init()
# a = math_pend.TwoStickPendulum(10)
# fi = a.solve(np.array([234, 0, 0, 0]), 0.002, 10)[:, 0:2]

surf = pygame.Surface((1200, 800))

menu = graphics.Menu(surf)
anim = graphics.Animation(surf)
N, l, angles0 = menu.run()
# dt = np.array([random.uniform(-0.01, 0.01) for i in range(int(N))])
dt = np.array([0.01, -0.02, 0.03, -0.02, 0.04, -0.02, 0.05, -0.02, 0.06, -0.02])
angles = np.array(angles0)
for i in range(10000):
    angles = np.vstack([angles, angles0 + i * dt])

anim.run(angles)
pygame.quit()
