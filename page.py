
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
    # Overrideable Callbacks
    # -------------------------------------------------------------------------

    def onCanvas(self):
        pass

    def onLegend(self):
        pass

    # -------------------------------------------------------------------------
    # Write helpers
    # -------------------------------------------------------------------------

    def addClustered(self, rgb, sw):
        s = '    <circle style="fill:{0};" cx="{1}%" cy="{2}%" r="0.75%" />\n'
        rgbStr = 'rgb({0},{1},{2})'.format(*rgb)
        self.handle.write(s.format(rgbStr, sw.hue, 101 - sw.light))

    def addSwatch(self, sw):
        s = '    <circle style="fill:{0};" cx="{1}%" cy="{2}%" r="0.75%" />\n'
        rgbStr = 'rgb({0},{1},{2})'.format(sw.red, sw.green, sw.blue)
        self.handle.write(s.format(rgbStr, sw.hue, 101 - sw.light))

    def addLegend(self, name, rgb):
        rgbStr = 'rgb({0},{1},{2})'.format(*rgb)
        s = legend.format(rgbStr, name)
        self.handle.write(s)

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
