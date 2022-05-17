import pygame
from src.client.canvas import Canvas
from src.client.game import Game
from src.client.network import Network

class Menu:

    def __init__(self):
        self.canvas = Canvas()
        self.screen = self.canvas.screen
        self.canvas.running = True
        self.main_menu()

    def new_screen_entry(self):
        self.canvas.click = False
        self.canvas.running = True
        self.canvas.draw_background()

    def main_menu(self):
        """Creates the main menu
        In:
            self
        Out:
            None
        """
        self.canvas = Canvas(name="Bombit menu")
        self.new_screen_entry()
        buttonList = [["Play", self.waiting_for_players_screen],
                      ["Settings", self.settings_screen],
                      ["Instructions", self.instructions_screen],
                      ["Quit game", self.quit_game]]
        while True:
            self.canvas.update_game_state(esq_shut_down=True)
            self.canvas.draw_background()
            self.canvas.draw_text("Main menu", self.canvas.black_color, int(self.canvas.width / 2),
                                  self.canvas.title_spacing_y)
            for x in range(len(buttonList)):
                self.canvas.create_button(buttonList[x][0], buttonList[x][1],
                                          int((self.canvas.width - self.canvas.button_width) / 2),
                                          self.canvas.button_spacing_y * (x + 2))

    def waiting_for_players_screen(self):
        """Shows the instructions for how to play the game
        In:
            self
        Out:
            None
        """

        self.new_screen_entry()
        while self.canvas.running:
            self.canvas.draw_background()
            self.canvas.draw_text("Waiting for other players", self.canvas.black_color, int(self.canvas.width / 2),
                                  self.canvas.title_spacing_y)

            self.canvas.create_button("Back", 0, int((self.canvas.width - self.canvas.button_width) / 2),
                                      self.canvas.height - self.canvas.button_height * 3)
            self.canvas.update_game_state()

    def settings_screen(self):
        """Shows the instructions for how to play the game
        In:
            self
        Out:
            None
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
        In:
            self
        Out:
            None
        """

        self.new_screen_entry()
        while self.canvas.running:
            self.canvas.draw_background()
            self.canvas.draw_text("Instructions", self.canvas.black_color, self.canvas.title_spacing_x,
                                  self.canvas.title_spacing_y)

            wordList = ["Instructions for the game"]

            for x in range(len(wordList)):
                self.canvas.draw_text(wordList[x], self.canvas.black_color, int(self.canvas.width / 2),
                                      int(self.canvas.button_spacing_y + self.canvas.title_spacing_y * x))

            self.canvas.create_button("Back", 0, int((self.canvas.width - self.canvas.button_width) / 2),
                                      self.canvas.height - self.canvas.button_height * 3)
            self.canvas.update_game_state()

    def quit_game(self):
        """Screen where you can enter your in grey boxes, can only proceed if valid name is input
        In:
            self,
            numberOfPlayers - The amount of players in the game
        Out:
            None
        """

        pygame.quit()
