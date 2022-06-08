import socket
import sys
import threading
import time

import pygame

from src.client.canvas import Canvas
from src.client.game import Game


class Client:
    """
    The class responsible for communicating with the server and handling the server data
    """

    # TODO: Make Client constantly listen to server so that it can get any updates it requires
    def __init__(self):
        """
        Init for the Client class. Sets up the connection to the server, adds a few global variables and starts
            the thread responsible for listening to server commands.
            If the client recieves that it is the first one to connect, it will be sent to a waiting screen until more
            people connect.
            When the second player connects it will send 'fetch' to the server, prompting it to send the board to both
            clients, which will then start the game.
        """
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
        """
        Connects the client to the server, recieves an encoded Id based on if it is the first or second client to connect
        which it decodes and then returns.
        :return id: Either '1' or '2' based on if it was the first or second client to connect to the server.
        """
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def listen_thread(self):
        """
        Resposible for listening to commands from server, if it recieves data from the server it will print it to the
            terminal and then send it to "handle_server_data" which will then take care of the data.
            If it recieves a socket error it will instead just return the error.
        :return socket error: If a socket error was encountered it will return error.
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
        Send data to server as an encoded string, will then sleep for 0.25 seconds to hinder the client from sending
            too much information to the server too fast.
        :return socket error: Will return a string version of the error
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
        """
        Recieves a string which represents a 13x13 board. Will then itterate through the string and create a
            2-d array of the string.
        :param string:
        :return:
        """
        one_d_arr = string.split(",")
        board = []
        for i in range(13):
            row = []
            for j in range(13):
                try:
                    row.append(one_d_arr[i * 13 + j])
                except IndexError:
                    print('Index out of bounds')
            board.append(row)
        self.board = board

    def handle_server_data(self, data):
        """
        If game is over, then data will either be "1:won" if player 1 has won or "2:won" if player 2 has won.
        Can also be 'Start', prompting it to lower the "game.waiting" flag, which will make it so that the client who is
        waiting for more players to join knows that the wait is over. Else it will be the playing-field,
            formated as a string.
        :param data: A decoded string sent over by the server.
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
        """
        Checks if any pygame events has occured, will then change the global variable "self.data" based on what event
            occured. Will then try to start a new thread that sends that data to the server, but only if the last
            send thread has ended.
        :return:
        """
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
        When the game is over, it will instead call the game_end_screen.
        :return:
        """
        clock = pygame.time.Clock()
        self.run = True
        while self.run:
            clock.tick(40)
            self.handle_pygame_events()
        self.game.game_end_screen(self.winner, self.id)
