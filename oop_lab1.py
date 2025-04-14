class Point:
    # атрибуты параметры экрана
    WIDTH = 2160
    HEIGHT = 1440

    # инициализатор (конструктор)
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    # region property
    # x getter
    @property
    def x(self) -> int:
        return self._x

    # x setter
    @x.setter
    def x(self, x: int) -> None:
        if x < 0 or x > self.WIDTH:
            raise ValueError(f"х должен находиться в интервале от 0 до {self.WIDTH}")
        self._x = x

    # y getter
    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        if y < 0 or y > self.HEIGHT:
            raise ValueError(f"y должен находиться в интервале от 0 до {self.HEIGHT}")
        self._y = y
    # endregion

    # region dunder-методы
    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"
    # endregion


class Vector:
    # инициализатор
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    # аналог инициализатора для случая, когда вектор создается поточкам
    @classmethod
    def from_points(cls, start: Point, end: Point) -> None:
        return cls(end.x - start.x, end.y - start.y)

    # region property
    # x getter
    @property
    def x(self) -> int:
        return self._x

    # x setter
    @x.setter
    def x(self, x: int) -> None:
        self._x = x

    # y getter
    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        self._y = y
    # endregion

    # region dunder methods
    def __getitem__(self, index: int) -> int:
        if index not in (0, 1):
            raise IndexError(
                "Для двумерного вектора обращаться к координатам можно только по индексам 0 и 1"
            )
        return [self.x, self.y][index]

    def __setitem__(self, index: int, value: int) -> None:
        if index not in (0, 1):
            raise IndexError(
                "Для двумерного вектора обращаться к координатам можно только по индексам 0 и 1"
            )
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value

    def __len__(self) -> int:
        return 2  # двумерное пространство

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self) -> int:
        if self.index < len(self):
            coordinate = self[self.index]
            self.index += 1
            return coordinate
        raise StopIteration

    def __eq__(self, other: "Vector") -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** (1 / 2)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k: int) -> "Vector":
        return Vector(self.x * k, self.y * k)

    def __truediv__(self, k: int) -> "Vector":
        return Vector(int(self.x / k), int(self.y / k))
    # endregion

    # region product methods
    def dot(self, other: "Vector") -> int:
        return sum([self[i] * other[i] for i in range(len(self))])

    @staticmethod
    def dot_product(v1: "Vector", v2: "Vector") -> int:
        return v1.dot(v2)

    def cross(self, other: "Vector") -> int:
        return self.x * other.y - self.y * other.x

    @staticmethod
    def cross_product(v1: "Vector", v2: "Vector") -> int:
        return v1.cross(v2)

    def triple_product(self, v1: "Vector", v2: "Vector") -> int:
        return 0
    # endregion


# region демонстрация работы класса Point
x1, y1 = [
    int(coord)
    for coord in input("\n\nВведите координаты точки 1 через пробел ").split()
]
p1 = Point(x1, y1)
x2, y2 = [
    int(coord) for coord in input("Введите координаты точки 2 через пробел ").split()
]
p2 = Point(x2, y2)

print(p1, p2)
print(repr(p1), repr(p2))
print("Точки равны" if p1 == p2 else "Точки не равны")
# endregion

# region демонстрация работы класса Vector
x1, y1 = [
    int(coord)
    for coord in input("\nВведите координаты вектора 1 через пробел ").split()
]
v1 = Vector(x1, y1)
x2, y2 = [
    int(coord) for coord in input("Введите координаты вектора 2 через пробел ").split()
]
v2 = Vector(x2, y2)
print("Вектор 3 создан по двум точкам, введенным ранее")
v3 = Vector.from_points(p1, p2)
k = int(input("Введите число "))

print(v1, v2, v3)
print(repr(v1), repr(v2), repr(v3))
print("Длины векторов:", abs(v1), abs(v2), abs(v3))
print("Cумма векторов 1 и 2:", v1 + v2)
print("Разность векторов 1 и 2:", v1 - v2)
print(f"Вектор 1, умноженный на число {k}:", v1 * k)
print("Скалярное произведение векторов 1 и 2:", Vector.dot_product(v1, v2))
print("Векторное произведение векторов 1 и 2:", abs(Vector.cross_product(v1, v2)))
print("Смешанное произведение векторов:", v1.triple_product(v2, v3))
# endregion
