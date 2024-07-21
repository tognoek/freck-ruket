import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character
from models.game_entities.dust_particle import Dustparticle

class Fan(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_active = True
        self.count_active = 0
        self.size_active = 30
        self.wind_power = 100
        self.power_fan = 3
        self.dust_particles = []

    def collision_player(self, player : Character):
        player.lock_jump = False
        if self.is_active:
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y_r = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            y = y_r - h
            other_rect = pygame.Rect((x, y),(w, h))
            wind_rect = pygame.Rect((x, y_r - self.wind_power), (w, self.wind_power))
            player_rect = player.rect()

            if self.type_entity == 1 and self.action == "On":
                if player.collision_tognoek(wind_rect,  player.data[player.action][4]):
                    player.lock_jump = True
                    player.set_action("Jump")
                    player.count_jump = 1
                    if player.data[player.action][4][1] + player.get_pos()[1] - (y_r - self.wind_power) < self.power_fan:
                        if not player.key_up:
                            player.speed = (player.speed[0], 0)
                    else:
                        player.speed = (player.speed[0], 0 - self.power_fan)
                if player.collision_tognoek(wind_rect,  player.data[player.action][5]):
                    player.lock_jump = True
                    player.set_action("Jump")
                    player.count_jump = 1
                    if player.data[player.action][5][1] + player.get_pos()[1] - (y_r - self.wind_power) < self.power_fan:
                        if not player.key_up:
                            player.speed = (player.speed[0], 0)
                    else:
                        player.speed = (player.speed[0], 0 - self.power_fan)
            if self.type_entity == 1 and self.action == "Idle":
                if player.collision_tognoek(other_rect, player.data[player.action][4]):
                    self.set_action("On")
                    player.speed_y(-8)
                    player.count_jump = 1
                    player.set_action("Jump")
                if player.collision_tognoek(other_rect, player.data[player.action][5]):
                    self.set_action("On")
                    player.speed_y(-8)
                    player.count_jump = 1
                    player.set_action("Jump")
                player.pos = (player.pos[0], player_rect.y)

            other_rect = pygame.Rect((x, y_r),(w, h))
            player_rect = player.rect()
            if self.type_entity == 1 and self.action == "On":
                if player.collision_tognoek(other_rect, player.data[player.action][2]):
                    player.type_entity = 3
                if player.collision_tognoek(other_rect, player.data[player.action][3]):
                    player.type_entity = 3
                if player.collision_tognoek(other_rect, player.data[player.action][6]):
                    player.type_entity = 3
                if player.collision_tognoek(other_rect, player.data[player.action][7]):
                    player.type_entity = 3
                
                player.pos = (player_rect.x, player.pos[1])

    def update(self, loop=False):
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0
            if self.action == "On":
                self.count_active += 1
            if self.count_active > self.size_active:
                self.set_action("Idle")
                self.count_active = 0
    def dust_particle(self):

        if self.action == "On":
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            for i in Dustparticle.create_dust_particles_fly((x, y), 1, (w, h), 0, (20, 40)):
                self.dust_particles.append(i)

    def render(self, surface, offset):
        # print(123123)
        super().render(surface, offset)
        self.dust_particle()
        for i in self.dust_particles:
            i.update()
            i.render(surface, offset)
            if i.is_die():
                self.dust_particles.remove(i)
