from pieces import Piece, PieceType, Color
from move import Move

BOARD_SIZE = 8


class Board:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.to_move = Color.WHITE
        self.move_history = []
        self.setup_start_position()

    def setup_start_position(self):
        # Pawns
        for col in range(BOARD_SIZE):
            self.board[6][col] = Piece(PieceType.PAWN, Color.WHITE)
            self.board[1][col] = Piece(PieceType.PAWN, Color.BLACK)

        # Rooks
        self.board[7][0] = Piece(PieceType.ROOK, Color.WHITE)
        self.board[7][7] = Piece(PieceType.ROOK, Color.WHITE)
        self.board[0][0] = Piece(PieceType.ROOK, Color.BLACK)
        self.board[0][7] = Piece(PieceType.ROOK, Color.BLACK)

        # Knights
        self.board[7][1] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.board[7][6] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.board[0][1] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.board[0][6] = Piece(PieceType.KNIGHT, Color.BLACK)

        # Bishops
        self.board[7][2] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[7][5] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[0][2] = Piece(PieceType.BISHOP, Color.BLACK)
        self.board[0][5] = Piece(PieceType.BISHOP, Color.BLACK)

        # Queens
        self.board[7][3] = Piece(PieceType.QUEEN, Color.WHITE)
        self.board[0][3] = Piece(PieceType.QUEEN, Color.BLACK)

        # Kings
        self.board[7][4] = Piece(PieceType.KING, Color.WHITE)
        self.board[0][4] = Piece(PieceType.KING, Color.BLACK)

    def in_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get_piece(self, row, col):
        if not self.in_bounds(row, col):
            return None
        return self.board[row][col]

    def make_move(self, move: Move):
        piece = self.get_piece(move.start_row, move.start_col)
        captured = self.get_piece(move.end_row, move.end_col)
        move.captured_piece = captured

        self.board[move.end_row][move.end_col] = piece
        self.board[move.start_row][move.start_col] = None

        if move.promotion_piece_type is not None:
            self.board[move.end_row][move.end_col] = Piece(move.promotion_piece_type, piece.color)

        self.move_history.append(move)
        self.to_move = Color.WHITE if self.to_move == Color.BLACK else Color.BLACK

    def undo_move(self):
        if not self.move_history:
            return
        move = self.move_history.pop()
        piece = self.get_piece(move.end_row, move.end_col)
        self.board[move.start_row][move.start_col] = piece
        self.board[move.end_row][move.end_col] = move.captured_piece
        self.to_move = Color.WHITE if self.to_move == Color.BLACK else Color.BLACK

