from data import swatch_list


class Swatch():
    @classmethod
    def acquire(cls):
        for row in swatch_list:
            yield Swatch(row[0], row[1])

    def __init__(self, rgb, name=''):
        import colorsys
        hsv = colorsys.rgb_to_hsv(*rgb)
        self.name = name
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]
        self.hue = 100 * hsv[0]
        self.saturation = 100 * hsv[1]
        self.light = 100 * hsv[2] / 256

    def __contains__(self, item):
        return hasattr(self, item)

    def __getitem__(self, key):
        return getattr(self, key)

    @property
    def rgb(self):
        return [self.red, self.green, self.blue]
