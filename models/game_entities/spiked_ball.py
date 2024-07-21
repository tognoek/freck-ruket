import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character 
import math

class SpikedBall(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
    
    def collision_player(self, player : Character):
        for i in range(8):
            if player.collision_tognoek_rect(self.image_rotate, player.data[player.action][i], self.pos_iamge, 14):
                player.type_entity = 3
                return
            
    def calculate_coordinates(self, x1, y1, x2, y2, step=1, offet = (0, 0)):
        coordinates = []
        
        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        
        steps = int(distance // step)
        
        for i in range(steps + 1):
            t = i / steps
            x = x1 + t * dx - offet[0]
            y = y1 + t * dy - offet[1]
            coordinates.append((round(x), round(y)))
        
        return coordinates

    def create(self):
        temp = self.data.copy()
        dx = temp[0][1][0] - temp[1][1][0]
        dy = temp[0][1][1] - temp[1][1][1]
        if len(temp[1][0]) >  2:
            self.max_angle = temp[1][0][2] / 2
        else:
            self.max_angle = 0
        self.len = math.hypot(dx, dy)
        if len(temp[1][0]) >  3:
            self.distance = temp[1][0][3]
        else:
            self.distance = 1
        self.angle = math.radians(self.max_angle)
        self.coordinates = (temp[0][1][0], temp[0][1][1])
        self.angle_default = 2 * math.asin(self.distance / 2 / self.len)
        self.angle_step = self.angle_default / 50
        self.angle_r = 0
        self.vector = -1
        self.vector_step = 1

    def update(self):
        super().update()
        dx = math.sin(self.angle) * self.len
        dy = math.cos(self.angle) * self.len
        self.pos = (dx + self.coordinates[0] , dy + self.coordinates[1])

        if self.max_angle > 0:
            angle_old = self.angle
            self.angle_r += self.vector_step * self.angle_step
            self.angle +=  self.angle_r * self.vector
            if angle_old * self.angle <= 0:
                self.vector_step *= -1
            if math.fabs(self.angle) > math.radians(self.max_angle):
                self.vector *= -1
                self.vector_step *= -1
                self.angle_r = 0
        else:
            self.angle += self.angle_default
            self.angle = self.angle % (2 * math.pi)

        self.image_rotate = self.get_image()

    def render(self, surface : pygame.Surface, offset):
        pos = self.get_pos()
        for t in self.calculate_coordinates(self.coordinates[0], self.coordinates[1], pos[0], pos[1], step = 10):
            surface.blit(self.images["Chain"][0], (t[0] + offset[0], t[1] + offset[1]))
            self.pos_iamge = (t[0], t[1])
        self.pos_iamge = (self.pos_iamge[0] - self.image_rotate.get_width() / 2 + 4, self.pos_iamge[1] - self.image_rotate.get_height() / 2 + 4)
        surface.blit(self.image_rotate, (self.pos_iamge[0] + offset[0], self.pos_iamge[1] + offset[1]))
        # super().render(surface, offset)