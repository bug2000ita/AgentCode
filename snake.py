import curses
import random


def main() -> None:
    """Run the snake game using the curses interface."""
    stdscr = curses.initscr()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    win = curses.newwin(h, w, 0, 0)
    win.keypad(True)
    win.timeout(100)

    snk_x = w // 4
    snk_y = h // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2],
    ]
    food = [h // 2, w // 2]
    win.addch(food[0], food[1], curses.ACS_PI)

    key = curses.KEY_RIGHT

    try:
        while True:
            next_key = win.getch()
            key = key if next_key == -1 else next_key

            if key not in [
                curses.KEY_RIGHT,
                curses.KEY_LEFT,
                curses.KEY_DOWN,
                curses.KEY_UP,
            ]:
                key = key

            head = [snake[0][0], snake[0][1]]
            if key == curses.KEY_RIGHT:
                head[1] += 1
            if key == curses.KEY_LEFT:
                head[1] -= 1
            if key == curses.KEY_UP:
                head[0] -= 1
            if key == curses.KEY_DOWN:
                head[0] += 1
            snake.insert(0, head)

            if head[0] in [0, h] or head[1] in [0, w] or head in snake[1:]:
                curses.endwin()
                return

            if head == food:
                food = None
                while food is None:
                    nf = [random.randint(1, h - 2), random.randint(1, w - 2)]
                    food = nf if nf not in snake else None
                win.addch(food[0], food[1], curses.ACS_PI)
            else:
                tail = snake.pop()
                win.addch(tail[0], tail[1], " ")

            win.addch(head[0], head[1], curses.ACS_CKBOARD)

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == "__main__":
    main()
