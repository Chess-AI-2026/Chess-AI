
class Move:
    def __init__(self, start_row, start_col, end_row, end_col,
                 captured_piece=None, promotion_piece_type=None,
                 is_castling=False, is_en_passant=False):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.captured_piece = captured_piece
        self.promotion_piece_type = promotion_piece_type
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant

    def __repr__(self):
        return f"({self.start_row},{self.start_col})->({self.end_row},{self.end_col})"
