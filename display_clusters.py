from page import Page
from operator import attrgetter


class Clusters(Page):
    def __init__(self, swatches, palette, indexes):
        self.swatches = swatches
        self.palette = palette
        self.indexes = indexes

    def onCanvas(self):
        for i, mu in enumerate(self.indexes):
            rgb = self.palette[mu].rgb
            sw = self.swatches[i]
            self.addClustered(rgb, sw)

        for sw in self.palette:
            self.addCentroid(sw, '+')

    def onLegend(self):
        for sw in sorted(self.palette, key=attrgetter('hue', 'saturation')):
            self.addLegend(sw.rgb, sw.name)
