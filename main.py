import pygame as pg
from random import choice  # Used for making background


pg.init()
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
FPS = 60

background = pg.Surface((WIDTH, HEIGHT))


def create_background():
    tiles = [pg.image.load(f"sprites/tile_0{i}.png").convert() for i in range(1, 5)]
    tile_size = tiles[0].get_width()

    for x in range(0, WIDTH, tile_size):
        for y in range(0, HEIGHT, tile_size):
            background.blit(choice(tiles), (x, y))


create_background()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.blit(background, (0, 0))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
