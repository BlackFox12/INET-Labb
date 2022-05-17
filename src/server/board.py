class Board:
    def __init__(self):
        self.board = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '1', '', '', '', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', '', '', '', '', '#'],
                      ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '', '#'],
                      ['#', '', '', '', '', '', '', '', '', '', '', '2', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

    def move_character_if_possible(self, player_id, direction):
        """
        Will first check if the move is possible, meaning that square is empty, it will then swap current player
            location with that square.
        :param player_id: The id of the current player to be moving
        :param direction: One of ['up', 'down', 'left' 'right']
        :return: False if not possible otherwise the board with the specific board places switched
        """
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == player_id:
                    if direction == 'up':
                        if self.board[y-1][x] == '':
                            self.board[y-1][x], self.board[y][x] = self.board[y][x], self.board[y-1][x]
                            return self.board
                        else:
                            return False
                    elif direction == 'down':
                        if self.board[y + 1][x] == '':
                            self.board[y + 1][x], self.board[y][x] = self.board[y][x], self.board[y + 1][x]
                            return self.board
                        else:
                            return False
                    elif direction == 'left':
                        if self.board[y][x - 1] == '':
                            self.board[y][x - 1], self.board[y][x] = self.board[y][x], self.board[y][x - 1]
                            return self.board
                        else:
                            return False
                    elif direction == 'right':
                        if self.board[y][x + 1] == '':
                            self.board[y][x + 1], self.board[y][x] = self.board[y][x], self.board[y][x + 1]
                            return self.board
                        else:
                            return False


