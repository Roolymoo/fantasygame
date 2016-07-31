from pygame import Rect


def is_collide_rect(rect1, rect2):
    """(Rect, Rect) -> Rect
    Returns rect2 iff rect1 collides with rect2, None otherwise."""
    if rect1.colliderect(rect2):
        return rect2
    else:
        return None


def is_collide_obj(obj1, obj2):
    """(Object, Object) -> rect
    Returns obj2.rect iff obj1.rect1 collides with obj2.rect, None otherwise."""
    if obj1.rect.colliderect(obj2.rect):
        return obj2.rect
    else:
        return None


def is_collide(obj, *objs):
    """(Object|Rect, tuple) -> rect"""
    if type(obj) == Rect:
        rect = obj
    else:
        rect = obj.rect

    for o in objs:
        if type(o) == Rect:
            r = is_collide_rect(rect, obj)
        else:
            r = is_collide_obj(rect, obj)

        if r:
                return r

    return None
