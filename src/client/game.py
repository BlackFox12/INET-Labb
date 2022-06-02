import pygame
from src.client.canvas import Canvas
from src.client.network import Network
from src.client.player import Player


class Game:

    def __init__(self, w = 800, h = 800):
        self.net = Network()
        self.width = w
        self.height = h
        #self.player1 = Player(50, 50, (44, 74, 226))
        #self.player2 = Player(100,100, (226, 15, 15))

        self.canvas = Canvas(name = "Bombit game")
        self.screen = self.canvas.screen
        self.canvas.running = True
        self.board = []

        if self.net.id == 1:
            self.waiting_for_players_screen()
        else:
            self.start_game()




    def start_game(self):
        self.run()

    def string_board_to_list(self, string):
        one_d_arr = string.split(",")
        board = []
        for i in range(0,13):
            row = []
            for j in range (0,13):
                row.append(one_d_arr[j])
            board.append(row)
        self.board = board

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

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                board = self.net.send(self.net.id + ":move:right")

            if keys[pygame.K_LEFT]:
                board = self.net.send(self.net.id + ":move:left")

            if keys[pygame.K_UP]:
                board = self.net.send(self.net.id + ":move:up")

            if keys[pygame.K_DOWN]:
                board = self.net.send(self.net.id + ":move:down")

            # Send Network Stuff
            #self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.apply_textures(board)
            self.canvas.update()

        pygame.quit()
    """
    def send_data(self):
        
        Send position to server
        :return: None
        
        #data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0 """


    def waiting_for_players_screen(self):
        """Shows the instructions for how to play the game
        In:
            self
        Out:
            None
        """

        self.canvas.click = False
        self.canvas.draw_background()

        while self.canvas.running:
            self.canvas.draw_background()
            self.canvas.draw_text("Waiting for other players", self.canvas.black_color, int(self.canvas.width / 2),
                                  self.canvas.title_spacing_y)

            self.canvas.create_button("Back", 0, int((self.canvas.width - self.canvas.button_width) / 2),
                                      self.canvas.height - self.canvas.button_height * 3)
            self.canvas.update_game_state()

            #TODO if anotherplayer joins, call start_game()
