class TwoDimensionalArray:
    def __init__(self, rows: int, columns: int, value: int = 0):
        self.array = []
        for row in range(rows):
            self.array.append([])
            for column in range(columns):
                self.array[row].append(value)
