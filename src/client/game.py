import pygame
import math
import os
from src.client.canvas import Canvas


class Game:

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
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == "#":
                    self.draw_background(x, y, "wall")

                elif board[y][x] == "":
                    self.draw_background(x, y, "ground")

                elif board[y][x] == "1":
                    self.draw_background(x, y, "ground")
                    self.draw_person(x, y, "player1")

                elif board[y][x] == "2":
                    self.draw_background(x, y, "ground")
                    self.draw_person(x, y, "player2")
                elif board[y][x] == "B":
                    self.draw_background("ground")
                    self.draw_bomb(x, y)

    def draw_background(self, x, y, texture_type):
        background_color = (0, 0, 0)  # Black
        if texture_type == "wall":
            background_color = (74, 78, 84)  # dark grey
        elif texture_type == "ground":
            background_color = (32, 214, 56)  # light green

        rect_width = math.ceil(self.width / self.board_size)
        rect_height = math.ceil(self.height / self.board_size)
        rectangle = pygame.Rect(x * rect_width, y * rect_height, rect_width, rect_height)
        pygame.draw.rect(self.screen, background_color, rectangle)

    def draw_person(self, x, y, player):
        person_color = (0, 0, 0)  # Black
        if player == "player1":
            person_color = (44, 74, 226)  # Blue
        elif player == "player2":
            person_color = (226, 15, 15)  # Red

        edge_buffer = 5

        circle_radius = self.background_size / 4
        circle = pygame.draw.circle(self.screen, person_color,
                                    (x * self.background_size + self.background_size / 2,
                                     y * self.background_size + edge_buffer + circle_radius), circle_radius)

        ellipse_width = self.background_size / 2
        ellipse_height = self.background_size - circle_radius - edge_buffer * 2

        ellipse = pygame.Rect((x * self.background_size + self.background_size / 4,
                               y * self.background_size + circle_radius + edge_buffer),
                              (ellipse_width, ellipse_height))
        pygame.draw.ellipse(self.screen, person_color, ellipse)

    def draw_bomb(self, x, y):
        bomb_img = pygame.image.load(os.path.join('../..pictures/tnt.png')).convert()
        self.screen.blit(bomb_img, (x*self.background_size, y*self.background_size))

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

            # TODO if anotherplayer joins, call start_game()

    def victory_screen(self, winning_player):
        pass
