class Dimensions:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __str__(self):
        return f'Dimensions(width: {self.width}, height: {self.height})'


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Point(x: {self.x}, y: {self.y})'
