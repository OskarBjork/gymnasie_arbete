from numpy import zeros


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = zeros((self.width, self.height))

    def get_coordinate_value(self, x: int, y: int) -> int:
        return self.grid[y][x]
