import pygame
from game import Game
from pieces import Color, PieceType
from board import BOARD_SIZE

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
SQUARE_SIZE = WINDOW_WIDTH // BOARD_SIZE

BOARD_LIGHT = (240, 217, 181)
BOARD_DARK = (181, 136, 99)

PURPLE = (180, 130, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class UI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)

        self.game = Game()
        self.running = True
        self.selected_square = None
        self.game_over_message = None

    def run(self):
        self.show_main_menu()
        while self.running:
            self.handle_game_loop()
        pygame.quit()

    def show_main_menu(self):
        in_menu = True
        while in_menu and self.running:
            self.screen.fill((50, 50, 80))
            self.draw_text_center("Chess", WINDOW_WIDTH // 2, 80, WHITE, 36)

            start_rect = self.draw_button("Start Game", WINDOW_WIDTH // 2, 200)
            instr_rect = self.draw_button("Instructions", WINDOW_WIDTH // 2, 260)
            quit_rect = self.draw_button("Quit", WINDOW_WIDTH // 2, 320)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_menu = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        in_menu = False
                    elif instr_rect.collidepoint(event.pos):
                        self.show_instructions()
                    elif quit_rect.collidepoint(event.pos):
                        self.running = False
                        in_menu = False

            self.clock.tick(30)

    def show_instructions(self):
        showing = True
        while showing and self.running:
            self.screen.fill((50, 50, 80))
            self.draw_text_center("Instructions", WINDOW_WIDTH // 2, 60, WHITE, 32)
            self.draw_text_center("Local Player vs Player chess.", WINDOW_WIDTH // 2, 120, WHITE)
            self.draw_text_center("Click a piece, then click a destination square.", WINDOW_WIDTH // 2, 150, WHITE)
            self.draw_text_center("White moves first, then Black.", WINDOW_WIDTH // 2, 180, WHITE)

            back_rect = self.draw_button("Back", WINDOW_WIDTH // 2, 400)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    showing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        showing = False

            self.clock.tick(30)

    def handle_game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over_message is None:
                self.handle_click(event.pos)

        self.draw_board()
        if self.game_over_message:
            self.draw_game_over_overlay()
        pygame.display.flip()
        self.clock.tick(30)

    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if self.selected_square is None:
            piece = self.game.board.get_piece(row, col)
            if piece is not None and piece.color == self.game.board.to_move:
                self.selected_square = (row, col)
        else:
            sr, sc = self.selected_square
            legal_moves = self.game.generate_legal_moves(self.game.board.to_move)
            chosen_move = None
            for m in legal_moves:
                if m.start_row == sr and m.start_col == sc and m.end_row == row and m.end_col == col:
                    chosen_move = m
                    break
            if chosen_move:
                piece = self.game.board.get_piece(sr, sc)

                is_pawn_promo = (
                        piece is not None and
                        piece.piece_type == PieceType.PAWN and
                        (
                                (piece.color == Color.WHITE and row == 0) or
                                (piece.color == Color.BLACK and row == 7)
                        )
                )

                if is_pawn_promo:
                    self.choose_promotion(chosen_move)
                else:
                    self.game.board.make_move(chosen_move)

                self.check_endgame()

            self.selected_square = None

    def choose_promotion(self, move):
        choosing = True
        options = [
            ("Queen", PieceType.QUEEN),
            ("Rook", PieceType.ROOK),
            ("Bishop", PieceType.BISHOP),
            ("Knight", PieceType.KNIGHT)
        ]

        while choosing and self.running:
            self.screen.fill((50, 50, 80))
            self.draw_text_center("Choose Promotion", WINDOW_WIDTH // 2, 80, WHITE, 32)

            buttons = []
            y = 200
            for text, ptype in options:
                rect = self.draw_button(text, WINDOW_WIDTH // 2, y)
                buttons.append((rect, ptype))
                y += 60

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    choosing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, ptype in buttons:
                        if rect.collidepoint(event.pos):
                            move.promotion_piece_type = ptype
                            self.game.board.make_move(move)
                            choosing = False
                            return

            self.clock.tick(30)

    def check_endgame(self):
        color_to_move = self.game.board.to_move
        if self.game.is_checkmate(color_to_move):
            winner = "Black" if color_to_move == Color.WHITE else "White"
            self.game_over_message = f"Checkmate! {winner} wins."
        elif self.game.is_stalemate(color_to_move):
            self.game_over_message = "Stalemate! Draw."

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = BOARD_LIGHT if (row + col) % 2 == 0 else BOARD_DARK
                pygame.draw.rect(self.screen, color,
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        if self.selected_square:
            sr, sc = self.selected_square
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (sc * SQUARE_SIZE, sr * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game.board.get_piece(row, col)
                if piece:
                    text = piece.piece_type.value
                    color = WHITE if piece.color == Color.WHITE else BLACK
                    self.draw_text_center(text,
                                          col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                          row * SQUARE_SIZE + SQUARE_SIZE // 2,
                                          color)

    def draw_text_center(self, text, x, y, color, size=24):
        font = pygame.font.SysFont("arial", size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)

    def draw_button(self, text, x, y):
        width, height = 220, 40
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        pygame.draw.rect(self.screen, PURPLE, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        self.draw_text_center(text, x, y, BLACK)
        return rect

    def draw_game_over_overlay(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        self.draw_text_center(self.game_over_message, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20, WHITE, 32)
        replay_rect = self.draw_button("Replay", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
        quit_rect = self.draw_button("Quit to Main Menu", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)

        pygame.display.flip()

        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_rect.collidepoint(event.pos):
                        self.game = Game()
                        self.game_over_message = None
                        waiting = False
                    elif quit_rect.collidepoint(event.pos):
                        self.game = Game()
                        self.game_over_message = None
                        waiting = False
                        self.show_main_menu()

            self.clock.tick(30)
