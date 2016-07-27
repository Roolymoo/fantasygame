from collections import deque

import pygame
from pygame import display
from pygame.locals import QUIT

from background import Background


def update_display(update_queue):
    """(deque) -> NoneType
    Updates the display with Rect's given in update_queue, and clears update_queue. Specifically, for each such Rect,
    updates the display/screen only within that Rect."""
    display.update(update_queue)

    update_queue.clear()


if __name__ == "__main__":
    # init
    running = True

    pygame.init()

    # allow key repeating for holding them down
    # i just pulled these values off internets
    KEY_DELAY = 1
    KEY_INTERVAL = 50
    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)

    fps_clock = pygame.time.Clock()
    FPS = 30

    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700

    # Mouse button codes (pygame specific)
    LEFT_MB = 1

    # colours
    WHITE = (255, 255, 255)

    # Art
    
    # music
    
    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # put desks, garbage cans, etc in here
    env_obj_col = deque()

    # put the ai stuff in here, but not player
    monster_col = deque()

    # init rendering
    # Queue of rects specifying areas of display to update
    update_queue = deque()

    background = Background(WINDOW_WIDTH, WINDOW_HEIGHT, WHITE)
    background.render(screen, update_queue)

    # Force update display (generally handled at end of main loop below)
    update_display(update_queue)

    while running:
        # input loop
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        update_display(update_queue)

        fps_clock.tick(FPS)
