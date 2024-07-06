class Camera:
    def __init__(self, left_top, bottom_right, size_scroll):
        self.left_top = left_top
        self.bottom_right = bottom_right
        self.size_scroll = size_scroll
        self.scroll = [0, 0]

    def update(self, pos = (0, 0), rate = 30):
        self.scroll[0] += (self.size_scroll[0] / 2 - pos[0] - self.scroll[0]) / rate
        self.scroll[1] += (self.size_scroll[1] / 2 - pos[1] - self.scroll[1]) / rate
        self.scroll[0] = min(self.scroll[0], -1 * self.left_top[0])
        self.scroll[0] = max(self.scroll[0], -1 * (self.bottom_right[0] - self.size_scroll[0]))
        self.scroll[1] = min(self.scroll[1], -1 * self.left_top[1])
        self.scroll[1] = max(self.scroll[1], -1 * (self.bottom_right[1] - self.size_scroll[1]))

    def get_scroll(self):
        return (int(self.scroll[0]), int(self.scroll[1]))
