from enum import Enum
from typing import List, Tuple

class MoveType(Enum):
    UNCOVER = 1
    EAT = 2
    MOVE = 3

Action = Tuple[MoveType, int, int, int, int]