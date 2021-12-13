import pygame
import graphics
import math_pend
import random
import numpy as np

pygame.init()

surf = pygame.Surface((1200, 800))

menu = graphics.Menu(surf)
anim = graphics.Animation(surf)
N, l, angles0 = menu.run()
if N != 0:
    a = math_pend.NStickPendulum(N, 10, l, 1)
else:
    a = math_pend.TwoStickPendulum(10)
angles = a.solve(list(angles0) + [3]*N, 0.01, 50)[:, 0:N]

# dt = np.array([random.uniform(-0.01, 0.01) for i in range(int(N))])
# dt = np.array([0.01, -0.02, 0.03, -0.02, 0.04, -0.02, 0.05, -0.02, 0.06, -0.02])
# angles = np.array(angles0)
# for i in range(10000):
#     angles = np.vstack([angles, angles0 + i * dt])

anim.run(angles)
pygame.quit()
