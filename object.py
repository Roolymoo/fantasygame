from pygame import Rect


class Object:
    """Basic structure for an object in the game."""
    def __init__(self, rect):
        self.rect = rect
        self.img = None

    def render(self, screen, update_queue):
        if self.img:
            screen.blit(self.img, self.rect)
            update_queue.append(self.rect)
