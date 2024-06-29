import pygame

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
    
    

class Map(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)

class Block(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)
        
    
class Character(Entity):

    def __init__(self, name, pos, images, sound, flip, volume, frame, data, size_frame=5, type_entity=1, speed = (0, 0)):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)
        self.count_jump = 0
        self.speed = speed
        self.data = data

    def render(self, surface, offset=(0, 0), point = False):
        super().render(surface, offset)
        if point:
            pygame.draw.circle(surface, (255, 0, 0), (self.rect().x, self.rect().y), 1)
            for i in self.data[self.action]:
                pygame.draw.circle(surface, (255, 0, 0), (self.rect().x + i[0], self.rect().y + i[1]), 1)

    


    def update(self, other, collision = "tognoek"):

        pos_old = self.pos

        super().update()
        
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        if other is None:
            other = []
        dot = pygame.Surface((1, 1))
        dot.fill((255, 255, 255))

        if collision == "tognoek":        
            self.pos = (self.pos[0] + self.speed[0], self.pos[1])
            entity_rect = self.rect()

            for i in other:
                other_rect = i.rect()
                if self.speed[0] > 0:
                    if self.collision_tognoek(i, self.data[self.action][2]):
                        entity_rect.right = other_rect.left + (entity_rect.width - self.data[self.action][2][0]) - 1
                        self.collisions["right"] = True
                    if self.collision_tognoek(i, self.data[self.action][3]):
                        entity_rect.right = other_rect.left + (entity_rect.width - self.data[self.action][2][0]) - 1
                        self.collisions["right"] = True
                if self.speed[0] < 0:
                    if self.collision_tognoek(i, self.data[self.action][6]):
                        entity_rect.left = other_rect.right - self.data[self.action][6][0]
                        self.collisions["left"] = True
                    if self.collision_tognoek(i, self.data[self.action][7]):
                        entity_rect.left = other_rect.right - self.data[self.action][7][0]
                        self.collisions["left"] = True
                
                self.pos = (entity_rect.x, self.pos[1])

            self.pos = (self.pos[0], self.pos[1] + (self.speed[1]))
            entity_rect = self.rect()

            for i in other:
                other_rect = i.rect()
                if self.speed[1] < 0:
                    if self.collision_tognoek(i, self.data[self.action][0]):
                        entity_rect.top = other_rect.bottom - self.data[self.action][0][1]
                        self.collisions["up"] = True
                    if self.collision_tognoek(i, self.data[self.action][1]):
                        entity_rect.top = other_rect.bottom - self.data[self.action][1][1]
                        self.collisions["up"] = True
                if self.speed[1] > 0:
                    if self.collision_tognoek(i, self.data[self.action][4]):
                        entity_rect.bottom = other_rect.top + (entity_rect.height - self.data[self.action][4][1]) - 1
                        self.collisions["down"] = True
                    if self.collision_tognoek(i, self.data[self.action][5]):
                        entity_rect.bottom = other_rect.top + (entity_rect.height - self.data[self.action][5][1]) - 1
                        self.collisions["down"] = True

                self.pos = (self.pos[0], entity_rect.y)
                    

        else:
            self.pos = (self.pos[0] + self.speed[0], self.pos[1])
            entity_rect = self.rect()
            for i in other:

                if collision == "mask":
                    check, pos_mask = self.collision_mask(i, True)
                if collision == "rect":
                    check, pos_mask = self.collision_rect(i)

                if check:
                    self.tg = pos_mask
                    if self.speed[0] > 0:
                        entity_rect.right = i.rect().left
                        if collision == "mask":
                            entity_rect.right = i.rect().left + self.off_pos[0]
                        self.collisions["right"] = True
                    if self.speed[0] < 0:
                        entity_rect.left = i.rect().right
                        if collision == "mask":
                            entity_rect.left = i.rect().right - self.off_pos[1]
                        self.collisions["left"] = True
                    
                    self.pos = (entity_rect.x, self.pos[1])
            
            self.pos = (self.pos[0], self.pos[1] + (self.speed[1]))
            entity_rect = self.rect()
            for i in other:

                if collision == "mask":
                    check, pos_mask = self.collision_mask(i, True)
                if collision == "rect":
                    check, pos_mask = self.collision_rect(i)
                if check:
                    self.tg = pos_mask 
                    if self.speed[1] > 0:
                        entity_rect.bottom = i.rect().top
                        self.collisions["down"] = True
                    if self.speed[1] < 0:
                        entity_rect.top = i.rect().bottom + pos_mask[1]
                        self.collisions["up"] = True
                    
                    self.pos = (self.pos[0], entity_rect.y)
        self.check_action(pos_old)

        self.animation()

    def check_action(self, pos_old):
        if pos_old == self.pos and self.check_collisions():
            self.set_action("Idle")
            self.count_jump = 0

        if pos_old[0] != self.pos[0] and self.collisions["down"]:
            self.set_action("Run")
            self.count_jump = 0

        if self.count_jump == 2:
            self.set_action("Double Jump")

        if self.count_jump == 1:
            self.set_action("Jump")

        if pos_old[1] < self.pos[1]:
            self.set_action("Fall")
        

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
        self.count_jump = self.count_jump + 1
        if self.count_jump < 3:
            self.speed = (self.speed[0], y)

    def reset_speed(self, e_type):
        if e_type:
            self.speed_x(0)
        else:
            self.speed_y(0)

class String:
    def __init__(self, surface : pygame.Surface) -> None:
        self.surface = surface

    def create_text(self, text, color =(255, 255, 255), font = 18):
        font = pygame.font.Font(None, font)
        self.text = font.render(text, True, color)
    
    def render_edit(self, center = False):
        if center:
            pos = (self.surface.get_width() // 2 - self.text.get_width() // 2, self.surface.get_height() // 2 - self.text.get_height() // 2)
        self.surface.blit(self.text, pos)

    def render(self, text, pos = (0, 0), color =(255, 255, 255), font = 18, center = False):
        font = pygame.font.Font(None, font)
        text = font.render(text, True, color)
        if center:
            pos = (self.surface.get_width() // 2 - text.get_width() // 2, self.surface.get_height() // 2 - text.get_height() // 2)
        self.surface.blit(text, pos)

class Background:
    def __init__(self, images, frame_size = 2):
        self.frame_size = frame_size
        self.fram = 0
        self.images = images
        self.pos = (0, 0)

    def update(self):
        self.fram = self.fram + 1
        if self.fram > self.frame_size:
            self.fram = 0
            self.pos = (self.pos[0] - 1, 0)
            if self.pos[0] < -1 * self.images[self.name].get_width():
                self.pos = (0, 0)

    def create(self, name, size = (0, 0)):
        self.name = name
        self.image = pygame.Surface((size[0] + self.images[self.name].get_width() * 3,size[1] + self.images[self.name].get_height() * 3))
        for i in range(int(size[1] / self.images[name].get_width()) + 3):
            for t in range(int(size[0] / self.images[name].get_height()) + 3):
                self.image.blit(self.images[name], (t * self.images[name].get_height(), i * self.images[name].get_width()))

    def render(self, surface : pygame.Surface):
        self.update()
        surface.blit(self.image, self.pos)

class Button:
    def __init__(self, name, text, color_on, color_off, pos, size, image = None) -> None:
        self.name = name
        self.text_show = text
        self.color_on = color_on
        self.color_off = color_off
        self.pos = pos
        self.size = size
        self.type = False
        self.image = image
        self.name_render = self.text_show

    def set_name(self, name_acction = None):
        if name_acction is not None:
            self.name_render = name_acction
        else:
            self.name_render = self.text_show

    def set_type(self, pos = (0, 0), type_click = -1):
        if self.pos[0] <= pos[0] and self.pos[0] + self.size_button[0] >= pos[0]:
            if self.pos[1] <= pos[1] and self.pos[1] + self.size_button[1] >= pos[1]:
                self.type = not self.type
                if type_click == 1:
                    return True
                else:
                    return False

    def render(self, surface : pygame.Surface):
        font = pygame.font.Font(None, 18)
        if self.type:
            self.text = font.render(self.name_render, True, self.color_on)
        else:
            self.text = font.render(self.name_render, True, self.color_off)
        self.size_button = (self.text.get_width() + self.size[0] + 2, self.text.get_height() + self.size[1] + 2)
        background = pygame.Surface(self.size_button)
        background.fill((0, 0, 0))
        pygame.draw.rect(background, (255, 255, 255), (1, 1, self.size_button[0] - 2, self.size_button[1] - 2))
        pos_text = (background.get_width() // 2 - self.text.get_width() // 2, background.get_height() // 2 - self.text.get_height() // 2)
        background.blit(self.text, pos_text)
        surface.blit(background, self.pos)



