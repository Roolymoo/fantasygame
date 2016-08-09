from collections import deque

import pygame
from pygame import display, transform, Rect
from pygame.locals import QUIT, KEYUP, K_ESCAPE

from background import Background
from fileloader import get_level, load_img
from object import Object
from ai import Kobold


def _get_level_dict():
    """(NoneType) -> NoneType
    Returns formatted dict for parsing levels being loaded."""
    return {"type": None, "img": None, "x": None, "y": None, "w": None, "h": None, "flip": None, "rotate": None,
            "scale": None, "colour": None, "repeat": None, "rects": None}


def _parse_colour(raw_colour):
    """(str) -> tuple
    Takes the str of the usual tuple colour format, and returns the usual tuple format."""
    return tuple(int(i) for i in raw_colour.strip("()").split(","))


def _parse_rect(data):
    """(dict) -> Rect"""
    return Rect(int(data["x"]), int(data["y"]), int(data["w"]), int(data["h"]))


def _parse_rects(data):
    """(dict) -> list
    Parses the rect's in data (type rects), and returns this as a list."""
    return [Rect(*map(int, raw_rect.strip("()").split(","))) for raw_rect in data["rects"].split(".")]


def update_display(update_queue):
    """(deque) -> NoneType
    Updates the display with Rect's given in update_queue, and clears update_queue. Specifically, for each such Rect,
    updates the display/screen only within that Rect."""
    display.update(update_queue)

    update_queue.clear()


def _resolve_params(data, obj_col):
    """(dict, list) -> NoneType
    For each object in obj_col, resolve the non-type parameters on it, and render the object if applicable."""
    for obj in obj_col:
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

        obj.render(screen, update_queue)

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

            # store objects created to be dealt with when resolving additional parameters later
            obj_col = []

            data = _get_level_dict()
            # parse data into raw pieces based on type parameter
            for raw_data in line.split():
                id, val = raw_data.split("=")
                data.update({id: val})

            # parse raw pieces corresponding to type parameter
            if data["type"] == "object":
                # how many times and in what direction do we repeat this object
                if data["repeat"]:
                    direction, num = data["repeat"].strip("()").split(",")
                    num = int(num)
                else:
                    # dummy direction
                    direction = "right"
                    num = 1

                rect = _parse_rect(data)
                w, h = rect.w, rect.h
                for i in range(num):
                    rect_c = rect.copy()
                    if direction == "right":
                        rect_c.x += i * w
                    elif direction == "left":
                        rect_c.x -= i * w
                    elif direction == "up":
                        rect_c.y -= i * h
                    elif direction == "down":
                        rect_c.y += i * h

                    obj = Object(rect_c)

                    obj_col.append(obj)
                    env_obj_col.append(obj)
            elif data["type"] == "bkgrd":
                obj = Object(_parse_rect(data))
                if data["colour"]:
                    obj.colour = _parse_colour(data["colour"])

                obj_col.append(obj)
                background.obj_col.append(obj)
            elif data["type"] == "kobold":
                obj = Kobold(_parse_rect(data))
                obj_col.append(obj)
                ai_col.append(obj)
            elif data["type"] == "navmesh":
                navmesh_col.extend(_parse_rects(data))

            _resolve_params(data, obj_col)

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
    RED = (255, 0, 0)

    # Art
    
    # music
    
    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # player
    player = None
    # put desks, garbage cans, etc in here
    env_obj_col = deque()
    # put the ai stuff in here, but not player
    ai_col = deque()
    # rectangles that ai are only allowed to be in (e.g. for movement)
    navmesh_col = deque()

    # init rendering
    # Queue of rects specifying areas of display to update
    update_queue = deque()

    background = Background(WINDOW_WIDTH, WINDOW_HEIGHT, WHITE)
    background.render(screen, update_queue)

    # level
    load_level("level.txt")

    # Force update display (generally handled at end of main loop below)
    update_display(update_queue)

    while running:
        # input loop
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # draw navmesh
        for rect in navmesh_col:
            pygame.draw.rect(screen, RED, rect, 1)
            update_queue.append(rect)

        update_display(update_queue)

        fps_clock.tick(FPS)
