import plotter
import geopy


class LinePlotter(plotter.Plotter):

    def parse_query(self, query):
        super(LinePlotter, self).parse_query(query)

        points = query.get('path')
        if points is None or len(points) == 0:
            points = [
                '47 N 52.8317 W',
                '47 N 42 W'
            ]

        self.points = points

        surface = query.get('surfacevariable')
        if surface is not None and (surface == '' or surface == 'none'):
            surface = None

        self.surface = surface

        name = query.get('name')
        if name is None or name == '':
            name = "%s to %s" % (
                geopy.Point(points[0]),
                geopy.Point(points[-1])
            )

        self.name = name
