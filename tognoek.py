import pygame

pygame.init()

screen = pygame.display.set_mode((700, 500))

display = pygame.Surface((350, 250))

pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

pos = [50, 120]

offset = [0, 0]

go = None

running = True

while running:

    if go != None:
        if go:
            pos[0] -= 5
        else:
            pos[0] += 5

    offset[0] += (350 / 2 - pos[0] - offset[0]) / 30
    offset[0] = int(offset[0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                go = True
            elif event.key == pygame.K_RIGHT:
                go = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                go = None

    display.fill((0, 0, 0))
    pygame.draw.circle(display, (55, 0, 0), (-250 + offset[0], 120), 10)
    pygame.draw.circle(display, (55, 0, 0), (700 + offset[0], 120), 10)
    pygame.draw.circle(display, (55, 0, 0), (70 + offset[0], 120), 10)
    pygame.draw.circle(display, (55, 0, 0), (170 + offset[0], 120), 10)
    pygame.draw.circle(display, (255, 0, 0), (pos[0] + offset[0], pos[1] + offset[1]), 10)
    screen.blit(pygame.transform.scale(display, (700, 500)), (0, 0))
    print(pos)
    pygame.display.update()
    clock.tick(60)

pygame.quit()