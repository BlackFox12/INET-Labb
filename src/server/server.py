import socket
from _thread import *
import sys


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

        self.currentId = "0"

        # pos = board[1][1]
        self.pos = ["0:1,1", "1:11,11"]
        while True:
            conn, addr = self.s.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))

    def threaded_client(self, conn):
        conn.send(str.encode(self.currentId))
        self.currentId = "1"

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
                    print("Recieved: " + reply)
                    arr = reply.split(":")
                    id = int(arr[0])
                    self.pos[id] = reply

                    if id == 0: nid = 1
                    if id == 1: nid = 0

                    reply = self.pos[nid][:]
                    print("Sending: " + reply)

                conn.sendall(str.encode(reply))
            except:
                break
        print("Connection Closed")
        conn.close()



Server()