from swatch import Swatch
from page import Page


class DisplaySwatches(Page):
    def onCanvas(self):
        for sw in Swatch.orderedList():
            self.addSwatch(sw)

if __name__ == "__main__":
    p = DisplaySwatches()
    p.render('cel/swatches.html', 'Starting Palette')
