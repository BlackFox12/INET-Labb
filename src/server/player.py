


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.inventory = []
        self.player_direction = 'up'

    def pickup(self):
        self.inventory.append('P')

    def plant_bomb(self):
        if len(self.inventory) > 0:
            self.inventory.pop(-1)

    def change_player_dir(self, direction):
        self.player_direction = direction



