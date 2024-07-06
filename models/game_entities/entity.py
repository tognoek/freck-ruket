import pygame, random

class Entity:

    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1):
        self.name = name
        self.pos = pos
        self.images = images
        self.sound = sound
        self.flip = flip
        self.volume = volume
        self.frame = frame
        self.action = 'Idle'
        self.size_frame = size_frame
        self.type_entity = type_entity
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.other_collisions_bottom = None

    def copy(self):
        return Entity(self.name, self.x, self.y, self.images, self.sound, self.volume, self.frame)
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.get_image().get_width(), self.get_image().get_height())
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.frame = 0
            self.off_pos = (3, 5)
    
    def check_collisions(self):
        if all(value == False for value in self.collisions.values()):
            return False
        else:
            return True
    def update(self):
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0
        


    def animation(self):
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0


    def get_image(self) -> pygame.Surface:
        return self.images[self.action][int(self.frame / self.size_frame)]
    
    def get_image_default(self) -> pygame.Surface:
        return self.images[self.action][0]
    
    def get_mask(self) -> pygame.Surface:
        mask_surface = pygame.mask.from_surface(self.get_image())
        return pygame.mask.Mask.to_surface(mask_surface)
    
    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.get_image(), self.flip, False), (int(self.pos[0] + offset[0]), int(self.pos[1] + offset[1])))

    def run_sound(self):
        if (self.sound != None):
            self.sound.set_volume(self.volume)
            self.sound.play()

    def get_pos(self) -> tuple:
        return self.pos
    
    def collision_mask(self, other, default=False):
        if default:
            entity_1 = pygame.mask.from_surface(self.get_image_default())
        else:
            entity_1 = pygame.mask.from_surface(self.get_image())
        entity_2 = pygame.mask.from_surface(other.get_image())
        offset_mask = (-self.get_pos()[0] + other.get_pos()[0], -self.get_pos()[1] + other.get_pos()[1])
        overlap_mask = entity_1.overlap(entity_2, offset_mask)
        if overlap_mask:
            return True, overlap_mask
        return False, (0, 0)
    
    def collision_rect(self, other):
        rect_1 = self.rect()
        rect_2 = other.rect()
        if rect_1.colliderect(rect_2):
            return True, (0, 0)
        return False, (0, 0)
    
    def collision_tognoek(self, other : pygame.Rect, point = (0, 0)):
        rect_1 = pygame.Rect((self.get_pos()[0] + point[0], self.get_pos()[1] + point[1]), (1, 1))
        if rect_1.colliderect(other):
            return True
        return False
  