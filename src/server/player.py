


class Player:
    """Player class for the game 'Bombit' """

    def __init__(self, player_id):
        """
        Init for Player class, takes player_id so that it is possible to differentiate the different Player objects
            if needed.
        :param player_id: The id of the player the instance represents
        """
        self.player_id = player_id
        self.inventory = ['P']
        self.player_direction = 'up'
        self.life = 1

    def pickup(self):
        """
        Picks up an extra bomb, meaning the the player can plant more bombs
        :return:
        """
        self.inventory.append('P')

    def plant_bomb(self):
        """
        Plants a bomb, meaning the inventory empties of one bomb, returns True if it succeded, false otherwise
        :return Bool: True if succes, false otherwise.
        """
        if len(self.inventory) > 0:
            self.inventory.pop(-1)
            return True
        else:
            return False

    def change_player_dir(self, direction):
        """
        Changes the direction the player is pointing in, used to plant in that specified direction,
            could have more uses to. For example drawing the player in different angles based on it's direction
        :param direction:
        :return:
        """
        self.player_direction = direction

    def is_alive(self):
        """
        Returns if the player is alive or dead
        :return Bool: True if alive, otherwise false
        """
        return self.life > 0
