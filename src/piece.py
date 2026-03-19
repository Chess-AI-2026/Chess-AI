
from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = -1


class PieceType(Enum):
    PAWN = "P"
    KNIGHT = "N"
    BISHOP = "B"
    ROOK = "R"
    QUEEN = "Q"
    KING = "K"


class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.piece_type = piece_type
        self.color = color

    def __repr__(self):
        return f"{self.color.name[0]}{self.piece_type.value}"
