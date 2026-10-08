from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 240, 60)
    BRIGHT_YELLOW = (252, 249, 157)
    RED = (255, 0, 0)
    BRIGHT_RED = (255, 150, 150)
    GREEN = (0, 255, 0)
    BRIGHT_GREEN = (171, 255, 171)
    BLUE = (0, 0, 255)
    BRIGHT_BLUE = (102, 186, 250)
    BLACK = (0, 0, 0)
    BACKGROUND = (67, 67, 67)
    TRANSPARENT = (0, 0, 0, 0)

    def get_bright(self, color: Color) -> Color:
        bright_name = f"BRIGHT_{color.name}"
        return Color[bright_name]

