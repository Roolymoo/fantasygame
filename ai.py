from pygame import Rect

from image import Image
from collision import is_collide_obj


def _get_img_set():
    """() -> dict
    Returns img_set dict format."""
    mov_states = ["idle"]
    return {s: None for s in mov_states}


def _update_kobold_img_set(img_set, rect):
    """(dict, Rect) -> NoneType
    Updates img_set with images for Kobold."""
    for mov_state in img_set:
        img_set[mov_state] = Image("creature.png", rect=rect)


def _do_explore(creature):
    ...


class AIMap:
    """Class for holding map knowledge for an ai."""
    def __init__(self, w, h):
        """(int, int) -> NoneType
        w, h specify the w, h of the ai."""
        self.w = w
        self.h = h
        self.map = dict()

    def add(self, type, rect):
        """(int, Rect) -> NoneType
        Adds entry to map of object of given type and dimensions rect. Type values:
        0 - passable
        1 - impassible"""
        self.map.update({(rect.x, rect.y): (type, rect)})

    def is_contains(self, rect):
        """(Rect) -> bool
        Returns true iff (rect.x, rect.y) is in self.map."""
        return (rect.x, rect.y) in self.map

    def get_type(self, rect):
        """(Rect) -> int
        Returns the type of the entry self has at rect."""
        return self.map[(rect.x, rect.y)][-1]

    def is_passable(self, rect, *objs):
        """(Rect, tuple) -> bool
        Returns true if rect is a passable region with respect to self or objs (a tuple of collections of objects which
        are possible obstacles), false otherwise, in which case it is added to self."""
        if self.is_contains(rect):
            return self.get_type(rect)
        else:
            # search through all objects for the first one that is an obstacle, if it exists
            for collection in objs:
                ...



class Creature:
    """Foundation class for creatures."""
    def __init__(self, rect, is_render=False):
        """(Rect, bool) -> NoneType"""
        self.rect = rect
        self.img_set = _get_img_set()
        self.mov_state = "idle"
        self.is_alive = True
        self.ai_state = "explore"
        # flag for rendering
        self.is_render = is_render

    def die(self):
        """() -> NoneType"""
        self.is_alive = False

    def is_alive(self):
        """() -> bool"""
        return self.is_alive

    def get_img(self):
        """() -> Surface"""
        return self.img_set[self.mov_state]

    def update(self):
        """() -> NoneType
        Continue with whatever the creature was doing."""
        if self.ai_state == "explore":
            _do_explore(self)

    def render(self, screen, update_queue):
        """(Surface, deque) -> NoneType
        Renders self if is_render flag set to true. Sets to false upon completion."""
        img = self.get_img()
        if img and self.is_render:
            img.render(screen, update_queue)
            self.is_render = False


class Kobold(Creature):
    def __init__(self, rect):
        Creature.__init__(self, rect)
        _update_kobold_img_set(self.img_set, rect)

