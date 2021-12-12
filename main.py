import pygame
import graphics
import math_pend
import numpy as np

pygame.init()
a = math_pend.TwoStickPendulum(10)
fi = a.solve(np.array([0, 0, 0, 0]), 0.002, 10)[:, 0:2]
print(fi)
screen = pygame.display.set_mode((1200, 800))
anim = graphics.Animation(screen)
anim.run(fi)
pygame.quit()
