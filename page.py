
starting = """
<html>
    <head>
        <title>{0}</title>
        <link rel="stylesheet" href="cel.css">
    </head>
    <body>
"""

closing = """
    </body>
</html>
"""

legend = """
<div class="legend">
    <div class="colorbox" style="background-color: {0};" title={0}></div>
    <div class="name">{1}</div>
</div>
"""


class Page(object):
    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    # Projection
    # -------------------------------------------------------------------------

    def projection(self, sw):
        return sw.hue, 101 - sw.light

    # -------------------------------------------------------------------------
    # Overrideable Callbacks
    # -------------------------------------------------------------------------

    def onCanvas(self):
        pass

    def onLegend(self):
        pass

    # -------------------------------------------------------------------------
    # Write helpers
    # -------------------------------------------------------------------------

    def addCentroid(self, sw, txt):
        circle = '<circle class="centroid" cx="{0}%" cy="{1}%" r="0.75%" />\n'
        self.handle.write('    ' + circle.format(*self.projection(sw)))

        opening = '    <text x="{0}%" y="{1}%"'.format(*self.projection(sw))
        align = ' dominant-baseline="middle" text-anchor="middle"'
        style = ' class="centroid"'
        closing = '>{0}</text>\n'.format(txt)
        self.handle.write(opening + align + style + closing)

    def addClustered(self, rgb, sw):
        s = '    <circle style="fill:{0};" cx="{1}%" cy="{2}%" r="0.75%" />\n'
        rgbStr = 'rgb({0},{1},{2})'.format(*rgb)
        self.handle.write(s.format(rgbStr, *self.projection(sw)))

    def addLegend(self, rgb, name):
        rgbStr = 'rgb({0},{1},{2})'.format(*rgb)
        s = legend.format(rgbStr, name)
        self.handle.write(s)

    def addSwatch(self, sw):
        s = '    <circle style="fill:{0};" cx="{1}%" cy="{2}%" r="0.75%" />\n'
        rgbStr = 'rgb({0},{1},{2})'.format(sw.red, sw.green, sw.blue)
        self.handle.write(s.format(rgbStr, *self.projection(sw)))

    # -------------------------------------------------------------------------
    # Main function
    # -------------------------------------------------------------------------

    def render(self, pathName, title):
        with open(pathName, 'w') as f:
            self.handle = f

            f.write(starting.format(title))
            f.write('  <svg>\n')
            self.onCanvas()
            f.write('  </svg>\n')
            f.write('  <div class="legendPanel">\n')
            self.onLegend()
            f.write('  </div>\n')
            f.write(closing)

        self.handle = None
