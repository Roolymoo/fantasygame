from pygame import Rect

from image import Image


def _get_img_set():
    """() -> dict
    Returns img_set dict format."""
    states = ["idle"]
    return {s: None for s in states}


def _update_kobold_img_set(img_set, rect):
    """(dict, Rect) -> NoneType
    Updates img_set with images for Kobold."""
    for s in img_set:
        img_set[s] = Image("creature.png", rect=rect)


class Creature:
    """Foundation class for creatures."""
    def __init__(self, rect):
        self.rect = rect
        self.img_set = _get_img_set()
        self.state = "idle"
        self.is_alive = True

    def die(self):
        self.is_alive = False

    def is_alive(self):
        return self.is_alive

    def get_img(self):
        """() -> Surface"""
        return self.img_set[self.state]

    def render(self, screen, update_queue):
        """(Surface, deque) -> NoneType"""
        img = self.get_img()
        if img:
            img.render(screen, update_queue)


class Kobold(Creature):
    def __init__(self, rect):
        Creature.__init__(self, rect)
        _update_kobold_img_set(self.img_set, rect)

