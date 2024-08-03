import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character
from models.game_entities.items.break_class import Break
from models.game_entities.items.fruits import Fruits
import random

class Box2(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, 
                 size_frame = 5, type_entity = 1, z_index = 1, data = None, images_fruits = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_active = True
        self.live = 4
        self.is_die_box = False
        self.is_die_breaks = False
        self.is_breaks = False
        self.breaks = []
        self.loop = False
        self.is_fruits = False
        self.is_die_fruits = False
        self.fruits = []
        self.size_fruits = 6
        self.images_fruits = images_fruits

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
        if self.is_die_breaks:
            for item_fruit in self.fruits:
                item_fruit.collision_player(player)
    def is_die(self):
        return self.is_die_box
    
    def render(self, surface, offset, pause = False):
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
                if not pause:
                    i.update()
                i.render(surface, offset)
            for i in self.breaks:
                if i.is_die():
                    self.is_die_breaks = True
        
        if self.is_fruits:
            if len(self.fruits) == 0:
                for _ in range(self.size_fruits):
                    pos = (self.pos[0] + random.randint(-20, 20), self.pos[1] - 5)
                    name = random.choice(["items_apple", "items_bananas", "items_kiwi", "items_cherries", 
                                          "items_pineapple", "items_melon", "items_strawberry", "items_orange"])
                    
                    entity = Fruits(name, pos, self.images_fruits, None, (False, False), 0, random.randint(0, 15), 3, 
                                    self.type_entity, self.z_index, None)
                    self.fruits.append(entity)
            
            for i in self.fruits:
                if  not pause:
                    i.update()
                if not i.is_die():
                    i.render(surface, offset)
            for i in self.fruits:
                if i.is_die():
                    self.is_die_fruits
        else:
            super().render(surface, offset)
            

    def update(self, loop=False):
        self.is_die_box = self.is_die_breaks and self.is_die_fruits
        if self.live < 0 and self.is_active:
            self.is_breaks = True
            self.is_active = False
            self.is_fruits = True
        super().update(self.loop)
            

    
