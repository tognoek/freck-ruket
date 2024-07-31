import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character
from models.game_entities.dust_particle import Dustparticle

class Trampoline(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_active = True
        self.count_active = 0
        self.size_active = 100
        self.feedback_force = -10
        self.is_dust_particle = True

    def collision_player(self, player : Character):
        if self.is_active:
            player_rect = player.rect()
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            other_rect = pygame.Rect((x, y),(w, h))
            if player.speed[1] > 0:
                if player.collision_tognoek(other_rect, player.data[player.action][4]):
                    if player.data[player.action][4][1] + player.get_pos()[1] - other_rect.top <= player.speed[1]:
                        self.is_active = False
                        self.set_action("Jump")
                        player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][4][1]) - 1
                        player.count_jump = 0
                        player.speed_y(self.feedback_force)
                if player.collision_tognoek(other_rect, player.data[player.action][5]):
                    if player.data[player.action][5][1] + player.get_pos()[1] - other_rect.top <= player.speed[1]:
                        self.is_active = False
                        player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][5][1]) - 1
                        self.set_action("Jump")
                        player.count_jump = 0
                        player.speed_y(self.feedback_force)

            player.pos = (player.pos[0], player_rect.y)

    def update(self, loop=False):
        if not self.is_active:
            self.count_active += 1
            if self.count_active >= self.size_active:
                self.is_active = True
                self.count_active = 0
        super().update(loop)

    def dust_particle(self):

        if self.is_dust_particle and self.action == "Jump":
            self.is_dust_particle = False
            frame = int(self.frame / self.size_frame)
            x = self.get_pos()[0] + self.data[self.action][frame][0][0]
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            for i in Dustparticle.create_dust_particles((x, y), 10, (w, h), 0, 1):
                self.dust_particles.append(i)

        if self.action == "Idle" and self.old_acction == "Jump":
            self.is_dust_particle = True


    def render(self, surface, offset, pause):
        super().render(surface, offset)
        self.dust_particle()
        for i in self.dust_particles:
            if not pause:
                i.update()
                i.render(surface, offset)
            if i.is_die():
                self.dust_particles.remove(i)
