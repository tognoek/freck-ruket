import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character
from models.game_entities.items.break_class import Break
import random

class Box2(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_active = True
        self.live = 4
        self.is_die_box = False
        self.is_breaks = False
        self.breaks = []
        self.loop = False

    def collision_player(self, player : Character):
        if self.is_active:
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            other_rect = pygame.Rect((x, y),(w, h))
            player_rect = player.rect()
            if self.type_entity == 1:
                if player.speed[0] > 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][2]):
                        player_rect.right = other_rect.left + (player_rect.width - player.data[player.action][2][0])
                        player.collisions["right"] = True
                    if player.collision_tognoek(other_rect, player.data[player.action][3]):
                        player_rect.right = other_rect.left + (player_rect.width - player.data[player.action][2][0])
                        player.collisions["right"] = True
                if player.speed[0] < 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][6]):
                        player_rect.left = other_rect.right - player.data[player.action][6][0] - 1
                        player.collisions["left"] = True
                    if player.collision_tognoek(other_rect, player.data[player.action][7]):
                        player_rect.left = other_rect.right - player.data[player.action][7][0] - 1
                        player.collisions["left"] = True
                player.pos = (player_rect.x, player.pos[1])
            player_rect = player.rect()
            if self.type_entity == 1:
                if player.speed[1] < 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][0]):
                        player_rect.top = other_rect.bottom - player.data[player.action][0][1] - 1
                        player.collisions["up"] = True
                        if player.action in ["Jump", "Double Jump"] and self.action != "Hit":
                            self.set_action("Hit")
                            self.live -= 1
                    elif player.collision_tognoek(other_rect, player.data[player.action][1]):
                        player_rect.top = other_rect.bottom - player.data[player.action][1][1] - 1
                        player.collisions["up"] = True
                        if player.action in ["Jump", "Double Jump"] and self.action != "Hit":
                            self.set_action("Hit")
                            self.live -= 1
                if player.speed[1] > 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][4]):
                        player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][4][1])
                        player.collisions["down"] = True
                        if player.action == "Fall" and self.action != "Hit":
                            self.set_action("Hit")
                            self.live -= 1
                    elif player.collision_tognoek(other_rect, player.data[player.action][5]):
                        player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][5][1])
                        player.collisions["down"] = True
                        if player.action == "Fall" and self.action != "Hit":
                            self.set_action("Hit")
                            self.live -= 1
                player.pos = (player.pos[0], player_rect.y)

    def is_die(self):
        return self.is_die_box
    
    def render(self, surface, offset):
        if self.is_breaks:
            if len(self.breaks) == 0:
                pos = (self.pos[0], self.pos[1] - 5)
                image = {"Idle" : [self.images["Break"][0]]}
                entity = Break("break", pos, image, None, (False, False),
                               0, 0, 1, self.type_entity, self.z_index,
                               None, (-0.5, -3), "Idle")
                self.breaks.append(entity)
                pos = (self.pos[0], self.pos[1] - 5)
                image = {"Idle" : [self.images["Break"][1]]}
                entity = Break("break", pos, image, None, (False, False),
                               0, 0, 1, self.type_entity, self.z_index,
                               None, (0.5, -3), "Idle")
                self.breaks.append(entity)
                pos = (self.pos[0], self.pos[1])
                image = {"Idle" : [self.images["Break"][2]]}
                entity = Break("break", pos, image, None, (False, False),
                               0, 0, 1, self.type_entity, self.z_index,
                               None, (-1, -3), "Idle")
                self.breaks.append(entity)
                pos = (self.pos[0], self.pos[1])
                image = {"Idle" : [self.images["Break"][3]]}
                entity = Break("break", pos, image, None, (False, False),
                               0, 0, 1, self.type_entity, self.z_index,
                               None, (1, -3), "Idle")
                self.breaks.append(entity)
            
            for i in self.breaks:
                i.update()
                i.render(surface, offset)
            for i in self.breaks:
                if i.is_die():
                    self.is_die_box = True
        else:
            super().render(surface, offset)
            

    def update(self, loop=False):
        if self.is_die_box:
            return False
        if self.live < 0 and self.is_active:
            self.is_breaks = True
            self.is_active = False
        super().update(self.loop)
            

    
