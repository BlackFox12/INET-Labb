import pygame
import math
import os
from src.client.canvas import Canvas


class Game:
    """
    Game class. Mainly applies textures on the bombit game board.
    But also has two different screens, one for before the game starts,
    and one for when the game is over.
    """

    def __init__(self, w=800, h=800):
        self.width = w
        self.height = h
        self.board_size = 13
        self.background_size = math.ceil(self.width / self.board_size)

        self.canvas = Canvas(name="Bombit game")
        self.screen = self.canvas.screen
        self.canvas.running = True
        self.waiting = False


    def apply_textures(self, board):
        """
        Applies textures to the board, I.e 62*62 pixel images.
        :param board: The game board that represents the current state of the game
        :return:
        """
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == "#":
                    self.draw_background(x, y, "wall")

                elif board[y][x] == "":
                    self.draw_background(x, y, "ground")

                elif board[y][x] == "1":
                    self.draw_background(x, y, "ground")
                    self.draw_player(x, y, "player1")

                elif board[y][x] == "2":
                    self.draw_background(x, y, "ground")
                    self.draw_player(x, y, "player2")

                elif board[y][x] == "B":
                    self.draw_background(x, y, "ground")
                    self.draw_bomb(x, y)

                elif board[y][x] == "P":
                    self.draw_background(x, y, "ground")
                    self.draw_bonus_bomb(x, y)

                elif board[y][x] == "F":
                    self.draw_background(x, y, "ground")
                    self.draw_fire(x, y)


    def draw_background(self, x, y, texture_type):
        """
        Draws background objects, either wall or ground depending on texture_type
        :param x: Coordinates in X-direction for upper left corner of the image
        :param y: oordinates in Y-direction for upper left corner of the image
        :param texture_type: Should be either 'wall' or 'ground' depending on
                    what type of texture square contains.
        :return:
        """
        if texture_type == "wall":
            bomb_img = pygame.image.load(
                os.path.join(os.path.dirname(__file__), '..', '..', 'pictures', 'Wall.png'))
            self.screen.blit(bomb_img, (x * self.background_size, y * self.background_size))
        elif texture_type == "ground":
            bomb_img = pygame.image.load(
                os.path.join(os.path.dirname(__file__), '..', '..', 'pictures', 'Ground.png'))
            self.screen.blit(bomb_img, (x * self.background_size, y * self.background_size))

    def draw_player(self, x, y, player):
        if player == "player1":
            bomb_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', '..', 'pictures', 'red_dragon.png'))
            self.screen.blit(bomb_img, (x * self.background_size, y * self.background_size))
        elif player == "player2":
            bomb_img = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', '..', 'pictures', 'blue_dragon.png'))
            self.screen.blit(bomb_img, (x * self.background_size, y * self.background_size))

    def draw_bomb(self, x, y):
        bomb_img = pygame.image.load(os.path.join(os.path.dirname( __file__ ), '..', '..', 'pictures', 'tnt.png'))
        self.screen.blit(bomb_img, (x*self.background_size, y*self.background_size))

    def draw_bonus_bomb(self, x, y):
        bomb_img = pygame.image.load(os.path.join(os.path.dirname( __file__ ), '..', '..', 'pictures', 'bonusTnt.png'))
        self.screen.blit(bomb_img, (x * self.background_size, y * self.background_size))

    def draw_fire(self, x, y):
        bomb_img = pygame.image.load(os.path.join(os.path.dirname( __file__ ), '..', '..', 'pictures', 'fire.png'))
        self.screen.blit(bomb_img, (x * self.background_size, y * self.background_size))

    def waiting_for_players_screen(self):
        """Shows the instructions for how to play the game
        In:
            self
        Out:
            None
        """
        # TODO fix so that you can go back to menu
        self.canvas.click = False
        self.canvas.draw_background()
        self.waiting = True

        while self.canvas.running and self.waiting:
            self.canvas.draw_background()
            self.canvas.draw_text("Waiting for other players", self.canvas.black_color, int(self.canvas.width / 2),
                                  self.canvas.title_spacing_y)

            self.canvas.create_button("Back", 0, int((self.canvas.width - self.canvas.button_width) / 2),
                                      self.canvas.height - self.canvas.button_height * 3)
            self.canvas.update_game_state()


    def victory_screen(self, winning_id, client_id):
        self.canvas.click = False
        self.canvas.running = True
        self.canvas.draw_background()

        while self.canvas.running:
            self.canvas.draw_background()
            if winning_id == client_id:
                text = "Congratulations you won!"
            else:
                text = "You lost"
            self.canvas.draw_text(text, self.canvas.black_color, int(self.canvas.width / 2),
                                  self.canvas.title_spacing_y)

            self.canvas.create_button("Back", 0, int((self.canvas.width - self.canvas.button_width) / 2),
                                      self.canvas.height - self.canvas.button_height * 3)
            self.canvas.update_game_state()

