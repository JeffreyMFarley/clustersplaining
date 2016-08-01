from swatch import Swatch
from page import Page
from operator import attrgetter


class DisplaySwatches(Page):
    def onCanvas(self):
        for sw in sorted(Swatch.acquire(), key=attrgetter('saturation')):
            self.addSwatch(sw)

if __name__ == "__main__":
    p = DisplaySwatches()
    p.render('cel/swatches.html', 'Starting Palette')
