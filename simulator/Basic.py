class Rectangle:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def Center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    def Tuple(self) -> tuple:
        return (self.x, self.y, self.width, self.height)

    def Contains(self, x, y) -> bool:
        if (self.x < x < self.x+self.width and self.y < y < self.y + self.height):
            return True
        else:
            return False