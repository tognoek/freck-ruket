import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character
from models.game_entities.dust_particle import Dustparticle

class FallingPlatforms(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.action = "On"
        self.is_active = True
        self.down = False
        self.is_dust_particle = True
        self.index_down = 0
        self.die = 0
        self.array = [2, 2, 2, -2, -2, -2]
        self.loopdown = False
        self.size_idle = 50
        self.index_idle = 0
        self.dust_particles = []
        self.speed_down = 3
        self.max_speed_down = 7

    def collision_player(self, player : Character):
        player.idle_look = False
        if self.is_active:
            player_rect = player.rect()
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            other_rect = pygame.Rect((x, y),(w, h))
            if not player.collisions["down"]:
                player.pos = (player.pos[0], player.pos[1] + 3)

            if player.speed[1] > 0:
                if player.collision_tognoek(other_rect, player.data[player.action][4]):
                    player.collisions["down"] = True
                    player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][4][1])
                    player.idle_look = True
                    if not self.down:
                        self.down = True
                if player.collision_tognoek(other_rect, player.data[player.action][5]):
                    player.collisions["down"] = True
                    player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][5][1])
                    player.idle_look = True
                    if not self.down:
                        self.down = True

            player.pos = (player.pos[0], player_rect.y)
            
    def dust_particle(self):

        if self.is_active:
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            for i in Dustparticle.create_dust_particles_fly((x + 4, y + 6), 1, (w - 8, h), 0, (20, 40), False):
                self.dust_particles.append(i)

    def update(self, loop=True):
        super().update(loop)
        if self.down and self.is_active and not self.loopdown:
            self.pos = (self.pos[0], self.pos[1] + self.array[self.index_down])
            self.index_down += 1
            if self.index_down >= len(self.array):
                self.index_down = 0
                self.loopdown = True

        if self.loopdown and self.is_active:
            self.index_idle += 1
            if self.index_idle >= self.size_idle:
                self.set_action("Idle")
                self.is_active = False

        if not self.is_active:
            self.pos = (self.pos[0], self.pos[1] + self.speed_down)
            self.speed_down += 0.5
            if self.speed_down > self.max_speed_down:
                self.speed_down = self.max_speed_down
            self.die += 1

    def is_die(self):
        return self.die > 100


    def render(self, surface, offset, pause):
        super().render(surface, offset, pause)
        if self.frame % 3 == 0:
            if not pause:
                self.dust_particle()
        for i in self.dust_particles:
            if not pause:
                i.update()
            i.render(surface, offset)
            if i.is_die():
                self.dust_particles.remove(i)
