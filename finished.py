import pygame as pg
from random import choice  # Used for making background
from math import sin, cos, atan2, radians, degrees


class Turret:
    def __init__(self, position, angle_deg, max_distance, max_angle_deg):
        self.position = position
        self.angle = angle_deg
        self.max_distance = max_distance
        self.max_angle = max_angle_deg

        self.stand = pg.image.load("sprites/turret_stand.png")
        self.gun = pg.image.load("sprites/turret.png")

    def can_detect_player(self, player_rect, obstacles):
        to_player = pg.Vector2(player_rect.center) - self.position

        # Too far away?
        if to_player.length() > self.max_distance:
            return False

        # Direction turret is facing as a unit vector
        turret_direction = pg.Vector2(cos(radians(self.angle)), -sin(radians(self.angle)))

        # Angle between turret's direction and direction to player
        angle_diff = turret_direction.angle_to(to_player)

        if abs(angle_diff) > 180:
            angle_diff = abs(angle_diff) - 360

        if abs(angle_diff) > self.max_angle / 2:
            return False

        # Check if any obstacle blocks the view
        for _, rect in obstacles:
            if rect.clipline(self.position, player_rect.center):
                return False

        return True
    
    def draw(self, screen):
        screen.blit(self.stand, self.stand.get_rect(center=self.position))
        rotated_gun = pg.transform.rotate(self.gun, self.angle)
        screen.blit(rotated_gun, rotated_gun.get_rect(center=self.position))


pg.init()
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
FPS = 60

player = pg.image.load("sprites/player.png")
player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))

background = pg.Surface((WIDTH, HEIGHT))
obstacles = []
turret = Turret(position=(250, 200), angle_deg=0, max_distance=400, max_angle_deg=90)


def create_obstacle(pos):
    image = pg.image.load("sprites/crate.png")
    rect = image.get_rect(center=pos)
    obstacles.append((image, rect))

    obstacles.append((image, rect))

def update_player_position():
    speed = 3.5

    keys = pg.key.get_pressed()

    direction = pg.Vector2(keys[pg.K_d] - keys[pg.K_a], keys[pg.K_s] - keys[pg.K_w])

    if direction.length() > 0:
        player_rect.move_ip(direction.normalize() * speed)

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
        if event.type == pg.MOUSEBUTTONDOWN:
            create_obstacle(event.pos)

    update_player_position()

    if turret.can_detect_player(player_rect, obstacles):
        # Calculate angle from turret to player
        direction = pg.Vector2(player_rect.center) - turret.position
        turret.angle = -degrees(atan2(direction.y, direction.x))

    screen.fill((0, 0, 0))

    # Draw everything
    screen.blit(background, (0, 0))
    turret.draw(screen)
    screen.blit(player, player_rect)
    screen.blits(obstacles)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
