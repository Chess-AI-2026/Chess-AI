import pygame
import sys
import random

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        # tracks if the game has ended
        self.game_over_msg = None 
        self.font = pygame.font.SysFont('monospace', 48, bold=True)

        self.state = 'MENU'      # 'MENU', 'PLAYING', 'PAUSED'
        self.game_mode = 'local' # 'local', 'easy', 'medium', 'hard'

    def draw_button(self, text, x, y, width, height):
        mouse_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, width, height)
        
        color = (100, 100, 100) if rect.collidepoint(mouse_pos) else (60, 60, 60)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=10)
        
        btn_font = pygame.font.SysFont('monospace', 30, bold=True)
        lbl = btn_font.render(text, 1, (255, 255, 255))
        lbl_pos = (x + width//2 - lbl.get_width()//2, y + height//2 - lbl.get_height()//2)
        self.screen.blit(lbl, lbl_pos)
        
        return rect

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            if self.state == 'MENU':
                screen.fill((40, 40, 40)) # makes dark gray background
                title = self.font.render('CHESS AI', 1, (255, 255, 255))
                screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

                # buttons
                btn_local = self.draw_button('Local PvP', WIDTH//2 - 125, 250, 250, 60)
                btn_easy = self.draw_button('AI - Easy', WIDTH//2 - 125, 350, 250, 60)
                btn_med = self.draw_button('AI - Medium', WIDTH//2 - 125, 450, 250, 60)
                btn_hard = self.draw_button('AI - Hard', WIDTH//2 - 125, 550, 250, 60)
                btn_quit  = self.draw_button('Quit', WIDTH//2 - 125, 650, 250, 60)

                # menu Event Loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # checks which button was clicked
                        if btn_local.collidepoint(event.pos):
                            self.game_mode = 'local'
                            self.state = 'PLAYING'
                        elif btn_easy.collidepoint(event.pos):
                            self.game_mode = 'easy'
                            self.state = 'PLAYING'
                        elif btn_med.collidepoint(event.pos):
                            self.game_mode = 'medium'
                            self.state = 'PLAYING'
                        elif btn_hard.collidepoint(event.pos):
                            self.game_mode = 'hard'
                            self.state = 'PLAYING'
                        elif btn_quit.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        
                        # resets the board so a fresh game starts
                        if self.state == 'PLAYING':
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            self.game_over_msg = None

            elif self.state == 'PAUSED':
                # draw the board in the background so you can still see the game
                game.show_bg(screen)
                game.show_pieces(screen)
                
                # dark transparent overlay
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(200)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                title = self.font.render('PAUSED', 1, (255, 255, 255))
                screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))

                btn_resume = self.draw_button('Resume', WIDTH//2 - 125, 350, 250, 60)
                btn_menu = self.draw_button('Main Menu', WIDTH//2 - 125, 450, 250, 60)

                # pause event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'PLAYING'
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if btn_resume.collidepoint(event.pos):
                            self.state = 'PLAYING'
                        elif btn_menu.collidepoint(event.pos):
                            self.state = 'MENU'

            elif self.state == 'PLAYING':
                # show methods
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.game_over_msg:
                            continue # Disable board clicks if the game is over
                    
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # if clicked square has a piece ?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece

                            # valid piece (color) ?
                            if piece.color == game.next_player:
                                if self.game_mode != 'local' and piece.color == 'black':
                                    continue
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods 
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                
                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)
                
                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                    
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # valid move ?
                            if board.valid_move(dragger.piece, move):
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)                            

                                # sounds
                                game.play_sound(captured)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()

                                # check for checkmate or stalemate
                                self.game_over_msg = game.check_game_over()
                    
                        dragger.undrag_piece()
                
                    # key press
                    elif event.type == pygame.KEYDOWN:

                        # pausing
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'PAUSED'
                    
                        # changing themes
                        if event.key == pygame.K_t:
                            game.change_theme()

                         # changing themes
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            self.game_over_msg = None

                    # quit application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if self.game_over_msg:
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.set_alpha(150)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))

                    lbl = self.font.render(self.game_over_msg, 1, (255, 255, 255))
                    lbl_pos = (WIDTH // 2 - lbl.get_width() // 2, HEIGHT // 2 - lbl.get_height() // 2)
                    screen.blit(lbl, lbl_pos)
                
                pygame.display.update() 

                if self.game_mode != 'local' and game.next_player == 'black' and not self.game_over_msg:
                    from ai import AI
                    ai = AI(self.game_mode)
                
                    if self.game_mode == 'easy':
                        moves = ai.get_all_moves(board, 'black')
                        best_move = random.choice(moves) if moves else None
                    else:
                        eval, best_move = ai.minimax(board, ai.depth, float('-inf'), float('inf'), False)
                
                    if best_move:
                        initial_sq = best_move.initial
                        piece = board.squares[initial_sq.row][initial_sq.col].piece
                    
                        captured = board.squares[best_move.final.row][best_move.final.col].has_piece()
                        board.move(piece, best_move)
                        board.set_true_en_passant(piece)
                    
                        game.play_sound(captured)
                        game.next_turn()
                        self.game_over_msg = game.check_game_over()

            pygame.display.update()
        

main = Main()
main.mainloop()