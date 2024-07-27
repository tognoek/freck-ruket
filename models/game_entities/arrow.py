import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character

class Arrow(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_die_arrow = False
        self.is_action = False

    def collision_player(self, player : Character):
        if not self.is_action:
            for i in player.data[player.action]:
                if player.collision_tognoek_circle(self.get_image(), i, self.get_pos(), 7):
                    self.set_action("Hit")
                    player.count_jump = 0
                    player.speed_y(-10)
                    self.is_action = True
                    return
    
    def is_die(self):
        return self.is_die_arrow
    

    def update(self, loop=False):
        if super().update():
            if self.action == "Hit":
                self.is_die_arrow = True
