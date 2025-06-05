import curses
import math

# Simple map layout: '#' walls, '.' empty space
MAP = [
    "##########",
    "#........#",
    "#..##....#",
    "#........#",
    "##########",
]

FOV = math.pi / 3  # Field of view (~60 degrees)
DEPTH = 16


def game_loop(stdscr) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    h, w = stdscr.getmaxyx()
    player_x, player_y = 3.0, 3.0
    player_angle = 0.0
    move_speed = 0.1
    rot_speed = 0.1

    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
        if key in (curses.KEY_LEFT, ord("a")):
            player_angle -= rot_speed
        if key in (curses.KEY_RIGHT, ord("d")):
            player_angle += rot_speed
        dx = math.cos(player_angle) * move_speed
        dy = math.sin(player_angle) * move_speed
        if key in (curses.KEY_UP, ord("w")):
            if MAP[int(player_y + dy)][int(player_x + dx)] == '.':
                player_x += dx
                player_y += dy
        if key in (curses.KEY_DOWN, ord("s")):
            if MAP[int(player_y - dy)][int(player_x - dx)] == '.':
                player_x -= dx
                player_y -= dy

        for x in range(w):
            ray_angle = (player_angle - FOV/2.0) + (x / w) * FOV
            step_size = 0.05
            distance_to_wall = 0.0
            hit_wall = False

            while not hit_wall and distance_to_wall < DEPTH:
                distance_to_wall += step_size
                test_x = int(player_x + math.cos(ray_angle) * distance_to_wall)
                test_y = int(player_y + math.sin(ray_angle) * distance_to_wall)
                if (test_x < 0 or test_x >= len(MAP[0]) or
                        test_y < 0 or test_y >= len(MAP)):
                    hit_wall = True
                    distance_to_wall = DEPTH
                elif MAP[test_y][test_x] == '#':
                    hit_wall = True

            ceiling = int(h / 2 - h / distance_to_wall)
            floor = h - ceiling
            if distance_to_wall <= DEPTH / 4.0:
                shade = '#'
            elif distance_to_wall < DEPTH / 3.0:
                shade = 'O'
            elif distance_to_wall < DEPTH / 2.0:
                shade = 'x'
            elif distance_to_wall < DEPTH:
                shade = '.'
            else:
                shade = ' '

            for y in range(h):
                if y < ceiling:
                    char = ' '
                elif y > ceiling and y <= floor:
                    char = shade
                else:
                    char = '.'
                try:
                    stdscr.addch(y, x, char)
                except curses.error:
                    pass
        stdscr.refresh()


def main() -> None:
    curses.wrapper(game_loop)


if __name__ == "__main__":
    main()
