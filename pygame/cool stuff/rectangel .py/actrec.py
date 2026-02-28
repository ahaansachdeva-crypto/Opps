import pygame

pygame.init()
screen = pygame.display.set_mode((130, 530))
screen.fill((100,210,34))
done = False


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        pygame.draw.rect(screen, (111, 25, 55), pygame.Rect(130, 530, 100 ,260))
        pygame.display.flip()