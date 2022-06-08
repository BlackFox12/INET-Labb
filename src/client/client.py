import pygame
import socket
import threading
import time
import sys
from src.client.canvas import Canvas
from src.client.game import Game

class Client:
    """The class responsible for communicating with the server and handling the server data
    """
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
        self.thread_running = True
        self.game = Game()
        self.canvas = Canvas()
        self.board = []
        thread = threading.Thread(target=self.listen_thread)
        thread.start()
        self.winner = "0"
        self.data = "fetch"
        if self.id == "2":
            self.data = "fetch"
            self.send_thread = threading.Thread(target=self.send_data_to_server_thread)
            self.send_thread.start()
            self.game_loop()
        else:
            self.game.waiting_for_players_screen()
            self.send_thread = threading.Thread(target=self.send_data_to_server_thread)
            self.send_thread.start()
            self.game_loop()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def listen_thread(self):
        """
        Retrieve data from server on a continious running thread.
        """
        while self.thread_running:
            try:
                data = self.client.recv(2048).decode()
                print("recieved:", data)
                self.handle_server_data(data)
            except socket.error as e:
                return str(e)

    def send_data_to_server_thread(self):
        """
        Send data to server as an encoded string
        :param data:
        :return:
        """
        try:
            print("Sending: " + self.data)
            self.client.send(str.encode(self.id + ":" + self.data))
            self.data = ""
            time.sleep(0.25)
            sys.exit()
        except socket.error as e:
            return str(e)

    def string_board_to_list(self, string):
        one_d_arr = string.split(",")
        board = []
        for i in range(13):
            row = []
            for j in range(13):
                row.append(one_d_arr[i*13 + j])
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
            self.thread_running = False
            array = data.split(":")
            self.winner = array[0]
        elif data == "start":
            self.game.waiting = False
        else:
            self.string_board_to_list(data)
            self.game.apply_textures(self.board)

    def handle_pygame_events(self):
        self.canvas.update_game_state()
        keys = pygame.key.get_pressed()
        self.data = ""

        if keys[pygame.K_RIGHT]:
            self.data = "move:right"

        elif keys[pygame.K_LEFT]:
            self.data = "move:left"

        elif keys[pygame.K_UP]:
            self.data = "move:up"

        elif keys[pygame.K_DOWN]:
            self.data = "move:down"

        elif keys[pygame.K_SPACE]:
            self.data = "plant"

        if self.data != "" and not self.send_thread.is_alive():
            self.send_thread = threading.Thread(target=self.send_data_to_server_thread)
            self.send_thread.start()

    def game_loop(self):
        """
        Every clock-cycle listen for user-input and if there is any, then send data to the server
        :return:
        """
        clock = pygame.time.Clock()
        self.run = True
        while self.run:
            clock.tick(40)
            self.handle_pygame_events() # TODO FIX, currently sends multiple events to server
        self.game.game_end_screen(self.winner, self.id)

