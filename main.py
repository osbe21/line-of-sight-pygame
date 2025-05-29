import pygame


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Line Of Sight Demo")

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic

    screen.fill((0, 0, 0))

    # Draw everything

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
