import copy
import random

class AI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        
        # defines how many moves the AI looks knows ahead of itself
        if difficulty == 'medium':
            self.depth = 2
        elif difficulty == 'hard':
            self.depth = 3
        else:
            self.depth = 1 # Easy mode

    def eval(self, board):
        # checks who is winning
        evaluation = 0
        for row in range(8):
            for col in range(8):
                if board.squares[row][col].has_piece():
                    evaluation += board.squares[row][col].piece.value
        return evaluation

    def get_all_moves(self, board, color):
        # makes list of every legal move available for the color a specific color
        moves = []
        for row in range(8):
            for col in range(8):
                if board.squares[row][col].has_team_piece(color):
                    piece = board.squares[row][col].piece
                    piece.clear_moves()
                    board.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        moves.append(move)
        return moves

    def order_moves(self, board, moves):
        def score_move(move):
            score = 0
            final_square = board.squares[move.final.row][move.final.col]
            
            if final_square.has_piece():
                captured_piece = final_square.piece
                moving_piece = board.squares[move.initial.row][move.initial.col].piece
                score = (10 * abs(captured_piece.value)) - abs(moving_piece.value)
                
            return score
            
        return sorted(moves, key=score_move, reverse=True)

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        # minimax AI brain: Simulates future moves to find the best outcome
        if depth == 0:
            return self.eval(board), None
        
        if maximizing_player: # white wants highest positive score
            max_eval = float('-inf')
            best_move = None
            moves = self.get_all_moves(board, 'white')
            moves = self.order_moves(board, moves)

            for move in moves:
                # seperate temporary board
                temp_board = copy.deepcopy(board)
                temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
                
                # simulation
                temp_board.move(temp_piece, move, testing=True)
                
                # recursion
                evaluation = self.minimax(temp_board, depth - 1, alpha, beta, False)[0]
                
                # memory Remember
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                    
                # Alpha-Beta Pruning
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else: # black (AI) wants the lowest negative score
            min_eval = float('inf')
            best_move = None
            moves = self.get_all_moves(board, 'black')
            moves = self.order_moves(board, moves)

            for move in moves:
                temp_board = copy.deepcopy(board)
                temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
                temp_board.move(temp_piece, move, testing=True)
                
                evaluation = self.minimax(temp_board, depth - 1, alpha, beta, True)[0]
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                    
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move