


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.inventory = ['P']
        self.player_direction = 'up'
        self.life = 1

    def pickup(self):
        self.inventory.append('P')

    def plant_bomb(self):
        if len(self.inventory) > 0:
            self.inventory.pop(-1)
            return True
        else:
            return False

    def change_player_dir(self, direction):
        self.player_direction = direction

    def is_alive(self):
        return self.life > 0



