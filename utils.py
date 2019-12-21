"""
utils
"""


class BoundaryCheck:

    def __init__(self, coords):
        self._coords = coords

    @staticmethod
    def centroid(coords):
        """
        calculate centroid
        """
        x_list = [i[0] for i in coords]
        y_list = [i[1] for i in coords]

        length = len(coords)

        x = sum(x_list) / length
        y = sum(y_list) / length

        return x, y

    @staticmethod
    def area_of_triangle(x1, y1, x2, y2, x3, y3):
        """
        calculate area of triangle
        """
        area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

        return area

    def area_of_polygon(self, centroid):
        """
        calculate area of polygon
        """
        x, y = [i for i in centroid]

        area_of_polygon = 0

        for i in range(len(self._coords) - 1):
            x1, y1 = [i for i in self._coords[i]]
            x2, y2 = [i for i in self._coords[i + 1]]
            area_of_polygon += self.area_of_triangle(x, y, x1, y1, x2, y2)

        x1, y1 = [i for i in self._coords[-1]]
        x2, y2 = [i for i in self._coords[0]]

        area_of_polygon += self.area_of_triangle(x, y, x1, y1, x2, y2)

        return area_of_polygon

    def exists(self, point):
        """
        check if the the given point exists within the rectangle or not
        """
        x, y = self.centroid(coords=self._coords)
        area_with_centroid = self.area_of_polygon([x, y])

        x, y = [i for i in point]
        area_with_new_point = self.area_of_polygon([x, y])

        return area_with_centroid == area_with_new_point
