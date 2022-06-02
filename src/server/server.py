import socket
from _thread import *
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
        while True:
            conn, addr = self.s.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))

    def handle_data(self, data):
        array = data.split(":")
        id = int(array[0])
        command = array[1]
        if command == "move":
            direction = array[2]
            self.board.move_character_if_possible(id, direction)
        elif command == "throw":
            pass
            # TODO Calculate throw direction, Either place down under, or somehow save latest move direction
        elif command == "pickup":
            # TODO add pickups (power-ups) and ability to pick them up
            pass



    def threaded_client(self, conn):
        conn.send(str.encode(self.currentId))
        self.currentId = "2"

        while True:
            try:
                data = conn.recv(2048)
                # data = "Move up"
                # data = Plant Bomb
                # data = pickup


                reply = data.decode('utf-8')
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    """print("Recieved: " + reply)
                    arr = reply.split(":")
                    id = int(arr[0])
                    self.pos[id] = reply

                    if id == 0: nid = 1
                    if id == 1: nid = 0

                    reply = self.pos[nid][:]
                    print("Sending: " + reply) """

                    self.handle_data(reply)

                conn.sendall(str.encode(self.board.to_string()))
            except:
                break
        print("Connection Closed")
        conn.close()






Server()