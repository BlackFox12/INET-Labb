import pygame

from pygame.locals import *


class Canvas:

    def __init__(self, w=800, h=800, name="Bombit Menu"):
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
        pygame.display.update()

    def draw_text(self, text, color, x, y, center=True):
        """Draws text on screen
        In:
            self,
            text - The text to be written on the screen
            color - What color the text should have
            surface - What surface the text should be on (in this program always self.screen)
            x - the position in x-direction
            y - the position i y-direction
            center - if True then x,y = center of text, else x,y = upper left corner
        Out:
            None
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

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill(self.white_color)

    def create_button(self, buttonName, function, x, y, enabled=True):
        """Creates clickable buttons if criteria is met
        In:
            self,
            buttonName - Text on the button
            function - what function the button should call upon when pressed
            x - coordinates for button
            y - coordinates for button
            enabled - Only proceeds to call funtion if True
        Out:
            None
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
            text_color = (255, 0, 0)  # Red color (if name is invalid)
        pygame.draw.rect(self.screen, self.grey_color, button)
        self.draw_text(buttonName, text_color, int(x + button_width / 2), int(y + button_height / 2))



    def update_game_state(self, esq_shut_down = False):
        """Updates the game, handles all input from mouse and keyboard if valid
        In:
            self,
            shutDown - Only True on main menu, handles if escape-key should shut down the game or just make you go back to the menu
            text - Only True on the screen where you can change your name
        Out:
            None
        """

        self.click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if esq_shut_down:  # Only True on main menu (so far)
                        pygame.quit()
                    else:
                        self.running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

        self.mx, self.my = pygame.mouse.get_pos()
        pygame.display.update()
        self.main_clock.tick(self.refresh_rate)
