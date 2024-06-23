import pygame
from ENV import IMAGE_SIZE

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

    def copy(self):
        return Entity(self.name, self.x, self.y, self.images, self.sound, self.volume, self.frame)
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.images[self.action][0].get_width(), self.images[self.action][0].get_height())
    
    def set_action(self, action):
        self.action = action
        self.frame = 0
    
    def update(self, other, movent = (0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        if other is None:
            other = []
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0

        self.pos = (self.pos[0] + int(movent[0]), self.pos[1])
        entity_rect = self.rect()
        for i in other:
            if self.collision_mask(i):
                if movent[0] > 0:
                    entity_rect.right = i.rect().left
                    self.collisions["right"] = True
                if movent[0] < 0:
                    entity_rect.left = i.rect().right
                    self.collisions["left"] = True
                
                self.pos = (entity_rect.x, self.pos[1])
        
        self.pos = (self.pos[0], self.pos[1] + int(movent[1]))
        entity_rect = self.rect()
        for i in other:
            if self.collision_mask(i):
                if movent[1] > 0:
                    entity_rect.bottom = i.rect().top
                    self.collisions["down"] = True
                if movent[1] < 0:
                    entity_rect.top = i.rect().bottom
                    self.collisions["up"] = True
                
                self.pos = (self.pos[0], entity_rect.y)

        self.animation()

    def animation(self):
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0


    def get_image(self) -> pygame.Surface:
        return self.images[self.action][int(self.frame / self.size_frame)]
    
    def get_mask(self) -> pygame.Surface:
        mask_surface = pygame.mask.from_surface(self.get_image())
        return pygame.mask.Mask.to_surface(mask_surface)
    
    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.get_image(), self.flip, False), (self.pos[0] + offset[0], self.pos[1] + offset[1]))

    def run_sound(self):
        if (self.sound != None):
            self.sound.set_volume(self.volume)
            self.sound.play()

    def get_pos(self) -> tuple:
        return self.pos
    
    def collision_mask(self, other):
        entity_1 = pygame.mask.from_surface(self.get_image())
        entity_2 = pygame.mask.from_surface(other.get_image())
        offset_mask = (self.get_pos()[0] - other.get_pos()[0], self.get_pos()[1] - other.get_pos()[1])
        if entity_1.overlap(entity_2, offset_mask):
            return True
        return None
    
    def collision_rect(self, other):
        rect_1 = self.rect()
        rect_2 = other.rect()
        if rect_1.colliderect(rect_2):
            return True
        return False
    
    

class Map(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)
        
    
class Character(Entity):

    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame=5, type_entity=1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)


