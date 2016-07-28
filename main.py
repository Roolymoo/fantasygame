from collections import deque

import pygame
from pygame import display, transform
from pygame.locals import QUIT

from background import Background
from fileloader import get_level, load_img
from object import Object


def _get_level_dict():
    """(NoneType) -> NoneType
    Returns formatted dict for parsing levels being loaded."""
    return {"type": None, "img": None, "x": None, "y": None, "w": None, "h": None, "flip": None, "rotate": None,
            "scale": None, "colour": None}


def _parse_colour(raw_colour):
    """(str) -> tuple
    Takes the str of the usual tuple colour format, and returns the usual tuple format."""
    return tuple(int(i) for i in raw_colour.strip("()").split(","))


def update_display(update_queue):
    """(deque) -> NoneType
    Updates the display with Rect's given in update_queue, and clears update_queue. Specifically, for each such Rect,
    updates the display/screen only within that Rect."""
    display.update(update_queue)

    update_queue.clear()


def load_level(level_n):
    """(str) -> NoneType
    Loads level information from level_n into variables declared in __main__."""
    with open(get_level(level_n)) as file:
        line = file.readline()
        while line:
            if line[0] == "#":
                # a comment, ignore
                line = file.readline()
                continue

            data = _get_level_dict()
            # parse data into raw pieces based on type parameter
            for raw_data in line.split():
                id, val = raw_data.split("=")
                data.update({id: val})

            # parse raw pieces corresponding to type parameter
            if data["type"] == "object":
                obj = Object(int(data["x"]), int(data["y"]), int(data["w"]), int(data["h"]))
                env_obj_col.append(obj)
            elif data["type"] == "bkgrd":
                obj = Object(int(data["x"]), int(data["y"]), int(data["w"]), int(data["h"]))
                if data["colour"]:
                    obj.colour = _parse_colour(data["colour"])
                background.obj_col.append(obj)

            # resolve additional parameters, if any
            if data["img"]:
                obj.img = load_img(data["img"])
            if data["flip"]:
                horiz, vert = None, None
                args = data["flip"].strip("()").split(",")
                if args[0] == "false":
                    horiz = False
                else:
                    horiz = True
                if args[1] == "false":
                    vert = False
                else:
                    vert = True

                obj.img = transform.flip(obj.img, horiz, vert)
            if data["rotate"]:
                obj.img = transform.rotate(obj.img, int(data["rotate"].split("=")[-1]))
            if data["scale"]:
                obj.img = transform.scale(obj.img, tuple(int(i) for i in data["scale"].strip("()").split(",")))

            # render obj if it has an image
            if obj.img:
                obj.render(screen, update_queue)

            line = file.readline()


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

    # player
    player = None

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
