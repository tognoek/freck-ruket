import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character
from models.game_entities.traps.broken import Broken
import random

class Blocks(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_active = True
        self.live = random.randint(3, 5)
        self.is_die_blocks = False
        self.is_broken = False
        self.broken = []
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
                        if player.action in ["Jump", "Double Jump"]:
                            self.set_action("HitTop")
                            self.live -= 1
                    if player.collision_tognoek(other_rect, player.data[player.action][1]):
                        player_rect.top = other_rect.bottom - player.data[player.action][1][1] - 1
                        player.collisions["up"] = True
                        if player.action in ["Jump", "Double Jump"]:
                            self.set_action("HitTop")
                            self.live -= 1
                if player.speed[1] > 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][4]):
                        player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][4][1])
                        player.collisions["down"] = True
                        if player.action == "Fall":
                            self.set_action("HitTop")
                            self.live -= 1
                    if player.collision_tognoek(other_rect, player.data[player.action][5]):
                        player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][5][1])
                        player.collisions["down"] = True
                        if player.action == "Fall":
                            self.set_action("HitTop")
                            self.live -= 1
                player.pos = (player.pos[0], player_rect.y)

    def is_die(self):
        return self.is_die_blocks
    
    def render(self, surface, offset):
        if not self.is_broken:
            super().render(surface, offset)
        else:
            if len(self.broken) == 0:
                pos = (self.pos[0], self.pos[1])
                entity = Broken("broken_1", (pos[0], pos[1] + 10), self.images, None, (False, False), 0, 0, 4, 
                                self.type_entity, self.z_index, None, [-0.5, -3], "Part 1")
                self.broken.append(entity)
                entity = Broken("broken_1", pos, self.images, None, (False, False), 0, 0, 4, 
                                self.type_entity, self.z_index, None, [0.5, -3], "Part 2")
                self.broken.append(entity)
            for i in self.broken:
                i.update()
                i.render(surface, offset)
            
            for i in self.broken:
                if i.is_die():
                    self.is_die_blocks = True
                    return
            

    def update(self, loop=False):
        if self.is_broken:
            return False
        if self.live < 0 and self.is_active:
            self.is_active = False
            self.size_frames = 5
            self.set_action("HitSide")
            self.loop = True
        if super().update(self.loop) and self.action == "HitSide":
            self.is_broken = True

    
