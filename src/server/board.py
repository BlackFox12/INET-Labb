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
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == element:
                    return x, y

    def move_character_if_possible(self, player_id, direction):
        """
        Will first check if the move is possible, meaning that square is empty, it will then swap current player
            location with that square.
        :param player_id: The id of the current player to be moving
        :param direction: One of ['up', 'down', 'left' 'right']
        """
        x, y = self.index_2d(str(player_id))
        x_move, y_move = self.change_check_square(x, y, direction)
        self.move_dir(x, y, x_move, y_move, str(player_id), direction)

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

    def is_empty(self, x, y):
        return self.board[y][x] == ''

    def is_powerup(self, x, y):
        return self.board[y][x] == 'P'

    def is_player(self, x, y):
        return str(self.board[y][x]) == '1' or str(self.board[y][x]) == '2'

    def is_not_wall(self, x, y):
        return self.board[y][x] != '#'

    def to_string(self):
        """
        Code found here https://www.techiedelight.com/flatten-list-of-lists-python/

        """
        return ",".join(str(x) for x in itertools.chain.from_iterable(self.board))

    def move_dir(self, x_start, y_start, x_move, y_move, player_id, direction):
        if self.is_empty(x_move, y_move) or self.is_powerup(x_move, y_move):
            self.pickup_powerup_if_possible(x_move, y_move, player_id)
            self.board[y_start][x_start], self.board[y_move][x_move] = \
                self.board[y_move][x_move], self.board[y_start][x_start]
            self.players[int(player_id) - 1].change_player_dir(direction)

    def pickup_powerup_if_possible(self, x_move, y_move, player_id):
        if self.is_powerup(x_move, y_move):
            self.players[int(player_id) - 1].pickup()
            self.board[y_move][x_move] = ''

    def plant_bomb_if_possible(self, player_id):
        x, y = self.index_2d(str(player_id))
        x_check, y_check = self.change_check_square(x, y, self.players[int(player_id) - 1].player_direction)
        if self.is_empty(x_check, y_check):
            has_bombs = self.players[int(player_id) - 1].plant_bomb()
            if has_bombs:
                self.board[y_check][x_check] = 'B'
                thread = threading.Thread(target=self.refresh_bomb_thread,
                                          args=(self.players[int(player_id) - 1], x_check, y_check))
                thread.start()

    def apply_and_remove_fire(self, x, y):
        self.apply_elem_in_cross_if_not_wall(x, y, 'F')
        time.sleep(1)
        self.apply_elem_in_cross_if_not_wall(x, y, '')

    def apply_elem_in_cross_if_not_wall(self, x, y, elem):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.board[y][x] = elem
        for cords in directions:
            no_wall_flag = True
            for i in range(1, 3):
                if self.is_not_wall(x + cords[0] * i, y + cords[1] * i) and no_wall_flag:
                    if self.is_player(x + cords[0] * i, y + cords[1] * i):
                        self.players[int(self.board[y + cords[1] * i][x + cords[0] * i]) - 1].life = 0
                    self.board[y + cords[1] * i][x + cords[0] * i] = elem
                else:
                    no_wall_flag = False

    def refresh_bomb_thread(self, player, x, y):
        time.sleep(3)
        self.apply_and_remove_fire(x, y)
        player.pickup()
        self.board[y][x] = ''


