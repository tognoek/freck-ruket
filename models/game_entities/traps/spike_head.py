import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character
from models.game_entities.dust_particle import Dustparticle

class SpikeHead(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None, vector = []):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        # self.action = "Blink"
        self.speed_rock = 0
        self.speed_max = 5
        self.vector = vector
        if self.vector == []:
            self.vector = [1, 2]
        for i in self.vector:
            if i < 1 or i > 4:
                self.vector = [1, 2]
                break
        # 1 left, 2 right, 3 top, 4 bottom
        self.array = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        self.name_action = ["", "Left Hit", "Right Hit", "Top Hit", "Bottom Hit"]
        self.index_action = 0
        self.old_index = 0

    def collision_player(self, player : Character, maps = None):
        player_rect = player.rect()
        frame = int(self.frame / self.size_frame)
        x = self.get_pos()[0] + self.data[self.action][frame][0][0]
        y = self.get_pos()[1] + self.data[self.action][frame][0][1]
        w = self.data[self.action][frame][1][0]
        h = self.data[self.action][frame][1][1]
        other_rect = pygame.Rect((x, y),(w, h))
        if self.type_entity == 1:
            for i in range(8):
                if player.collision_tognoek(other_rect, player.data[player.action][i]):
                    player.type_entity = 3

    def collision(self, other):
        if self.action == "Idle":
            self.pos = (self.pos[0] + self.array[self.vector[self.index_action]][0] * self.speed_rock, self.pos[1] + self.array[self.vector[self.index_action]][1] * self.speed_rock)
        entity_rect = self.rect()
        coll =  False
        for i in other:
            if self.collision_rect(i)[0] and i.type_entity == 1:
                if self.array[self.vector[self.index_action]][0] > 0:
                    entity_rect.right = i.rect().left + 0
                    coll = True
                if self.array[self.vector[self.index_action]][0] < 0:
                    entity_rect.left = i.rect().right - 0
                    coll = True
                if self.array[self.vector[self.index_action]][1] > 0:
                    entity_rect.bottom = i.rect().top + 0
                    coll = True
                if self.array[self.vector[self.index_action]][1] < 0:
                    entity_rect.top = i.rect().bottom - 0
                    coll = True
                self.pos = (entity_rect.x, entity_rect.y)

        if coll:
            self.index_action = (self.index_action + 1) % len(self.vector)
            self.set_action(self.name_action[self.vector[self.index_action]])
            self.speed_rock = 0
                

    def update(self, map):
        if super().update():
            if self.action == "Blink":
                self.set_action("Idle")
            if self.action in self.name_action:
                self.set_action("Blink")
        if self.action == "Idle":
            self.speed_rock += 0.2
            if self.speed_rock > self.speed_max:
                self.speed_rock = self.speed_max
        self.collision(map)

            

    


        

