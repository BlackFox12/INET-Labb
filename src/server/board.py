import itertools
import threading
import time

class Board:
    """Board class, handles all the games logic based on what the players decied to do"""

    def __init__(self, players, when_board_updates, when_player_wins):
        """
        Init for the board class, sets up the board and some global variables
        :param players: An array containing two instances of the Player class
        :param when_board_updates: A function to be called every time some change is made on the board
        :param when_player_wins:  A function to be called when someone has won
        """
        self.players = players
        self.when_board_updates = when_board_updates
        self.when_player_wins = when_player_wins
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
        """
        Return X and Y index of a specified element, returns False if it cannot be found.
        :param element: The element to be searched for
        :return: X and Y coords on the board for the first instance of the specified element, False if can't be found
        """
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == element:
                    return x, y
        return False

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
        """
        Based on direction will change x and y to one square away from what they originally were.
        :param x: Coords in X-direction
        :param y: Coords in Y-direction
        :param direction: One of ['up', 'down', 'left' 'right']
        :return x_move, y_move: Coords one away from x and y's original value.
        """
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
        """
        Returns true if the x and y coords specified is an empty square
        :param x: Coords in X-direction
        :param y: Coords in Y-direction
        :return Bool: True if it is empty, False if not
        """
        return self.board[y][x] == ''

    def is_powerup(self, x, y):
        """
        Returns true if the x and y coords specified contains 'P' (meaning powerup or extra_bomb)
        :param x: Coords in X-direction
        :param y: Coords in Y-direction
        :return Bool: True if it is 'P', False if not
        """
        return self.board[y][x] == 'P'

    def is_player(self, x, y):
        """
        Returns true if the x and y coords specified contains '1' or '2' (meaning player one or two)
        :param x: Coords in X-direction
        :param y: Coords in Y-direction
        :return Bool: True if it is '1' or '2', False if not
        """
        return str(self.board[y][x]) == '1' or str(self.board[y][x]) == '2'

    def is_not_wall(self, x, y):
        """
        Returns true if the x and y coords specified does not contains '#' (meaning wall)
        :param x: Coords in X-direction
        :param y: Coords in Y-direction
        :return Bool: True if it is not '#', False if it is
        """
        return self.board[y][x] != '#'

    def is_walkable_square(self, x, y):
        """
        Returns true if the x and y coords specified either is empty, contains powerup or Fire
        :param x: Coords in X-direction
        :param y: Coords in Y-direction
        :return Bool: True if it is a walkable square, false if not (Either player, wall or bomb)
        """
        return self.board[y][x] == '' or self.board[y][x] == 'P' or self.board[y][x] == 'F'

    def to_string(self):
        """
        Code found here https://www.techiedelight.com/flatten-list-of-lists-python/
        Flattens the 2-d array into a string, with a comma ',' added between each element
        :return String: A string representing the current state of the board
        """
        return ",".join(str(x) for x in itertools.chain.from_iterable(self.board))

    def move_dir(self, x_start, y_start, x_move, y_move, player_id, direction):
        """
        Tries to make the specified player move from (x_start, y_start) into (x_move, y_move)
            Will end the game if player walks into fire. Otherwise will just send over the current state of the board
            to the clients if the move was successfull
        :param x_start: x-coords for the starting poisition of the player
        :param y_start: y-coords for the starting poisition of the player
        :param x_move: x-coords for the position the player wants to move into
        :param y_move: y-coords for the position the player wants to move into
        :param player_id: The id of the player that wants to move
        :param direction: The current direction the player is facing
        :return:
        """
        if self.is_walkable_square(x_move, y_move):
            if self.board[y_move][x_move] == 'F':
                winner = "1" if player_id == "2" else "2"
                self.board[y_start][x_start] = ''
                self.when_board_updates(self.to_string())
                self.when_player_wins(winner)
                return
            else:
                self.pickup_powerup_if_possible(x_move, y_move, player_id)
                self.board[y_start][x_start], self.board[y_move][x_move] = \
                    self.board[y_move][x_move], self.board[y_start][x_start]
                self.players[int(player_id) - 1].change_player_dir(direction)
                self.when_board_updates(self.to_string())

    def pickup_powerup_if_possible(self, x_move, y_move, player_id):
        """
        Tries to pickup a 'P' from the board and add it to the players inventory.
            Only succeds if the square the player wants to move into contains a 'P'
        :param x_move: The x-coords for the square the player is moving into
        :param y_move: The y-coords for the square the player is moving into
        :param player_id: The player that is performing the move
        :return:
        """
        if self.is_powerup(x_move, y_move):
            self.players[int(player_id) - 1].pickup()
            self.board[y_move][x_move] = ''
            self.when_board_updates(self.to_string())

    def plant_bomb_if_possible(self, player_id):
        """
        Tries to plant a bomb on the board. Only succeeds if the player has bombs in their invenytory and the
            square the player is trying to plant the bomb in is currently empty.
        :param player_id: The id of the player trying to plant the bomb
        :return:
        """
        x, y = self.index_2d(str(player_id))
        x_check, y_check = self.change_check_square(x, y, self.players[int(player_id) - 1].player_direction)
        if self.is_empty(x_check, y_check):
            has_bombs = self.players[int(player_id) - 1].plant_bomb()
            if has_bombs:
                self.board[y_check][x_check] = 'B'
                self.when_board_updates(self.to_string())
                thread = threading.Thread(target=self.refresh_bomb_thread,
                                          args=(self.players[int(player_id) - 1], x_check, y_check))
                thread.start()

    def apply_and_remove_fire(self, x, y):
        """
        Replaces all the non-wall squares in a cross pattern with Fire, broadcasts the board to the clients.
            Then returns the board to it's previous state (minus power-ups) if noone died, else ends the game
        :param x: X-Coords for middle of the cross (where the bomb is planted)
        :param y: Y-Coords for middle of the cross (where the bomb is planted)
        :return:
        """
        self.apply_elem_in_cross_if_not_wall(x, y, 'F')
        self.when_board_updates(self.to_string())
        if not self.players[0].is_alive():
            self.when_player_wins("2")
        elif not self.players[1].is_alive():
            self.when_player_wins("1")
        else:
            time.sleep(1)
            self.apply_elem_in_cross_if_not_wall(x, y, '')
            self.when_board_updates(self.to_string())

    def apply_elem_in_cross_if_not_wall(self, x, y, elem):
        """
        Will try to apply the specified elemnt in a cross pattern on non-wall squares. If it encounters a wall it will
            raise a flag and won't replace any more squares in that direction. The flag is reset when it later moves on
            and tries to apply the elemnt in other directions.
        :param x: X-Coords for middle of the cross (where the bomb is planted)
        :param y: Y-Coords for middle of the cross (where the bomb is planted)
        :param elem: The element that will replace non-wall elements on the board.
        :return:
        """
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.board[y][x] = elem
        for cords in directions:
            no_wall_flag = True
            for i in range(1, 3):
                if no_wall_flag and self.is_not_wall(x + cords[0] * i, y + cords[1] * i):
                    if self.is_player(x + cords[0] * i, y + cords[1] * i):
                        self.players[int(self.board[y + cords[1] * i][x + cords[0] * i]) - 1].life = 0
                    self.board[y + cords[1] * i][x + cords[0] * i] = elem
                else:
                    no_wall_flag = False

    def refresh_bomb_thread(self, player, x, y):
        """
        Will apply fire in a cross starting from the x and y coords of tha planted bomb. Then it will remove the fire and replace
        with empty squares. Will afterwards return the bomb into the players inventory.
        :param player:
        :param x: X-Coords for middle of the cross (where the bomb is planted)
        :param y: Y-Coords for middle of the cross (where the bomb is planted):
        :return:
        """
        time.sleep(3)
        self.apply_and_remove_fire(x, y)
        player.pickup()
