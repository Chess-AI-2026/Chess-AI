from board import Board, BOARD_SIZE
from pieces import PieceType, Color
from move import Move
import random

DIRECTIONS = {
    PieceType.BISHOP: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    PieceType.ROOK: [(-1, 0), (1, 0), (0, -1), (0, 1)],
    PieceType.QUEEN: [(-1, -1), (-1, 1), (1, -1), (1, 1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)],
}

PIECE_VALUES = {
    PieceType.PAWN: 1,
    PieceType.KNIGHT: 3,
    PieceType.BISHOP: 3,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 9,
    PieceType.KING: 1000
}


class Game:
    def __init__(self):
        self.board = Board()

    def generate_legal_moves(self, color: Color):
        moves = self.generate_moves(color)
        legal = []
        for move in moves:
            self.board.make_move(move)
            if not self.is_check(color):
                legal.append(move)
            self.board.undo_move()
        return legal

    def generate_moves(self, color: Color):
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece is None or piece.color != color:
                    continue

                if piece.piece_type == PieceType.PAWN:
                    moves.extend(self.pawn_moves(row, col, piece))
                elif piece.piece_type == PieceType.KNIGHT:
                    moves.extend(self.knight_moves(row, col, piece))
                elif piece.piece_type in (PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN):
                    moves.extend(self.sliding_moves(row, col, piece))
                elif piece.piece_type == PieceType.KING:
                    moves.extend(self.king_moves(row, col, piece))

        return moves

    def pawn_moves(self, row, col, piece):
        moves = []
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        fwd = row + direction
        if self.board.in_bounds(fwd, col) and self.board.get_piece(fwd, col) is None:
            moves.append(self.maybe_promotion(row, col, fwd, col, piece))

            if row == start_row:
                fwd2 = row + 2 * direction
                if self.board.get_piece(fwd2, col) is None:
                    moves.append(Move(row, col, fwd2, col))

        for dc in (-1, 1):
            c_row = row + direction
            c_col = col + dc
            if not self.board.in_bounds(c_row, c_col):
                continue
            target = self.board.get_piece(c_row, c_col)
            if target is not None and target.color != piece.color:
                moves.append(self.maybe_promotion(row, col, c_row, c_col, piece))

        return moves

    def maybe_promotion(self, sr, sc, er, ec, piece):
        if (piece.color == Color.WHITE and er == 0) or \
           (piece.color == Color.BLACK and er == 7):
            return Move(sr, sc, er, ec, promotion_piece_type=None)
        return Move(sr, sc, er, ec)

    def knight_moves(self, row, col, piece):
        moves = []
        jumps = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                 (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in jumps:
            r, c = row + dr, col + dc
            if self.board.in_bounds(r, c):
                target = self.board.get_piece(r, c)
                if target is None or target.color != piece.color:
                    moves.append(Move(row, col, r, c))
        return moves

    def sliding_moves(self, row, col, piece):
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

    def king_moves(self, row, col, piece):
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.board.in_bounds(r, c):
                    target = self.board.get_piece(r, c)
                    if target is None or target.color != piece.color:
                        moves.append(Move(row, col, r, c))
        return moves


    def find_king(self, color: Color):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = self.board.get_piece(r, c)
                if p and p.color == color and p.piece_type == PieceType.KING:
                    return r, c
        return None

    def is_check(self, color: Color):
        king_pos = self.find_king(color)
        enemy = Color.WHITE if color == Color.BLACK else Color.BLACK
        for move in self.generate_moves(enemy):
            if (move.end_row, move.end_col) == king_pos:
                return True
        return False

    def is_checkmate(self, color: Color):
        return self.is_check(color) and len(self.generate_legal_moves(color)) == 0

    def is_stalemate(self, color: Color):
        return not self.is_check(color) and len(self.generate_legal_moves(color)) == 0

    def evaluate_board(self):
        score = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = self.board.get_piece(r, c)
                if p:
                    val = PIECE_VALUES[p.piece_type]
                    score += val if p.color == Color.WHITE else -val
        return score


    def ai_easy(self, color):
        moves = self.generate_legal_moves(color)
        return random.choice(moves) if moves else None

    def ai_medium(self, color):
        return self.get_best_move(color, depth=2)

    def ai_hard(self, color):
        return self.get_best_move(color, depth=3)


    def get_best_move(self, color, depth):
        best_move = None

        if color == Color.WHITE:
            best_score = float("-inf")
            for move in self.generate_legal_moves(color):
                self.board.make_move(move)
                score = self.minimax(depth - 1, False, float("-inf"), float("inf"))
                self.board.undo_move()
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = float("inf")
            for move in self.generate_legal_moves(color):
                self.board.make_move(move)
                score = self.minimax(depth - 1, True, float("-inf"), float("inf"))
                self.board.undo_move()
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def minimax(self, depth, maximizing, alpha, beta):
        color = Color.WHITE if maximizing else Color.BLACK

        if depth == 0:
            return self.evaluate_board()

        moves = self.generate_legal_moves(color)
        if not moves:
            if self.is_check(color):
                return float("-inf") if maximizing else float("inf")
            return 0

        if maximizing:
            value = float("-inf")
            for move in moves:
                self.board.make_move(move)
                value = max(value, self.minimax(depth - 1, False, alpha, beta))
                self.board.undo_move()
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        else:
            value = float("inf")
            for move in moves:
                self.board.make_move(move)
                value = min(value, self.minimax(depth - 1, True, alpha, beta))
                self.board.undo_move()
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
