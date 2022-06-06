import socket
import threading
from src.server.player import Player
from src.server.board import Board


class Server:

    def __init__(self):
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

        self.players = []
        self.connections = []
        self.occupied_connections = [["1", False], ["2", False]]

        while True:
            conn, addr = self.s.accept()
            if not self.occupied_connections[0][1]:
                self.occupied_connections[0][1] = True
                self.currentId = connection[0]
                player = Player(self.currentId)
                self.players.append(player)
                self.connections.append(conn)
                print("Connected to: ", addr)
                thread = threading.Thread(target=self.threaded_client, args=(conn, ))
                thread.start()
            if len(self.players) == 2:
                self.board = Board(self.players)

    def accept

    def handle_data(self, data):
        array = data.split(":")
        client_id = int(array[0])
        command = array[1]
        if command == "move":
            direction = array[2]
            self.board.move_character_if_possible(client_id, direction)
        elif command == "plant":
            self.board.plant_bomb_if_possible(client_id, self.broadcast_data)

        elif command == "fetch":
            # Send board to clients
            self.broadcast_data("start")

        self.broadcast_data(self.board.to_string())

    def broadcast_data(self, data):
        print("Broadcasting", data)
        if data != "":
            for conn in self.connections:
                conn.sendall(str.encode(data))


    def threaded_client(self, conn):
        conn.send(str.encode(self.currentId))
        #self.currentId = "2"
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
Server()