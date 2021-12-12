import pygame
import numpy as np

FPS = 150

YELLOW = (255, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)

FIELD_WIDTH = 100
FIELD_HEIGHT = 35

col_x = 1000
way = pygame.Surface((1200, 800), pygame.SRCALPHA, 32)
sc = pygame.display.set_mode((1200, 800))
way = way.convert_alpha()

START_POS = (600, 400)


class Window:
    """
    abstract class for all program's windows
    """

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
        self.screen = screen

        self.start_button = Button(970, 700, 200, 70, "Start!", self.screen)

        self.text1 = Text("NPendulumN", YELLOW, (430, 12), 80, self.screen)
        self.text2 = Text("N: ", WHITE, (col_x - 50, 100), 50, self.screen)
        self.text3 = Text("l: ", WHITE, (col_x - 50, 150), 50, self.screen)
        self.texts = [self.text1, self.text2, self.text3]

        self.field_N = InsertField(5, col_x, 100, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_l = InsertField(60, col_x, 150, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle1 = InsertField(30, col_x, 200, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle2 = InsertField(0, col_x, 250, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle3 = InsertField(30, col_x, 300, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle4 = InsertField(0, col_x, 350, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle5 = InsertField(30, col_x, 400, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle6 = InsertField(0, col_x, 450, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle7 = InsertField(30, col_x, 500, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle8 = InsertField(0, col_x, 550, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle9 = InsertField(30, col_x, 600, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle10 = InsertField(30, col_x, 650, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.insert_fields = [self.field_N, self.field_l, self.field_angle1, self.field_angle2, self.field_angle3,
                              self.field_angle4, self.field_angle5, self.field_angle6,
                              self.field_angle7, self.field_angle8, self.field_angle9,
                              self.field_angle10]
        self.angles = [np.pi / 180 * button.get_value() for button in self.insert_fields[2:]]

    def draw_objects(self):
        """Draws all objects in the window"""
        for text in self.texts:
            text.draw()

        for f in self.insert_fields[:(int(self.field_N.get_value()) + 2)]:
            f.draw()

        self.angles = [np.pi / 180 * button.get_value() for button in self.insert_fields[2:]]
        pos_s = Animation.data_transform(self.angles, self.field_l.get_value())
        for i in range(min(int(self.field_N.get_value()), 10)):
            pygame.draw.line(self.screen, YELLOW, pos_s[i], pos_s[i + 1], 5)
            pygame.draw.circle(self.screen, YELLOW, pos_s[i + 1], 5)
        pygame.draw.circle(self.screen, YELLOW, pos_s[0], 5)
        self.start_button.draw()
        sc.blit(self.screen, (0, 0))

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for f in self.insert_fields:
                        if f.check_mouse():
                            f.activate()
                        else:
                            f.deactivate()

                    if self.start_button.check_mouse():
                        finished = True

                if event.type == pygame.KEYDOWN:
                    for f in self.insert_fields:
                        if event.key == 13:
                            f.deactivate()
                        if event.key == pygame.K_BACKSPACE:
                            if f.is_active and f.value != "":
                                f.value = f.value[:-2]
                                f.value += "|"
                                f.text.set_text(f.value)
                        else:
                            if len(f.value) < 5:
                                f.insert(event.unicode)

            self.draw_objects()
            pygame.display.update()
            self.screen.fill(BLACK)

        n = int(self.field_N.get_value())
        return n, self.field_l.get_value(), np.array(self.angles[:n])


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

    def draw(self):
        """
        draw text on screen
        :return:
        """
        f1 = pygame.font.Font(None, self.size)
        text1 = f1.render(self.text, True,
                          self.current_color, self.background)
        self.screen.blit(text1, (self.x, self.y))

    def activate(self):
        """
        change active fields color
        :return:
        """
        if not self.is_active:
            self.is_active = True
            self.current_color = self.base_color

    def deactivate(self):
        """
        chnge deactive fields in grey color
        :return:
        """
        if self.is_active:
            self.is_active = False
            self.current_color = (100, 100, 100)

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

    def get_value(self):
        try:
            if self.is_active:
                return float(self.value[:-1])
            else:
                return float(self.value)
        except ValueError:
            return 0


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
            if self.counter > angles.shape[0] - 10:
                finished = True
            self.counter += 1
            self.screen.fill(BLACK)

    def draw_objects(self, angles):
        pos_s = self.data_transform(angles)
        for i in range(len(angles)):
            pygame.draw.line(self.screen, YELLOW, pos_s[i], pos_s[i+1], 5)
            pygame.draw.circle(self.screen, YELLOW, pos_s[i+1], 5)

        pygame.draw.circle(self.screen, YELLOW, pos_s[0], 5)
        pygame.draw.circle(way, RED, pos_s[-1], 1)
        sc.blit(self.screen, (0, 0))
        sc.blit(way, (0, 0))

    @staticmethod
    def data_transform(angles, length=50):
        data_cos = np.cos(angles.copy())
        data_sin = np.sin(angles.copy())
        y_s = np.cumsum(length * data_cos)
        x_s = np.cumsum(length * data_sin)
        return np.column_stack([np.insert(x_s, 0, 0) + START_POS[0], np.insert(y_s, 0, 0) + START_POS[1]])
