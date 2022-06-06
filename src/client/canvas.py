import pygame

from pygame.locals import *


class Canvas:
    """
    Class for handling many pygame display related things.
    Like drawing buttons and text on the display.
    """

    def __init__(self, w=800, h=800, name="Bombit Menu"):
        """
        Init for the Canvas class
        :param w: display-width
        :param h: display height
        :param name: the name that is displayed in top-left corner
        """
        self.width = w
        self.height = h

        # Spacings
        self.button_width = 200
        self.button_height = 50
        self.title_spacing_y = 20
        self.title_spacing_x = 50
        self.button_spacing_y = 100
        self.button_spacing_x = 50

        self.screen = pygame.display.set_mode((w, h))
        self.mx, self.my = pygame.mouse.get_pos()
        self.click = False
        self.running = True
        self.main_clock = pygame.time.Clock()
        self.refresh_rate = 60

        # Colors
        self.grey_color = (160, 160, 160)
        self.white_color = (255, 255, 255)
        self.black_color = (0, 0, 0)

        pygame.init()
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        """
        Updates the display with all the newly added display stuff
        :return:
        """
        pygame.display.update()

    def draw_text(self, text, color, x, y, center=True):
        """Draws text on screen
        :param text: The text to be written on the screen
        :param color: What color the text should have
        :param x: The position in x-direction
        :param y: The position i y-direction
        :param center: Ff True then x,y = center of text, else x,y = upper left corner
        :return:
        """
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", 20)
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        if center:
            text_rect.center = (int(x), int(y))
        else:
            text_rect.midleft = (int(x), int(y))
        self.screen.blit(text_obj, text_rect)

    def draw_background(self):
        """
        Paints the whole screen in white
        :return:
        """
        self.screen.fill(self.white_color)

    def create_button(self, buttonName, function, x, y, enabled=True):
        """Creates clickable buttons if criteria is met
        :param buttonName: Text on the button
        :param function: THe function the button should call upon when pressed
        :param x: coordinates for buttons upper left corner (in x - direction)
        :param y: coordinates for buttons upper left corner (in y - direction)
        :param enabled: Only proceeds to call function if True
        :return:
        """
        button_width = 200
        button_height = 50
        text_color = self.black_color
        button = pygame.Rect(x, y, button_width, button_height)
        if enabled:
            if button.collidepoint(self.mx, self.my):
                if self.click:
                    if function == 0:
                        self.running = False
                    else:
                        function()

        else:
            text_color = (255, 0, 0)  # Red color (if enabled = False)
        pygame.draw.rect(self.screen, self.grey_color, button)
        self.draw_text(buttonName, text_color, int(x + button_width / 2), int(y + button_height / 2))



    def update_game_state(self, esc_shut_down = False):
        """Updates the game, handles all input from mouse and keyboard if valid
        :param esc_shut_down - Only True on main menu, handles if escape-key should shut down the game or just make you go back to the menu
        :return:
        """
        self.click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if esc_shut_down:  # Only True on main menu (so far)
                        pygame.quit()
                    else:
                        self.running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

        self.mx, self.my = pygame.mouse.get_pos()
        pygame.display.update()
        self.main_clock.tick(self.refresh_rate)
