import pygame
from game import Game
from pieces import Color, PieceType
from board import BOARD_SIZE

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
SQUARE_SIZE = WINDOW_WIDTH // BOARD_SIZE

BOARD_LIGHT = (240, 217, 181)
BOARD_DARK = (181, 136, 99)

Brown = (240, 217, 181)
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

        self.mode = "pvp"
        self.ai_difficulty = "easy"
        self.player_color = Color.WHITE

    def run(self):
        self.show_main_menu()
        while self.running:
            self.handle_game_loop()
        pygame.quit()

    def show_main_menu(self):
        in_menu = True
        while in_menu and self.running:
            self.screen.fill((181, 136, 99))
            self.draw_text_center("Chess", WINDOW_WIDTH // 2, 80, WHITE, 36)

            pvp_rect = self.draw_button("Player vs Player", WINDOW_WIDTH // 2, 200)
            ai_rect = self.draw_button("Play vs AI", WINDOW_WIDTH // 2, 260)
            quit_rect = self.draw_button("Quit", WINDOW_WIDTH // 2, 320)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_menu = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_rect.collidepoint(event.pos):
                        self.mode = "pvp"
                        self.game = Game()
                        self.game_over_message = None
                        in_menu = False

                    elif ai_rect.collidepoint(event.pos):
                        self.mode = "ai"
                        self.choose_ai_difficulty()
                        self.choose_player_color()
                        self.game = Game()
                        self.game_over_message = None
                        in_menu = False

                    elif quit_rect.collidepoint(event.pos):
                        self.running = False
                        in_menu = False

            self.clock.tick(30)

    def choose_ai_difficulty(self):
        choosing = True
        while choosing and self.running:
            self.screen.fill((181, 136, 99))
            self.draw_text_center("Choose AI Difficulty", WINDOW_WIDTH // 2, 80, WHITE, 32)

            easy_rect = self.draw_button("Easy", WINDOW_WIDTH // 2, 200)
            med_rect = self.draw_button("Medium", WINDOW_WIDTH // 2, 260)
            hard_rect = self.draw_button("Hard", WINDOW_WIDTH // 2, 320)
            back_rect = self.draw_button("Back", WINDOW_WIDTH // 2, 380)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    choosing = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rect.collidepoint(event.pos):
                        self.ai_difficulty = "easy"
                        choosing = False

                    elif med_rect.collidepoint(event.pos):
                        self.ai_difficulty = "medium"
                        choosing = False

                    elif hard_rect.collidepoint(event.pos):
                        self.ai_difficulty = "hard"
                        choosing = False

                    elif back_rect.collidepoint(event.pos):
                        return

            self.clock.tick(30)

    def choose_player_color(self):
        choosing = True
        while choosing and self.running:
            self.screen.fill((181, 136, 99))
            self.draw_text_center("Choose Your Color", WINDOW_WIDTH // 2, 80, WHITE, 32)

            white_rect = self.draw_button("Play as White", WINDOW_WIDTH // 2, 200)
            black_rect = self.draw_button("Play as Black", WINDOW_WIDTH // 2, 260)
            random_rect = self.draw_button("Random", WINDOW_WIDTH // 2, 320)
            back_rect = self.draw_button("Back", WINDOW_WIDTH // 2, 380)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    choosing = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if white_rect.collidepoint(event.pos):
                        self.player_color = Color.WHITE
                        choosing = False

                    elif black_rect.collidepoint(event.pos):
                        self.player_color = Color.BLACK
                        choosing = False

                    elif random_rect.collidepoint(event.pos):
                        import random
                        self.player_color = random.choice([Color.WHITE, Color.BLACK])
                        choosing = False

                    elif back_rect.collidepoint(event.pos):
                        return

            self.clock.tick(30)

    def handle_game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over_message is None:
                if self.mode == "pvp" or self.game.board.to_move == self.player_color:
                    self.handle_click(event.pos)

        if self.mode == "ai" and self.game_over_message is None:
            if self.game.board.to_move != self.player_color:
                self.handle_ai_move()

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

    def handle_ai_move(self):
        ai_color = Color.BLACK if self.player_color == Color.WHITE else Color.WHITE

        if self.ai_difficulty == "easy":
            move = self.game.ai_easy(ai_color)
        elif self.ai_difficulty == "medium":
            move = self.game.ai_medium(ai_color)
        else:
            move = self.game.ai_hard(ai_color)

        if move:
            piece = self.game.board.get_piece(move.start_row, move.start_col)

            if (
                piece is not None and
                piece.piece_type == PieceType.PAWN and
                (
                    (piece.color == Color.WHITE and move.end_row == 0) or
                    (piece.color == Color.BLACK and move.end_row == 7)
                )
            ):
                move.promotion_piece_type = PieceType.QUEEN

            self.game.board.make_move(move)

        self.check_endgame()

    def choose_promotion(self, move):
        choosing = True
        options = [
            ("Queen", PieceType.QUEEN),
            ("Rook", PieceType.ROOK),
            ("Bishop", PieceType.BISHOP),
            ("Knight", PieceType.KNIGHT)
        ]

        while choosing and self.running:
            self.screen.fill((181, 136, 99))
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
                            var = False
                            return

            self.clock.tick(30)

    def check_endgame(self):
        color_to_move = self.game.board.to_move
        if self.game.is_checkmate(color_to_move):
            winner = "Black" if color_to_move == Color.WHITE else "White"
            self.game_over_message = f"Checkmate! {winner} wins."
        elif self.game.is_stalemate(color_to_move):
            self.game_over_message = "Stalemate Draw."

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
        pygame.draw.rect(self.screen, Brown, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        self.draw_text_center(text, x, y, BLACK)
        return rect

    def draw_game_over_overlay(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        self.draw_text_center(self.game_over_message,
                              WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20, WHITE, 32)

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
