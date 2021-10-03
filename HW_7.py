import math


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Point(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)


class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
        self.point = Point(x, y)

    def contains(self, point):
        sqrt_distance = (self.x-point.x)**2 + (self.y-point.y)**2
        return sqrt_distance <= self.radius**2

    def square(self):
        return math.pi * self.radius ** 2


class Triangle:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def square(self):
        x1 = self.v1[0]
        y1 = self.v1[1]
        x2 = self.v2[0]
        y2 = self.v2[1]
        x3 = self.v3[0]
        y3 = self.v3[1]
        return abs(0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)))


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Shape):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y)
        self.height = height
        self.width = width
        self.angle = angle

    def square(self):
        return self.width * self.height


class colorizer:

    def __init__(self, color):
        self.color = color

    def __enter__(self):
        color = self.color
        color_dict = {'grey': "\033[90m",
                      'red': "\033[91m",
                      'green': "\033[92m",
                      'yellow': "\033[93m",
                      'blue': "\033[94m",
                      'pink': "\033[95m",
                      'turquoise': "\033[96m"}
        if color in color_dict.keys():
            print(color_dict[color])

    def __exit__(self, type, value, traceback):
        print('\033[0m', end='')


class frange:

    def __init__(self, right, left=None, step=1):
        if left is not None:
            self._right = left
            self._left = right
        else:
            self._left = 0
            self._right = right
        self._step = step

    def __next__(self):
        if self._step > 0 and self._left + self._step > self._right:
            raise StopIteration()
        elif self._step < 0 and self._left + self._step < self._right:
            raise StopIteration()
        result = self._left
        self._left += self._step
        return result

    def __iter__(self):
        return self
