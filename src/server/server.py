import socket
import threading
import sys
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

        self.s.listen(2)
        print("Waiting for a connection")
        self.reply = ''

        self.currentId = "1"

        self.board = Board()

        self.connections = []
        while True:
            conn, addr = self.s.accept()
            self.connections.append(conn)
            print("Connected to: ", addr)

            thread = threading.Thread(target=self.threaded_client, args=(conn, ))
            thread.start()

    def handle_data(self, data):
        array = data.split(":")
        client_id = int(array[0])
        command = array[1]
        print("id =", client_id, "Command", command)
        if command == "move":
            direction = array[2]
            self.board.move_character_if_possible(client_id, direction)
            print("id =", client_id, "Direction", direction)
        elif command == "throw":
            pass
            # TODO Calculate throw direction, Either place down under, or somehow save latest move direction
        elif command == "pickup":
            # TODO add pickups (power-ups) and ability to pick them up
            pass
        elif command == "fetch":
            # Send board to clients
            self.broadcast_data("start")
        print(self.board.to_string())
        self.broadcast_data(self.board.to_string())

    def broadcast_data(self, data):
        for conn in self.connections:
            conn.sendall(str.encode(data))

    def threaded_client(self, conn):
        conn.send(str.encode(self.currentId))
        self.currentId = "2"
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