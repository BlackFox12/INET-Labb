import pygame
from src.client.canvas import Canvas


class Game:

    def __init__(self, w = 800, h = 800):
        self.width = w
        self.height = h

        self.canvas = Canvas(name = "Bombit game")
        self.screen = self.canvas.screen
        self.canvas.running = True
        self.waiting = False

    def apply_textures(self, board):
        wall_color = (74, 78, 84)       # dark grey
        player1_color = (44, 74, 226)   # Blue
        player2_color = (226, 15, 15)   # Red
        ground_color = (32, 214, 56)    # light green

        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == "#":
                    self.canvas.draw_bombit_rectangles(x, y, wall_color)

                elif board[y][x] == "":
                    self.canvas.draw_bombit_rectangles(x, y, ground_color)

                elif board[y][x] == "1":
                    self.canvas.draw_bombit_rectangles(x, y, player1_color)

                elif board[y][x] == "2":
                    self.canvas.draw_bombit_rectangles(x, y, player2_color)
        pygame.display.update()

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

            #TODO if anotherplayer joins, call start_game()

    def victory_screen(self, winning_player):
        pass
