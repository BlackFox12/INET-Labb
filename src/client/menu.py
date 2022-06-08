import pygame

from src.client.canvas import Canvas
from src.client.client import Client


class Menu:
    """
    The Menu class is a menu for the game Bombit.
        It will draw buttons and text on a pygame window.
    """


    def __init__(self):
        """
        Init for the menu class, sets up the screen and calls the main_menu function
        """
        self.canvas = Canvas()
        self.screen = self.canvas.screen
        self.canvas.running = True
        self.main_menu()

    def new_screen_entry(self):
        """
        Should be called every time the menu goes from one screen to another.
        It resets some global variables and paints over the screen in white.
        :return:
        """
        self.canvas.click = False
        self.canvas.running = True
        self.canvas.draw_background()

    def main_menu(self):
        """
        The main menu, a hub of buttons that when clicked leads to other
            menu screens (or will start the game).
        :return:
        """
        self.canvas = Canvas(name="Bombit menu")
        self.new_screen_entry()
        buttonList = [["Play", self.start_game],
                      ["Settings", self.settings_screen],
                      ["Instructions", self.instructions_screen],
                      ["Quit game", pygame.quit]]
        while True:
            self.canvas.update_game_state(esc_shut_down=True)
            # esc_shut_down = True means that if the user presses 'Escape'
            # pygame.quit() will be called, meaning the window will close
            self.canvas.draw_background()
            self.canvas.draw_text("Main menu", self.canvas.black_color, int(self.canvas.width / 2),
                                  self.canvas.title_spacing_y)
            for x in range(len(buttonList)):
                self.canvas.create_button(buttonList[x][0], buttonList[x][1],
                                          int((self.canvas.width - self.canvas.button_width) / 2),
                                          self.canvas.button_spacing_y * (x + 2))

    def start_game(self):
        """ Starts the game
        :return:
        """
        #pygame.quit()
        Client()


    def settings_screen(self):
        """A screen for changing the game settings (Not really implemented)
        :return:
        """

        self.new_screen_entry()
        while self.canvas.running:
            self.canvas.draw_background()
            self.canvas.draw_text("Settings", self.canvas.black_color, self.canvas.title_spacing_x,
                                  self.canvas.title_spacing_y)

            wordList = ["Settings for the game"]

            for x in range(len(wordList)):
                self.canvas.draw_text(wordList[x], self.canvas.black_color, int(self.canvas.width / 2),
                                      int(self.canvas.button_spacing_y + self.canvas.title_spacing_y * x))

            self.canvas.create_button("Back", 0, int((self.canvas.width - self.canvas.button_width) / 2),
                                      self.canvas.height - self.canvas.button_height * 3)
            self.canvas.update_game_state()

    def instructions_screen(self):
        """Shows the instructions for how to play the game
        :return:
        """

        self.new_screen_entry()
        while self.canvas.running:
            self.canvas.draw_background()
            self.canvas.draw_text("Instructions", self.canvas.black_color, self.canvas.title_spacing_x,
                                  self.canvas.title_spacing_y)

            wordList = ["Instructions for the game", "Use Arrows to move", "Use Space to plant bomb",
                        "Kill opponent to win"]

            for x in range(len(wordList)):
                self.canvas.draw_text(wordList[x], self.canvas.black_color, int(self.canvas.width / 2),
                                      int(self.canvas.button_spacing_y + self.canvas.title_spacing_y * x))

            self.canvas.create_button("Back", 0, int((self.canvas.width - self.canvas.button_width) / 2),
                                      self.canvas.height - self.canvas.button_height * 3)
            self.canvas.update_game_state()


