import pygame, random

class Dustparticle():
    def __init__(self, pos, size, color, speed, life_time, max_size=2):
        self.pos = pos
        self.size = size
        self.color = color
        self.speed = speed
        self.life_time = life_time
        self.max_size = max_size

    def update(self):
        self.life_time -= 1
        self.pos = (self.pos[0] + self.speed[0], self.pos[1] + self.speed[1])
        self.size = self.size + 0.3
        if self.size > self.max_size:
            self.size = self.max_size

    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def is_die(self):
        return self.life_time <= 0

    def render(self, surface, offset):
        pygame.draw.circle(surface, self.color, (self.pos[0] + offset[0], self.pos[1] + offset[1]), int(self.size))
        radius = self.size + 1
        surface.blit(self.circle_surf(radius, (20, 20, 60)), (int(self.pos[0] + offset[0] - radius), int(self.pos[1] + offset[1] - radius)), special_flags=pygame.BLEND_RGB_ADD)

    def create_dust_particles_jump(pos, num_particles=5):
        particles = []
        for _ in range(num_particles):
            speed = [random.uniform(-1, 1), random.uniform(0.5, 1)]
            life_time = random.randint(10, 20)
            color = (200, 200, 200)
            particle = Dustparticle(pos, 1.5, color, speed, life_time)
            particles.append(particle)
        return particles
    
    def create_dust_particles(pos, num_particles=5, size = (16, 16), r = 1, max_size = 2):
        particles = []
        for _ in range(num_particles):
            speed = [random.uniform(-1, 1), random.uniform(0.5, 1)]
            life_time = random.randint(10, 20)
            pos_r = (pos[0] + random.randint(0, size[0]), pos[1])
            color = (200, 200, 200)
            particle = Dustparticle(pos_r, r, color, speed, life_time, max_size)
            particles.append(particle)
        return particles
    
    def create_dust_particles_fly(pos, num_particles=5, size = (16, 16), r = 1, life = (10, 20)):
        particles = []
        for _ in range(num_particles):
            speed = [random.uniform(-0.5, 0.5), random.uniform(-3, -1)]
            life_time = random.randint(life[0], life[1])
            pos_r = (pos[0] + random.randint(0, size[0]), pos[1])
            color = (200, 200, 200)
            particle = Dustparticle(pos_r, r, color, speed, life_time)
            particles.append(particle)
        return particles
        
