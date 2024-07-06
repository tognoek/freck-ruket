import pygame

from models.game_entities.entity import Entity

    
class Character(Entity):

    def __init__(self, name, pos, images, sound, flip, volume, frame, data, size_frame=5, type_entity=1, speed = (0, 0)):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity)
        self.count_jump = 0
        self.speed = speed
        self.data = data
        self.wall_jump = False

    def render(self, surface, offset=(0, 0), point = True):
        super().render(surface, offset)
        if point:
            pygame.draw.circle(surface, (255, 0, 0), (self.rect().x + offset[0], self.rect().y + offset[1]), 1)
            for i in self.data[self.action]:
                pygame.draw.circle(surface, (255, 0, 0), (self.rect().x + i[0] + offset[0], self.rect().y + i[1] + offset[1]), 1)

    def hit(self):
        print("Hit")


    def update(self, other, collision = "tognoek"):

        pos_old = self.pos

        if self.type_entity == 3:
            self.hit()
            return

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
                if i.type_entity == 1:
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
                if i.type_entity == 1:
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
                
                if i.type_entity == 2:
                    if self.speed[1] > 0:
                        if self.collision_tognoek(i, self.data[self.action][4]):
                            if self.data[self.action][4][1] + self.get_pos()[1] - other_rect.top <= self.speed[1]:
                                entity_rect.bottom = other_rect.top + (entity_rect.height - self.data[self.action][4][1]) - 1
                                self.collisions["down"] = True
                        if self.collision_tognoek(i, self.data[self.action][5]):
                            if self.data[self.action][5][1] + self.get_pos()[1] - other_rect.top <= self.speed[1]:
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
        if self.collisions["down"]:
            self.count_jump = 0
            self.wall_jump = False
            if pos_old == self.pos:
                self.set_action("Idle")
                self.speed = (0, 5)
            else:
                self.set_action("Run")

        if not self.wall_jump:

            if self.count_jump == 2:
                self.set_action("Double Jump")

            if self.count_jump == 1:
                self.set_action("Jump")

            if pos_old[1] < self.pos[1]:
                self.set_action("Fall")

        if not self.collisions["down"] and self.speed[1] > 0:
            if self.collisions["right"] or self.collisions["left"] or self.wall_jump:
                self.set_action("Wall Jump")
                self.wall_jump = True
                if self.flip:
                    self.speed = (-3, 1)
                else:
                    self.speed = (3, 1)
            if not self.collisions["right"] and not self.collisions["left"] and self.wall_jump:
                self.set_action("Fall")
                self.wall_jump = False
                self.speed = (0, 4)
        

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
        if not self.wall_jump:
            self.speed = (x, self.speed[1])
        else:
            if x * self.speed[0] < 0:
                self.speed = (x, -5)
                self.wall_jump = False
                self.count_jump = 1

    def speed_y(self, y):
        self.count_jump = self.count_jump + 1
        if self.count_jump < 3 and not self.wall_jump:
            self.speed = (self.speed[0], y)

    def reset_speed(self, e_type):
        if e_type:
            self.speed_x(0)
        else:
            self.speed_y(0)
