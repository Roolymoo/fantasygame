from pygame import Rect

from collision import is_collide_rect, is_collide_obj


class Object:
    """Basic structure for an object in the game."""
    def __init__(self, rect):
        self.rect = rect
        self.img = None

    def is_collide(self, *objs):
        """(tuple) -> rect
        If self collides with any obj in objs (collection of classes with rect attributes or rect's), return that rect.
        Otherwise return None."""
        for obj in objs:
            if type(obj) == Rect:
                rect = is_collide_rect(self.rect, obj)
                if rect:
                    return rect
            else:
                rect = is_collide_obj(self, obj)
                if rect:
                    return rect
        return None

    def render(self, screen, update_queue):
        if self.img:
            screen.blit(self.img, self.rect)
            update_queue.append(self.rect)
