import os.path

from pygame import image


def get_level(level_n):
    """(str) -> str
    Returns full relative path of file level_n."""
    return os.path.join("levels", level_n)


def load_img(img_n):
    """(str) -> Surface
    Loads img given by img_n and returns as Surface."""
    return image.load(os.path.join("art", img_n))
