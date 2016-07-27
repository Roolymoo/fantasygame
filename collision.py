def is_collide_rect(rect1, rect2):
    """(Rect, Rect) -> bool
    Returns True iff rect1 collides with rect2, False otherwise."""
    return rect1.rect.colliderect(rect2)
