from board import Board, BOARD_SIZE
from pieces import PieceType, Color
from move import Move

DIRECTIONS = {
    PieceType.BISHOP: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    PieceType.ROOK: [(-1, 0), (1, 0), (0, -1), (0, 1)],
    PieceType.QUEEN: [(-1, -1), (-1, 1), (1, -1), (1, 1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)],
}


class Game:
    def __init__(self):
        self.board = Board()

    def generate_legal_moves(self, color: Color):
        moves = self.generate_pseudo_legal_moves(color)
        legal_moves = []
        for move in moves:
            self.board.make_move(move)
            if not self.is_in_check(color):
                legal_moves.append(move)
            self.board.undo_move()
        return legal_moves

    def generate_pseudo_legal_moves(self, color: Color):
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece is None or piece.color != color:
                    continue

                if piece.piece_type == PieceType.PAWN:
                    moves.extend(self._pawn_moves(row, col, piece))
                elif piece.piece_type == PieceType.KNIGHT:
                    moves.extend(self._knight_moves(row, col, piece))
                elif piece.piece_type in (PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN):
                    moves.extend(self._sliding_moves(row, col, piece))
                elif piece.piece_type == PieceType.KING:
                    moves.extend(self._king_moves(row, col, piece))

        return moves

    def _pawn_moves(self, row, col, piece):
        moves = []
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        fwd_row = row + direction
        if self.board.in_bounds(fwd_row, col) and self.board.get_piece(fwd_row, col) is None:
            moves.append(self._maybe_promotion(row, col, fwd_row, col, piece))

            if row == start_row:
                fwd2_row = row + 2 * direction
                if self.board.get_piece(fwd2_row, col) is None:
                    moves.append(Move(row, col, fwd2_row, col))

        for dc in (-1, 1):
            c_col = col + dc
            c_row = row + direction
            if not self.board.in_bounds(c_row, c_col):
                continue
            target = self.board.get_piece(c_row, c_col)
            if target is not None and target.color != piece.color:
                moves.append(self._maybe_promotion(row, col, c_row, c_col, piece))

        return moves

    def _maybe_promotion(self, sr, sc, er, ec, piece):
        if (piece.color == Color.WHITE and er == 0) or \
           (piece.color == Color.BLACK and er == 7):
            return Move(sr, sc, er, ec, promotion_piece_type=None)
        return Move(sr, sc, er, ec)

    def _knight_moves(self, row, col, piece):
        moves = []
        jumps = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                 (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in jumps:
            r, c = row + dr, col + dc
            if not self.board.in_bounds(r, c):
                continue
            target = self.board.get_piece(r, c)
            if target is None or target.color != piece.color:
                moves.append(Move(row, col, r, c))
        return moves

    def _sliding_moves(self, row, col, piece):
        moves = []
        for dr, dc in DIRECTIONS[piece.piece_type]:
            r, c = row + dr, col + dc
            while self.board.in_bounds(r, c):
                target = self.board.get_piece(r, c)
                if target is None:
                    moves.append(Move(row, col, r, c))
                else:
                    if target.color != piece.color:
                        moves.append(Move(row, col, r, c))
                    break
                r += dr
                c += dc
        return moves

    def _king_moves(self, row, col, piece):
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if not self.board.in_bounds(r, c):
                    continue
                target = self.board.get_piece(r, c)
                if target is None or target.color != piece.color:
                    moves.append(Move(row, col, r, c))
        return moves

    def find_king(self, color: Color):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color and piece.piece_type == PieceType.KING:
                    return row, col
        return None

    def is_in_check(self, color: Color):
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        enemy_color = Color.WHITE if color == Color.BLACK else Color.BLACK
        enemy_moves = self.generate_pseudo_legal_moves(enemy_color)
        for move in enemy_moves:
            if (move.end_row, move.end_col) == king_pos:
                return True
        return False

    def is_checkmate(self, color: Color):
        if not self.is_in_check(color):
            return False
        return len(self.generate_legal_moves(color)) == 0

    def is_stalemate(self, color: Color):
        if self.is_in_check(color):
            return False
        return len(self.generate_legal_moves(color)) == 0

