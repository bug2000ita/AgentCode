"""Mini Doom demo using pygame with textured walls."""

from __future__ import annotations

import math
import sys

import pygame


MAP = [
    "##########",
    "#........#",
    "#..##....#",
    "#........#",
    "##########",
]

FOV = math.pi / 3
DEPTH = 16
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


def create_ball_texture(size: int = 64) -> pygame.Surface:
    """Return a red ball texture as a pygame surface."""
    surf = pygame.Surface((size, size))
    background = (40, 20, 20)
    ball_color = (255, 0, 0)
    surf.fill(background)
    radius = size // 8
    for y in range(radius, size, radius * 2):
        offset = (y // (radius * 2) % 2) * radius
        for x in range(radius - offset, size, radius * 2):
            pygame.draw.circle(surf, ball_color, (x, y), radius)
    return surf.convert()


def create_bear_texture(size: int = 64) -> pygame.Surface:
    """Return a simple baby bear texture."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    brown = (150, 110, 60)
    black = (0, 0, 0)

    ear_r = size // 6
    face_r = size // 3
    pygame.draw.circle(surf, brown, (size // 3, size // 3), ear_r)
    pygame.draw.circle(surf, brown, (size * 2 // 3, size // 3), ear_r)
    pygame.draw.circle(surf, brown, (size // 2, size // 2 + ear_r // 2), face_r)
    eye_r = max(1, size // 32)
    eye_y = size // 2
    pygame.draw.circle(surf, black, (size // 2 - ear_r // 2, eye_y), eye_r)
    pygame.draw.circle(surf, black, (size // 2 + ear_r // 2, eye_y), eye_r)
    pygame.draw.circle(surf, black, (size // 2, size // 2 + ear_r), eye_r + 1)
    return surf.convert_alpha()


def cast_ray(px: float, py: float, angle: float) -> tuple[float, float]:
    """Return distance to wall and horizontal texture coordinate."""
    step_size = 0.05
    distance = 0.0
    hit = False
    tex_x = 0.0
    hit_x = px
    hit_y = py
    while not hit and distance < DEPTH:
        distance += step_size
        hit_x = px + math.cos(angle) * distance
        hit_y = py + math.sin(angle) * distance
        cell_x = int(hit_x)
        cell_y = int(hit_y)
        if (
            cell_x < 0
            or cell_x >= len(MAP[0])
            or cell_y < 0
            or cell_y >= len(MAP)
        ):
            hit = True
            distance = DEPTH
        elif MAP[cell_y][cell_x] == "#":
            hit = True
            x_offset = hit_x - cell_x
            y_offset = hit_y - cell_y
            if abs(x_offset - 0.5) > abs(y_offset - 0.5):
                tex_x = y_offset
            else:
                tex_x = x_offset
    return distance, tex_x


def game_loop() -> None:
    """Run the textured raycasting demo."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    texture = create_ball_texture()
    bear_texture = create_bear_texture()

    enemy_pos = [5.5, 2.5]

    # List of active water "splashes" drawn when the player shoots.
    # Each entry is a countdown of frames to keep the splash visible.
    splashes: list[int] = []

    px, py = 3.0, 3.0
    angle = 0.0
    move_speed = 0.1
    rot_speed = 0.05

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Spawn a new splash when the player shoots water.
                splashes.append(10)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            angle -= rot_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            angle += rot_speed
        dx = math.cos(angle) * move_speed
        dy = math.sin(angle) * move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            nx, ny = px + dx, py + dy
            cell_x, cell_y = int(nx), int(ny)
            if (
                0 <= cell_x < len(MAP[0])
                and 0 <= cell_y < len(MAP)
                and MAP[cell_y][cell_x] == "."
            ):
                px, py = nx, ny
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            nx, ny = px - dx, py - dy
            cell_x, cell_y = int(nx), int(ny)
            if (
                0 <= cell_x < len(MAP[0])
                and 0 <= cell_y < len(MAP)
                and MAP[cell_y][cell_x] == "."
            ):
                px, py = nx, ny

        # Check collision with the enemy
        if math.hypot(px - enemy_pos[0], py - enemy_pos[1]) < 0.5:
            print("You were mauled by a baby bear!")
            running = False

        screen.fill((0, 0, 0))

        for x in range(SCREEN_WIDTH):
            ray_angle = angle - FOV / 2 + (x / SCREEN_WIDTH) * FOV
            distance, tex_x = cast_ray(px, py, ray_angle)
            wall_height = SCREEN_HEIGHT / max(distance, 0.0001)
            start = int(SCREEN_HEIGHT / 2 - wall_height / 2)
            end = int(SCREEN_HEIGHT / 2 + wall_height / 2)
            tex_column = int(tex_x * texture.get_width())
            column = texture.subsurface(pygame.Rect(tex_column, 0, 1, texture.get_height()))
            column = pygame.transform.scale(column, (1, end - start))
            screen.blit(column, (x, start))

        # Draw the baby bear enemy if it's visible
        dx = enemy_pos[0] - px
        dy = enemy_pos[1] - py
        dist = math.hypot(dx, dy)
        angle_to_enemy = math.atan2(dy, dx)
        rel_angle = (angle_to_enemy - angle + math.pi) % (2 * math.pi) - math.pi
        if abs(rel_angle) < FOV / 2:
            wall_dist, _ = cast_ray(px, py, angle_to_enemy)
            if dist < wall_dist:
                size = SCREEN_HEIGHT / max(dist, 0.0001)
                sprite = pygame.transform.scale(
                    bear_texture, (int(size), int(size))
                )
                screen_x = SCREEN_WIDTH / 2 - (rel_angle / (FOV / 2)) * (
                    SCREEN_WIDTH / 2
                )
                screen.blit(
                    sprite,
                    (screen_x - size / 2, SCREEN_HEIGHT / 2 - size / 2),
                )

        # Draw active water splashes at the center of the screen.
        for i in range(len(splashes)):
            pygame.draw.circle(
                screen,
                (0, 150, 255),
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                10,
            )
            splashes[i] -= 1
        splashes = [s for s in splashes if s > 0]

        # Draw a simple water pistol overlay so the player sees it in
        # first-person view. It stays anchored to the bottom right of the
        # screen, giving the illusion of a held weapon.
        handle = pygame.Rect(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 50, 25, 40)
        body = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 90, 25)
        barrel = pygame.Rect(SCREEN_WIDTH - 65, SCREEN_HEIGHT - 85, 60, 15)
        pygame.draw.rect(screen, (40, 40, 40), body)
        pygame.draw.rect(screen, (0, 200, 255), barrel)
        pygame.draw.rect(screen, (70, 70, 70), handle)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main() -> None:
    try:
        game_loop()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
