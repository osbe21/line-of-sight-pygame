import pygame as pg
import math


class Turret:
    def __init__(self, position, angle_deg, max_distance, max_angle_deg):
        self.position = position
        self.angle = angle_deg
        self.max_distance = max_distance
        self.max_angle = max_angle_deg

        self.stand = pg.image.load("sprites/turret_stand.png").convert_alpha()
        self.gun = pg.image.load("sprites/turret.png").convert_alpha()

    def can_detect_player(self):
        to_player = player_pos - self.position

        # Too far away?
        if to_player.length() > self.max_distance:
            return False

        # Direction turret is facing as a unit vector
        turret_direction = pg.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle)))

        # Angle between turret's direction and direction to player
        angle_diff = turret_direction.angle_to(to_player)

        if abs(angle_diff) > 180:
            angle_diff = abs(angle_diff) - 360

        if abs(angle_diff) > self.max_angle / 2:
            return False

        # Check if any obstacle blocks the view
        for _, rect in obstacles:
            if rect.clipline(self.position, player_pos):
                return False

        return True

    def update_rotation(self):
        if self.can_detect_player():
            # Calculate angle from turret to player
            direction = player_pos - self.position
            self.angle = -math.degrees(math.atan2(direction.y, direction.x))
    
    def draw(self, screen):
        self.draw_fov_cone(screen)

        screen.blit(self.stand, self.stand.get_rect(center=self.position))
        rotated_gun = pg.transform.rotate(self.gun, self.angle)
        screen.blit(rotated_gun, rotated_gun.get_rect(center=self.position))

    def draw_fov_cone(self, screen):
        cone_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

        start_angle = self.angle - self.max_angle/2
        stop_angle = self.angle + self.max_angle/2

        points = [self.position]
        for angle in range(math.floor(start_angle), math.ceil(stop_angle)):
            vec = pg.Vector2.from_polar((self.max_distance, -angle))
            points.append(self.position + vec)
        
        pg.draw.polygon(cone_surface, (255, 0, 0, 80), points)

        screen.blit(cone_surface, (0, 0))


pg.init()
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
FPS = 60

player = pg.image.load("sprites/player.png").convert_alpha()
player_pos = pg.Vector2(WIDTH // 2, HEIGHT // 2)
player_rotation = 0

obstacles = []
turret_1 = Turret(position=(200, 200), angle_deg=0, max_distance=250, max_angle_deg=90)
turret_2 = Turret(position=(550, 200), angle_deg=270, max_distance=250, max_angle_deg=90)


def create_obstacle(pos):
    image = pg.image.load("sprites/crate.png").convert_alpha()
    rect = image.get_rect(center=pos)
    obstacles.append((image, rect))

def get_player_position_and_rotation():
    speed = 3.5

    keys = pg.key.get_pressed()

    direction = pg.Vector2(keys[pg.K_d] - keys[pg.K_a], keys[pg.K_s] - keys[pg.K_w])

    if direction.length() > 0:
        new_pos = player_pos + direction.normalize() * speed
        new_rot = -math.degrees(math.atan2(direction.y, direction.x))

        return (new_pos, new_rot)
    
    return (player_pos, player_rotation)


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            create_obstacle(event.pos)

    player_pos, player_rotation = get_player_position_and_rotation()
    turret_1.update_rotation()
    turret_2.update_rotation()

    screen.fill("#339131")

    screen.blits(obstacles)

    rotated_player = pg.transform.rotate(player, player_rotation)
    rotated_rect = rotated_player.get_rect(center=player_pos)
    screen.blit(rotated_player, rotated_rect)
    
    turret_1.draw(screen)
    turret_2.draw(screen)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
