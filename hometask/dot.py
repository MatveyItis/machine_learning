
class Dot:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return 'x=' + str(self.x) + ' ' + 'y=' + str(self.y)

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))