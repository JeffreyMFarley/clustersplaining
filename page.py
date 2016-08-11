
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

    # / x(t) \ = /  cos(p)  sin(p) \ / a cos(t) \
    # \ y(t) /   \ -sin(p)  cos(p) / \ b sin(t) /
    #which makes the projection onto the x-axis equal to
    # x(t) = a cos(p) cos(t) + b sin(p) sin(t),
    # and y(t) analogously.
    # y(t) = -a sin(p) cos(t) + b cos(p) sin(t)

    def projection(self, sw):
        from math import cos, sin, pi

        two_radians = 6.28318530718
        pi_over_2 = 1.57079632679

        b = sw.saturation / 2.0
        a = sw.light / 2.0
        p = (sw.hue / 100.0) * two_radians

        t = pi + pi / 6.0

        # x = a * math.cos(p)
        # y = a * math.sin(p)

        x = a * cos(p) * cos(t) + b * sin(p) * sin(t)
        y = -1.0 * a * sin(p) * cos(t) + b * cos(p) * sin(t)

        return x + 50, y + 50

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
            f.write('  <svg viewBox="0 0 600 600" width="100%" height="100%" '
                    'preserveAspectRatio="xMidYMid meet">\n')
            self.onCanvas()
            f.write('  </svg>\n')
            f.write('  <div class="legendPanel">\n')
            self.onLegend()
            f.write('  </div>\n')
            f.write(closing)

        self.handle = None
