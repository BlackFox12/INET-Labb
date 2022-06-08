import socket
import threading
import time

from src.server.board import Board
from src.server.player import Player


class Server:
    """
    The server class, responsible for communicating with all the clients connected to it. Will then handle any
        'legal' commands recieved and tell the game board to update in response to the command.
    """

    def __init__(self):
        """
        Init for the server class. Sets up the socket, and some global variables.
        Then waits for the clients to connect, if there are any viable connection spots left.
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = 'localhost'
        self.port = 5555

        self.server_ip = socket.gethostbyname(self.server)
        try:
            self.s.bind((self.server, self.port))

        except socket.error as e:
            print(str(e))

        self.s.listen(3)
        print("Waiting for a connection")
        self.reply = ''
        self.currentId = ""
        self.players = []
        self.connections = []
        self.occupied_connections = [["1", False], ["2", False]]

        while True:
            conn, addr = self.s.accept()
            if not self.occupied_connections[0][1]:
                self.accept_connection(conn, addr, 0)
            elif not self.occupied_connections[1][1]:
                self.accept_connection(conn, addr, 1)
            else:
                conn.close()
            if len(self.players) == 2:
                self.board = Board(self.players, self.broadcast_data, self.when_player_wins)

    def reset_server(self):
        """
        Closes the connections, opens up the spots for new connections to come in, and empties out both the
            list of players and the list of connections
        :return:
        """
        for connection in self.connections:
            connection.close()
        self.occupied_connections[0][1], self.occupied_connections[1][1] = False, False
        self.players = []
        self.connections = []

    def when_player_wins(self, player):
        """
        When a player wins, it will broadcast to the clients who won, and then reset the server
        :param player: The player who won
        :return:
        """
        time.sleep(2)
        self.broadcast_data(player + ":won")
        time.sleep(1)
        self.reset_server()

    def accept_connection(self, conn, addr, order):
        """
        Acceps a connection and starts a thread for the client which will listen to any client commands.
            Will also print out the address of the client connected.
        :param conn: The connection made with the server
        :param addr: The address of the client
        :param order: Either '0' if first connection or '1' if second connection
        :return:
        """
        self.occupied_connections[order][1] = True
        self.currentId = self.occupied_connections[order][0]
        player = Player(self.currentId)
        self.players.append(player)
        self.connections.append(conn)
        print("Connected to: ", addr)
        thread = threading.Thread(target=self.threaded_client, args=(conn,))
        thread.start()

    def handle_data(self, data):
        """
        Data will come in on the form (id:command:direction) if command is 'move' and instead just (id:command) if
            any other expected type of data. Will call the respective function based on the command received.
        :param data: A string with information from the client
        :return:
        """
        array = data.split(":")
        client_id = int(array[0])
        command = array[1]
        if command == "move":
            direction = array[2]
            self.board.move_character_if_possible(client_id, direction)
        elif command == "plant":
            self.board.plant_bomb_if_possible(client_id)
        elif command == "fetch":
            # Send board to clients
            self.broadcast_data("start")
            self.broadcast_data(self.board.to_string())

    def broadcast_data(self, data):
        """
        Sends data in the form of an encoded string to all current connections.
        :param data: A String
        :return:
        """
        print("Broadcasting", data)
        if data != "":
            for conn in self.connections:
                conn.sendall(str.encode(data))

    def threaded_client(self, conn):
        """
        A thread responsible for listening to clients, decode the data comming in and then try to handle it.
            When a client disconnects it will print that, and make the server ready to accept new connections.
        :param conn: The connection to the client
        :return:
        """
        conn.send(str.encode(self.currentId))
        conn_id = int(self.currentId)
        while True:
            try:
                data = conn.recv(2048)
                reply = data.decode('utf-8')
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    self.handle_data(reply)
            except:
                break
        print("Connection Closed")
        conn.close()
        self.occupied_connections[conn_id - 1][1] = False
        if len(self.connections) > 0:
            self.connections.remove(conn)


Server()
