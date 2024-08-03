import random
from models.game_entities.entity import Entity
from models.game_entities.character import Character

class Fruits(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.set_action(self.name.split("_")[1][0].upper() + self.name.split("_")[1][1:])
        self.is_die_arrow = False
        self.is_action = True
        self.frame = random.randint(0, len(self.images[self.action]) - 2 * self.size_frame)

    def collision_player(self, player : Character):
        if self.is_action:
            for i in player.data[player.action]:
                if player.collision_tognoek_circle(self.get_image(), i, self.get_pos(), 7):
                    self.set_action("Collected")
                    player.update_point(1)
                    self.is_action = False
                    return
    
    def is_die(self):
        return self.is_die_arrow
    

    def update(self, loop=False):
        if super().update():
            if self.action == "Collected":
                self.is_die_arrow = True
