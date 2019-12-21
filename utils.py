"""
utils
"""


class BoundaryCheck:

    def __init__(self, coords):
        self._coords = coords

    @staticmethod
    def area_of_triangle(x1, y1, x2, y2, x3, y3):
        """
        calculate area of triangle
        """
        area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

        return area

    def area_of_polygon_wrt_point(self, centroid):
        """
        calculate area of polygon
        """
        x, y = [i for i in centroid]

        area_of_polygon = 0.0

        for i in range(len(self._coords) - 1):
            x1, y1 = [i for i in self._coords[i]]
            x2, y2 = [i for i in self._coords[i + 1]]
            area_of_polygon += self.area_of_triangle(x, y, x1, y1, x2, y2)

        x1, y1 = [i for i in self._coords[-1]]
        x2, y2 = [i for i in self._coords[0]]

        area_of_polygon += self.area_of_triangle(x, y, x1, y1, x2, y2)

        return area_of_polygon

    def area_of_polygon(self):
        x = [i[0] for i in self._coords]
        y = [i[1] for i in self._coords]
        n = len(self._coords)
        area = 0.0
        j = n - 1
        for i in range(0, n):
            area += (x[j] + x[i]) * (y[j] - y[i])
            j = i
        return int(abs(area / 2.0))

    def exists(self, point):
        """
        check if the the given point exists within the rectangle or not
        """

        area_with_centroid = self.area_of_polygon()

        x, y = [i for i in point]
        area_with_new_point = self.area_of_polygon_wrt_point([x, y])

        return area_with_centroid == area_with_new_point
