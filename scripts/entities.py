import pygame


class Entiti:

    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5):
        self.name = name
        self.pos = pos
        self.images = images
        self.sound = sound
        self.flip = flip
        self.volume = volume
        self.frame = frame
        self.action = 'Idle'
        self.size_frame = size_frame

    def copy(self):
        return Entiti(self.name, self.x, self.y, self.images, self.sound, self.volume, self.frame)
    
    def set_action(self, action):
        self.action = action
        self.frame = 0
    
    def update(self, movent = (0, 0)):
        x = self.pos[0] + movent[0]
        y = self.pos[1] + movent[1]
        self.pos = (x, y)
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0

    def get_image(self):
        return self.images[self.action][int(self.frame / self.size_frame)]
    
    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.get_image(), self.flip, False), (self.pos[0] + offset[0], self.pos[1] + offset[1]))

    def run_sound(self):
        if (self.sound != None):
            self.sound.set_volume(self.volume)
            self.sound.play()

    
