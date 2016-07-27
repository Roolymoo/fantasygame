from collections import deque

from pygame import Rect, draw


class Background:
    """Handles all background objects."""
    def __init__(self, w, h, colour):
        """(int, int, tuple) -> NoneType"""
        self.rect = Rect(0, 0, w, h)
        self.colour = colour
        # objs that become part of background
        self.obj_col = deque()

    def reset(self):
        self.obj_col.clear()

    def render(self, screen, update_queue, rect=None):
        """(Surface, deque, Rect) -> NoneType
        If rect is None, render everything, otherwise only render what intersects with the rect."""
        if rect is None:
            draw.rect(screen, self.colour, self.rect)
            update_queue.append(self.rect)

            for obj in self.obj_col:
                obj.render(screen, update_queue)
        else:
            draw.rect(screen, self.colour, rect)
            update_queue.append(rect)

            for obj in self.obj_col:
                if obj.rect.colliderect(rect):
                    obj.render(screen, update_queue)
