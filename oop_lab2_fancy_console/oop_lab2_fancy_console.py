# Лабораторная работа №2: "Красивая консоль"
from enum import Enum


class Colour(Enum):
    BLACK = "\u001b[30;1m"
    RED = "\u001b[31;1m"
    GREEN = "\u001b[32;1m"
    YELLOW = "\u001b[33;1m"
    BLUE = "\u001b[34;1m"
    PURPLE = "\u001b[35;1m"
    WHITE = "\u001b[37;1m"
    NEUTRAL = "\u001b[0m"


class Printer:
    def __init__(
        self, colour: Colour, position: tuple[int, int], symbol: str, font_name: str
    ) -> None:
        self.position = position[:]
        self.symbol = symbol
        self.colour = colour
        self.font: dict[str, list[str]] = {}
        self.font_height: int = 0
        self.font_width: int = 0
        self.load_font(font_name)

    def load_font(self, filename: str) -> None:
        try:
            with open(filename, "r") as file:
                self.font.clear()
                self.font_height, self.font_width = [
                    int(_) for _ in file.readline().split()
                ]
                while True:
                    char = file.readline().strip()
                    if not char:
                        break
                    self.font[char] = []
                    for i in range(self.font_height):
                        line = file.readline().rstrip().ljust(self.font_width)
                        self.font[char].append(line)
        except Exception as e:
            print(f"Error loading font file: {e}")

    def print(self, text: str) -> None:
        print("\033[2J")
        for i in range(self.font_height):
            line = []
            for char in text.upper():
                if char == " ":
                    line.append(" " * (self.font_width - 5))
                else:
                    line.append(self.font[char][i])
            line = "  ".join(line)
            rendered_line = line.replace("#", self.symbol)
            print(f"\u001b[{self.position[0]+i+1};{self.position[1]+1}H{rendered_line}")

    @classmethod
    def static_print(
        cls,
        colour: Colour,
        text: str,
        position: tuple[int, int],
        symbol: str,
        font_name: str,
    ) -> None:
        print(colour.value)
        temp_printer = cls(colour, position, symbol, font_name)
        temp_printer.print(text)
        print("\u001b[0m")

    def __enter__(self):
        print(self.colour.value)
        return self

    def __exit__(self, *args) -> None:
        print(Colour.NEUTRAL.value)


if __name__ == "__main__":
    Printer.static_print(
        Colour.PURPLE,
        "My favourite",
        (3, 5),
        "Ж",
        "C:/MyPythonProjects/oop_lab2/alphabet5.txt",
    )
    with Printer(
        Colour.RED, (1, 9), "@", "C:/MyPythonProjects/oop_lab2/alphabet9.txt"
    ) as printer:
        printer.print("subject is oop")
    print("\n\n=== THE FINAL COLOUR IS NEUTRAL === ")
