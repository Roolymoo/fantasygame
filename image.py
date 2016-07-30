from fileloader import load_img


class Image:
    """For holding images and relevant data."""
    def __init__(self, img_n, img=None, rect=None):
        """(str, Surface) -> NoneType"""
        self.img_n = img_n
        self.img = img
        self.rect = rect

    def load(self):
        self.img = load_img(self.img_n)

    def render(self, screen, update_queue):
        """(Surface, deque) -> NoneType"""
        if not self.img:
            self.load()

        screen.blit(self.img, self.rect)
        update_queue.append(self.rect)
