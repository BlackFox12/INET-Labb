import pygame
import socket
import threading
from src.client.game import Game

class Client:
    # TODO: Make Client constantly listen to server so that it can get any updates it requires
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"  # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
        # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
        # ipv4 address. This feild will be the same for all your clients.
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()
        print("ID:", self.id)
        self.run = False
        self.thread_running = False
        self.game = Game()
        self.board = []

        thread = threading.Thread(target=self.listen_thread)
        thread.start()


        if self.id == "2":
            self.send_data_to_server("fetch")
            self.game_loop()
        else:
            self.game.waiting_for_players_screen()
            self.game_loop()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def listen_thread(self):
        """
        Retrieve data from server on a continious running thread.
        """
        self.thread_running = True
        while self.thread_running:
            try:
                data = self.client.recv(2048).decode()
                print("Data:", data)
                self.handle_server_data(data)
            except socket.error as e:
                return str(e)

    def send_data_to_server(self, data):
        """
        Send data to server as an encoded string
        :param data:
        :return:
        """
        try:
            self.client.send(str.encode(self.id + ":" + data))
        except socket.error as e:
            return str(e)

    def string_board_to_list(self, string):
        one_d_arr = string.split(",")
        board = []
        for i in range(13):
            row = []
            for j in range(13):
                row.append(one_d_arr[i*13 + j])
            print(row)
            board.append(row)
        self.board = board

    def handle_server_data(self, data):
        """
        If game is over, then data will either be "1:won" if player 1 has won or "2:won" if player 2 has won. Else it will be
        the playing-field, formated as a string.
        :param data:
        :return:
        """
        if data == "1:won" or data == "2:won":
            self.run = False
            self.game.victory_screen(data)
        elif data == "start":
            self.game.waiting = False
        else:
            self.string_board_to_list(data)
            self.game.apply_textures(self.board)

    def handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.K_ESCAPE:
                self.run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.send_data_to_server("move:right")

        if keys[pygame.K_LEFT]:
            self.send_data_to_server("move:left")

        if keys[pygame.K_UP]:
            self.send_data_to_server("move:up")

        if keys[pygame.K_DOWN]:
            self.send_data_to_server("move:down")

        if keys[pygame.K_SPACE]:
            self.send_data_to_server("throw")

        if keys[pygame.K_a]:
            self.send_data_to_server("pickup")


    def game_loop(self):
        """
        Every clock-cycle listen for user-input and if there is any, then send data to the server
        :return:
        """
        clock = pygame.time.Clock()
        self.run = True
        while self.run:
            clock.tick(10)
            self.handle_pygame_events() # TODO FIX, currently sends multiple events to server