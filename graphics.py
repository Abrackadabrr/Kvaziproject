import pygame
import numpy as np

FPS = 60

YELLOW = (255, 180, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)

FIELD_WIDTH = 120
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
        self.text3 = Text("length: ", WHITE, (col_x - 135, 150), 50, self.screen)
        self.text4 = Text("angles: ", WHITE, (col_x - 140, 200), 50, self.screen)

        self.text5 = Text("full time: ", WHITE, (60, 100), 50, self.screen)
        self.text6 = Text("time step: ", WHITE, (40, 150), 50, self.screen)
        self.text7 = Text("For analys: ", WHITE, (40, 300), 50, self.screen)
        self.text8 = Text("fst angle: ", WHITE, (60, 350), 50, self.screen)
        self.text9 = Text("snd angle: ", WHITE, (40, 400), 50, self.screen)
        self.text10 = Text(f"Pendulum", WHITE, (40, 500), 50, self.screen)
        self.text11 = Text(f"parameter: ", WHITE, (40, 550), 50, self.screen)
        self.text12 = Text(f"Windage: ", WHITE, (40, 650), 50, self.screen)
        self.text13 = Text(f"Save: ", WHITE, (col_x - 110, 500), 50, self.screen)
        self.text14 = Text(f"Filename: ", WHITE, (col_x - 110, 550), 50, self.screen)

        self.texts = [self.text1, self.text2, self.text3, self.text4, self.text5,
                      self.text6, self.text7, self.text8, self.text9, self.text10,
                      self.text11, self.text12, self.text13, self.text14]

        self.field_N = InsertField(1, col_x, 100, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_l = InsertField(60, col_x, 150, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle1 = InsertField(0, col_x, 200, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle2 = InsertField(30, col_x, 250, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle3 = InsertField(60, col_x, 300, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle4 = InsertField(90, col_x, 350, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle5 = InsertField(120, col_x, 400, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle6 = InsertField(150, col_x, 450, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle7 = InsertField(180, col_x, 500, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle8 = InsertField(210, col_x, 550, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle9 = InsertField(240, col_x, 600, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_angle10 = InsertField(270, col_x, 650, FIELD_WIDTH, FIELD_HEIGHT, self.screen)

        self.field_full_time = InsertField(10, 220, 100, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_time_step = InsertField(0.01, 220, 150, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_first_angle = InsertField(1, 235, 350, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_second_angle = InsertField(1, 235, 400, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_pend_param = InsertField(10, 235, 550, FIELD_WIDTH, FIELD_HEIGHT, self.screen)
        self.field_windage = InsertField(0.1, 235, 650, FIELD_WIDTH, FIELD_HEIGHT, self.screen)

        self.field_filename = InsertField(0.1, col_x, 600, FIELD_WIDTH, FIELD_HEIGHT, self.screen)

        self.click_save = ClickField(col_x, 500, self.screen)

        self.insert_fields = [self.field_N, self.field_l, self.field_time_step, self.field_full_time,
                              self.field_first_angle, self.field_second_angle, self.field_pend_param,
                              self.field_windage, self.field_filename,
                              self.field_angle1, self.field_angle2, self.field_angle3,
                              self.field_angle4, self.field_angle5, self.field_angle6,
                              self.field_angle7, self.field_angle8, self.field_angle9,
                              self.field_angle10]

        self.angles = [np.pi / 180 * button.get_value() for button in self.insert_fields[9:]]  # тут было 2 - поменял на 6

        self.start = False

    def draw_objects(self):
        """Draws all objects in the window"""
        for text in self.texts:
            text.draw()

        for f in self.insert_fields[:(int(self.field_N.get_value()) + 9)]:  # тут было 2 - поменял на 6
            f.draw()

        self.angles = [np.pi / 180 * button.get_value() for button in self.insert_fields[9:]]  # тут было 2 - поменял на 6
        self.click_save.draw()
        pos_s = Animation.data_transform(self.angles, self.field_l.get_value())
        for i in range(min(int(self.field_N.get_value()), 10)):
            pygame.draw.line(self.screen, YELLOW, pos_s[i], pos_s[i + 1], 5)
            pygame.draw.circle(self.screen, YELLOW, pos_s[i + 1], 5)
        pygame.draw.circle(self.screen, YELLOW, pos_s[0], 5)
        self.start_button.draw()
        sc.blit(self.screen, (0, 0))

    def run(self):
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            clock.tick(FPS)

            first_angle = self.field_first_angle.get_value()
            second_angle = self.field_second_angle.get_value()
            N = self.field_N.get_value()

            all_right = True
            if first_angle > N or first_angle < 1:
                self.field_first_angle.set_text_color('red')
            else:
                self.field_first_angle.set_text_color('black')
        
            if second_angle > N or second_angle < 1:
                self.field_second_angle.set_text_color('red')
            else:
                self.field_second_angle.set_text_color('black')
            try:
                int(second_angle)
            except ...:
                self.field_second_angle.set_text_color('red')
            try:
                int(first_angle)
            except ...:
                self.field_first_angle.set_text_color('red')

            try:
                if 0 < int(second_angle) <= N and 0 < int(first_angle) <= N:
                    all_right = True
                else:
                    all_right = False
            except ...:
                all_right = False
            if not all_right:
                self.start_button.set_active(False)
            else:
                self.start_button.set_active(True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for f in self.insert_fields:
                        if f.check_mouse():
                            f.activate()
                        else:
                            f.deactivate()

                    if self.start_button.check_mouse() and all_right:
                        self.start = True
                        finished = True

                    self.click_save.check_mouse()

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
                            if len(f.value) < 7:
                                f.insert(event.unicode)

            self.draw_objects()
            pygame.display.update()
            self.screen.fill(BLACK)

        n = int(self.field_N.get_value())
        return n, self.field_pend_param.get_value(), self.field_windage.get_value(),\
                  self.field_l.get_value(), np.array(self.angles[:n]), \
                  self.field_full_time.get_value(), self.field_time_step.get_value(), \
                  int(self.field_first_angle.get_value()), int(self.field_second_angle.get_value()), \
                  self.click_save.get_value(), self.field_filename.get_value()


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

    def set_current_color(self, color):
        self.current_color = color

    def set_back_color(self, color):
        self.background = color

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

    def set_text_color(self, color):
        self.text.set_current_color(color)


class ClickField:
    def __init__(self, x, y, screen):
        """
        init function
        :param x: x position
        :param y: y position
        :param screen: surface
        """
        self.r = 14
        self.x = x + self.r
        self.y = y + 1.2 * self.r
        self.screen = screen
        self.is_active = False

    def draw(self):
        pygame.draw.circle(self.screen, WHITE, (self.x, self.y), self.r)
        if self.is_active:
            pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r / 2)

    def change(self):
        self.is_active = not self.is_active

    def check_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if np.sqrt((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) < self.r:
            self.change()

    def get_value(self):
        return self.is_active


class Button:
    """
    class for buttons
    """

    def __init__(self, x, y, w, h, text, screen, color=YELLOW, text_size=0):
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
        if not text_size:
            self.size = h
        else:
            self.size = text_size
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.text = text
        self.w = w
        self.h = h
        self.is_active = False
        self.text_class = Text(self.text, BLACK, (self.x + (self.w - len(self.text) * 22) / 2, self.y + self.h * 0.2),
                               self.size, self.screen, self.color)

    def set_active(self, boolean):
        self.is_active = boolean
        if not self.is_active:
            self.color = GREY
            self.text_class.set_back_color(GREY)
        else:
            self.color = YELLOW
            self.text_class.set_back_color(YELLOW)

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
        if not self.is_active:
            return False
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.w and self.y < mouse_pos[1] < self.y + self.h:
            self.color = (255, 255, 0)
            self.text_class = Text(self.text, BLACK,
                                   (self.x + (self.w - len(self.text) * 22) / 2, self.y + self.h * 0.2),
                                   self.h, self.screen, self.color)
            return True
        else:
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
        self.start_button = Button(400, 700, 200, 70, "Start", self.screen)
        self.skip_button = Button(630, 700, 200, 70, "Skip ", self.screen)
        self.return_button = Button(500, 700, 200, 70, "To menu", self.screen)
        self.start_button.set_active(True)
        self.skip_button.set_active(True)

    def pre_run(self, angles, length):
        clock = pygame.time.Clock()
        finished = False
        while not finished:

            clock.tick(FPS)
            self.screen.fill(BLACK)

            self.start_button.draw()
            self.skip_button.draw()
            self.draw_objects(angles[0], length)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.check_mouse():
                        return True
                    if self.skip_button.check_mouse():
                        pygame.quit()
                        return False

            pygame.display.update()

    def run(self, angles, length, time_step):
        if not self.pre_run(angles, length):
            return False
        calc_fps = int(1 / time_step)
        counter_increment = calc_fps/FPS
        if counter_increment <= 0:
            counter_increment = 1

        finished = False
        clock = pygame.time.Clock()
        while not finished:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

            self.draw_objects(angles[int(np.floor(self.counter))], length)
            pygame.display.update()
            if self.counter > angles.shape[0] - 20:
                finished = True
            self.counter += counter_increment
            self.screen.fill(BLACK)
        return True

    def draw_objects(self, angles, length):
        pos_s = self.data_transform(angles, length)
        for i in range(len(angles)):
            pygame.draw.line(self.screen, YELLOW, pos_s[i], pos_s[i + 1], 5)
            pygame.draw.circle(self.screen, YELLOW, pos_s[i + 1], 5)

        pygame.draw.circle(self.screen, YELLOW, pos_s[0], 5)
        pygame.draw.circle(way, RED, pos_s[-1], 1)
        sc.blit(self.screen, (0, 0))
        sc.blit(way, (0, 0))

    @staticmethod
    def data_transform(angles, length):
        data_cos = np.cos(angles.copy())
        data_sin = np.sin(angles.copy())
        y_s = np.cumsum(length * data_cos)
        x_s = np.cumsum(length * data_sin)
        return np.column_stack([np.insert(x_s, 0, 0) + START_POS[0], np.insert(y_s, 0, 0) + START_POS[1]])
