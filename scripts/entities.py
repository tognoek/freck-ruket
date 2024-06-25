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
        return pygame.Rect(self.pos[0], self.pos[1], self.get_image().get_width(), self.get_image().get_height())
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.frame = 0
    
    def check_collisions(self):
        if all(value == False for value in self.collisions.values()):
            return False
        else:
            return True
    def update(self, other, movent = (0, 0), collision = False):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        if other is None:
            other = []
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0

        self.pos = (self.pos[0] + int(movent[0]), self.pos[1])
        entity_rect = self.rect()
        for i in other:

            if collision:
                check, pos_mask = self.collision_mask(i)
            else:
                check, pos_mask = self.collision_rect(i)

            if check:
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

            if collision:
                check, pos_mask = self.collision_mask(i)
            else:
                check, pos_mask = self.collision_rect(i)
            if check:
                if movent[1] > 0:
                    entity_rect.bottom = i.rect().top
                    self.collisions["down"] = True
                if movent[1] < 0:
                    entity_rect.top = i.rect().bottom + pos_mask[1]
                    self.collisions["up"] = True
                
                self.pos = (self.pos[0], entity_rect.y)


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
    
    

class Map(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)
        
    
class Character(Entity):

    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame=5, type_entity=1, speed = (0, 0)):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)
        self.jump = True
        self.double_jump = True
        self.speed = speed

    def update(self, other):

        pos_old = self.pos

        super().update(other, self.speed)
        
        if self.action == "Idle" or self.action == "Run":
            self.jump = False
    
        if pos_old == self.pos and self.check_collisions():
            self.set_action("Idle")

        if pos_old[0] != self.pos[0] and self.collisions["down"]:
            self.set_action("Run")

        if pos_old[1] > self.pos[1] and not self.jump and self.speed[1] < 0:
            self.set_action("Jump")
            self.jump = True
            self.double_jump = False

        if pos_old[1] < self.pos[1]:
            self.set_action("Fall")

        if self.action == "Fall" and self.speed[1] < 0 and not self.double_jump:
            self.set_action("Double Jump")
            self.double_jump = True

        self.animation()

    def update_speed(self):
        self.speed = (self.speed[0], self.speed[1] + 0.4)
        if self.speed[1] > 5:
            self.speed = (self.speed[0], 5)

        if self.collisions["up"]:
            self.speed = (self.speed[0], 0)

        if self.speed[0] > 0:
            self.flip = False
        if self.speed[0] < 0:
            self.flip = True


    def speed_x(self, x):
        self.speed = (x, self.speed[1])

    def speed_y(self, y):
        if y < 0:
            if not self.jump:
                self.speed = (self.speed[0], y)
            if not self.double_jump and self.action == "Fall":
                self.speed = (self.speed[0], y)

    def reset_speed(self, e_type):
        if e_type:
            self.speed_x(0)
        else:
            self.speed_y(0)

