import pygame
import os
import numpy as np
from abc import abstractmethod

FPS = 150

YELLOW = (255, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)


class Window:
    """
    abstract class for all program's windows
    """

    # @abstractmethod
    # def run(self):
    #     """
    #     abstract method, uses for runtime functions
    #     :return: smth useful
    #     """
    #     pass

    @staticmethod
    def create_text(text, color, position, size, screen, background=BLACK):
        """
            abstract method, create text on screen
            :return: text
        """
        f1 = pygame.font.Font(None, size)
        text1 = f1.render(text, True,
                          color, background)
        screen.blit(text1, position)


class Menu(Window):
    """
    class of first window of program, where init all parameters
    """

    def __init__(self, screen):
        """
        init function
        :param screen: surface
        """
        self.buttons = []
        self.screen = screen
        self.text1 = Text("NPendulumN", YELLOW, (430, 12), 80, self.screen)
        self.texts = [self.text1]

    def draw_objects(self):
        """Draws all objects in the window"""
        for text in self.texts:
            text.draw()

    def run(self):
        """
        Returns parameters as an np.array([x, y, z, vx, vy, vz, time, step,
         x-axis, y-axis, air_force, sun_force, integrator, is_finished)
         axis: 0 -- x, 1 -- y, 2 -- z, 3 -- vx, 4 -- vy, 5 -- vz, 6 -- time
         forces: bool variables
         integrator: 0 -- Euler, 1 -- RK4, 2 -- Dormand-Prince
         is_finished: True if stop, False if go next
        :return:
        """
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

            self.draw_objects()
            pygame.display.update()
            self.screen.fill(BLACK)


class Text:
    """
    class for working with text fields
    """

    def __init__(self, text, color, position, size, screen, background=BLACK):
        """
        init function
        :param text: text
        :param color: color
        :param position: text position
        :param size: field size
        :param screen: surface
        :param background: background
        """
        self.text = text
        self.base_color = color
        self.current_color = color
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.screen = screen
        self.background = background
        self.is_active = True
        self.f1 = pygame.font.Font(None, self.size)
        self.text1 = self.f1.render(self.text, True, self.current_color, self.background)

    def draw(self):
        """
        draw text on screen
        :return:
        """
        self.screen.blit(self.text1, (self.x, self.y))

    def set_text(self, text):
        """
        set text
        :param text: text
        :return:
        """
        self.text = text


class InsertField:
    """
    class for inserting
    """

    def __init__(self, value, x, y, width, height, screen):
        """
        init function
        :param value: value
        :param x: x position on screen
        :param y: y position on screen
        :param width: width
        :param height: height
        :param screen: surface
        """
        self.is_active = False
        self.value = str(value)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.text = Text(self.value, BLACK, (self.x + 7, self.y + 7), 40, self.screen, WHITE)

    def draw(self):
        """
        drawing text on screen
        :return:
        """
        pygame.draw.rect(self.screen, WHITE, (self.x, self.y, self.width, self.height))
        self.text.draw()

    def insert(self, char):
        """
        set text in field
        :param char: symbol
        :return:
        """
        if self.is_active:
            self.value = self.value[:-1]
            self.value += str(char)
            self.value += "|"
            self.text.set_text(self.value)

    def activate(self):
        """
        activate field
        :return:
        """
        if not self.is_active:
            self.is_active = True
            self.value += "|"
            self.text.set_text(self.value)

    def deactivate(self):
        """
        disactivate field
        :return:
        """
        if self.is_active:
            self.value = self.value[:-1]
            self.is_active = False
            self.text.set_text(self.value)

    def check_mouse(self):
        """
        check mouse position
        :return:
        """
        if self.x < pygame.mouse.get_pos()[0] < self.x + self.width and self.y < pygame.mouse.get_pos()[1] < self.y \
                + self.height:
            return True
        else:
            return False


class Button:
    """
    class for buttons
    """

    def __init__(self, x, y, w, h, text, screen, color=YELLOW):
        """
        init function
        :param x: x position
        :param y: y position
        :param w: width
        :param h: height
        :param text: text
        :param screen: surface
        :param color: color
        """
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.text = text
        self.w = w
        self.h = h
        self.is_active = False
        self.text_class = Text(self.text, BLACK, (self.x + (self.w - len(self.text) * 22) / 2, self.y + self.h * 0.2),
                               self.h, self.screen, self.color)

    def draw(self):
        """
        draw text on the screen
        :return:
        """
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))
        self.text_class.draw()

    def check_mouse(self):
        """
        check mouse position
        :return:
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.w and self.y < mouse_pos[1] < self.y + self.h:
            self.is_active = True
            self.color = (255, 235, 0)
            self.text_class = Text(self.text, BLACK,
                                   (self.x + (self.w - len(self.text) * 22) / 2, self.y + self.h * 0.2),
                                   self.h, self.screen, self.color)
            return True
        else:
            self.is_active = False
            self.color = YELLOW
            self.text_class = Text(self.text, BLACK,
                                   (self.x + (self.w - len(self.text) * 22) / 2, self.y + self.h * 0.2),
                                   self.h, self.screen, self.color)
            return False


class Animation(Window):

    def __init__(self, screen):
        self.objects = []
        self.screen = screen
        self.counter = 0

    def run(self, angles):
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

            self.draw_objects(angles[self.counter])
            pygame.display.update()
            print(self.counter)
            if self.counter > angles.shape[0] - 10:
                finished = True
            self.counter += 2
            self.screen.fill(BLACK)

    def draw_objects(self, angles):
        pos_s = self.data_transform(angles)
        for i in range(len(angles)):
            pygame.draw.line(self.screen, YELLOW, pos_s[i], pos_s[i+1], 5)
            pygame.draw.circle(self.screen, YELLOW, pos_s[i+1], 5)

    def data_transform(self, angles):
        length = 250
        data_cos = np.cos(angles.copy())
        data_sin = np.sin(angles.copy())
        y_s = np.cumsum(length * data_cos)
        x_s = np.cumsum(length * data_sin)
        return np.column_stack([np.insert(x_s, 0, 0) + 600, np.insert(y_s, 0, 0) + 200])


class Kernel:

    def __init__(self, x, y, angle, length=50):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length

    def draw(self, x, y, angle, screen):
        pygame.draw.aaline(screen, YELLOW, [self.x, self.y], [self.x + self.length * np.sin(self.angle),
                                                              self.y + self.length * np.cos(self.angle)])
