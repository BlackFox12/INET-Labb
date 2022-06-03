import itertools

import threading
import time

class Board:
    def __init__(self, players):
        self.players = players
        self.board = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '1', '', '', '', '', '', '', '', '', 'P', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', 'P', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', 'P', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', 'P', '', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', '', '', '', '2', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

    def index_2d(self, element):
        for y, x in enumerate(self.board):
            if element in x:
                return y, x.index(element)

    def move_character_if_possible(self, player_id, direction):
        """
        Will first check if the move is possible, meaning that square is empty, it will then swap current player
            location with that square.
        :param player_id: The id of the current player to be moving
        :param direction: One of ['up', 'down', 'left' 'right']
        """
        player_str = str(player_id)
        y, x = self.index_2d(player_str)
        x_move, y_move = self.change_check_square(x, y, direction)
        self.move_dir(x, y, x_move, y_move, player_str, direction)

    def change_check_square(self, x, y, direction):
        x_move, y_move = x, y
        if direction == 'up':
            y_move = y_move - 1
        elif direction == 'down':
            y_move = y_move + 1
        elif direction == 'left':
            x_move = x_move - 1
        elif direction == 'right':
            x_move = x_move + 1
        return x_move, y_move

    def check_if_square_is_empty(self, x, y):
        if self.board[y][x] == '':
            return True
        else:
            return False

    def to_string(self):
        """
        Code found here https://www.techiedelight.com/flatten-list-of-lists-python/

        """
        return ",".join(str(x) for x in itertools.chain.from_iterable(self.board))

    def move_dir(self, x_start, y_start, x_move, y_move, player_id, direction):
        if self.change_check_square(x_move, y_move) or self.board[y_move][x_move] == 'P':
            self.pickup_powerup_if_possible(x_move, y_move, player_id)
            self.board[y_start][x_start], self.board[y_move][x_move] = \
                self.board[y_move][x_move], self.board[y_start][x_start]
            self.players[int(player_id) - 1].change_player_dir(direction)

    def pickup_powerup_if_possible(self, x_move, y_move, player_id):
        if self.board[y_move][x_move] == 'P':
            self.players[int(player_id) - 1].pickup()
            self.board[y_move][x_move] = ''

    def plant_bomb_if_possible(self, player_id):
        y, x = self.index_2d(str(player_id))
        x_check, y_check = self.change_check_square(y, x, self.players[int(player_id) - 1].player_direction)
        if self.change_check_square(x_check, y_check, self.players[int(player_id) - 1].player_direction):
            self.board[y_check][x_check] = 'B'
            self.players[int(player_id) - 1].plant_bomb()
            thread = threading.Thread(target=self.refresh_bomb_thread,
                                      args=(self.players[int(player_id) - 1], x_check, y_check))
            thread.start()

    def refresh_bomb_thread(self, player, x, y):
        time.sleep(3)
        player.pickup()
        self.board[y][x] = ''


