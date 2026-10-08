
from dataclasses import dataclass
from enum import Enum


@dataclass
class Vector2i:
    x: int
    y: int


class GameState(Enum):
    PLAYER_TURN = 1
    CHECKING_PAIRS = 2
    GAME_OVER = 3
