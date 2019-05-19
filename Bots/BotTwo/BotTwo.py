import random
from reconchess import *
import time


class BotTwo(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.opponent_color = None
        self.move_num = 0
        self.my_piece_captured_square = None
        self.opp_king_captured = False
        self.capture_allowed = False
        self.depth = 3
        
    def handle_game_start(self, color: Color, board: chess.Board):
        self.board = board
        self.color = color
        self.capture_allowed = False
        self.depth = 3
        
        if self.color == chess.WHITE:
            self.opponent_color = chess.BLACK
        else:
            self.opponent_color = chess.WHITE
        
    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        # if the opponent captured our piece, remove it from our board.
        self.my_piece_captured_square = capture_square
        if captured_my_piece:
            self.board.remove_piece_at(capture_square)

    def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> Square:
        coin = random.randint(0, 100)
        print("MOVE NUMBER", self.move_num+1)
        if self.opp_king_captured != False:
            square_to_return = self.opp_king_captured
            if coin > 80:
                square_to_return = square_to_return +1
            else:
                square_to_return = square_to_return-1
            self.opp_king_captured = False
            return square_to_return
        # sense if out piece was captured
        if self.my_piece_captured_square:
            return self.my_piece_captured_square
        
        elif(self.move_num == 2):
            #print("THIS HAPPENED")
            #print()
            #print()
            #print()
            return (52 if self.color == chess.BLACK else 12) 
        else:
            enemy_king_square = self.board.king(self.opponent_color)
            if self.move_num == 6 and (enemy_king_square == 60 or enemy_king_square == 4) and coin < 65:  
                return (52 if enemy_king_square == 60 else 13)
            if self.move_num > 6 and (enemy_king_square == 60 or enemy_king_square == 4) and coin < 65:  
                return (enemy_king_square + 1 - 8 if enemy_king_square == 60 else enemy_king_square + 9)
            elif(enemy_king_square == None):
                if coin < 60:
                    return (62 - 8 if self.opponent_color == chess.BLACK else 6 + 8)
                else:
                    return (58 - 8 if self.opponent_color == chess.BLACK else 2 + 8)
       
        if(coin >= 65 and coin <= 90):
            my_king_square = self.board.king(self.color)
            return (my_king_square + 8 if self.color == chess.WHITE else my_king_square - 8)
        # otherwise, random sense action
        for square, piece in self.board.piece_map().items():
            if piece.color == self.color:
                sense_actions.remove(square)
        return random.choice(sense_actions)

    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        # add changes to board, if any
        for square, piece in sense_result:
            self.board.set_piece_at(square, piece)
                    
    def handle_king_attacked(self, board):
        #print("HANDLING...")
        for move in board.pseudo_legal_moves:
            if (not board.is_into_check(move)):
                print("Handle move...", move)
                return move
        
        return None
        
    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        now = time.time()
        self.move_num += 1
        print(self.board)
        if(self.board.turn == self.opponent_color):
            self.board.push(chess.Move.null())  
                    
        enemy_king_square = self.board.king(self.opponent_color)
        #print("Enemy king square is", enemy_king_square)
        if enemy_king_square:
            # if there are any ally pieces that can take king, execute one of those moves
            enemy_king_attackers = self.board.attackers(self.color, enemy_king_square)
            if enemy_king_attackers:
                print("Attacking enemy king")
                attacker_square = enemy_king_attackers.pop()
                #self.board.push(chess.Move(attacker_square, enemy_king_square))
                self.opp_king_captured = enemy_king_square
                return chess.Move(attacker_square, enemy_king_square)

        my_king_square = self.board.king(self.color)
        if my_king_square:
            my_king_attackers = self.board.attackers(self.opponent_color, my_king_square)
            if my_king_attackers:
                print("My king attacked")
                move = self.handle_king_attacked(self.board.copy())
                if move != None:
                    return move
        
        found, move = self.king_path(self.board.copy(), 0, self.depth, seconds_left - (time.time() - now))
        print("BEST MOVE IS:", move)
        #print("Capture allowed:", self.capture_allowed)
        if move == None:
            self.capture_allowed = True
            found, move = self.king_path(self.board.copy(), 0, self.depth, seconds_left - (time.time() - now))
            self.capture_allowed = False
        if found and move in move_actions:
            return move
            
        return random.choice(move_actions + [None])

    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                           captured_opponent_piece: bool, capture_square: Optional[Square]):
        if(self.board.turn == self.opponent_color):
            self.board.push(chess.Move.null())
        if taken_move is not None:
            print("In handle move result")
            self.board.push(taken_move)
        elif(requested_move != None):
            self.board.push(requested_move)
                
    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
                        game_history: GameHistory):
        pass
               
        
    def king_path(self, board, depth, max_depth, time_remaining):
        now = time.time()
        
        if time_remaining < 0.1:
            return None, 999999
        
        if board.turn != self.color:
            board.push(chess.Move.null())
        '''
        Check if opponent's king is attacked
        '''
        enemy_king_square = board.king(self.opponent_color)
        if enemy_king_square:
            # if there are any ally pieces that can take king, execute one of those moves
            enemy_king_attackers = board.attackers(self.color, enemy_king_square)
            if enemy_king_attackers:
                #print("ENEMY_KING_SQUARE:", enemy_king_square)
                
                attacker_square = enemy_king_attackers.pop()
                #print("ATTACKER_SQUARE:", attacker_square)
                #print(chess.Move(attacker_square, enemy_king_square))                
                
                return True, depth
                
        if depth == max_depth:
            #print("FALSE")
            return False, depth
  
        '''
        if opponent's king is not attacked right now, go deeper in search
        '''
        path_found = False
        best_move = None
        smallest_depth = 9999999
        capture = False
        '''
        Look at every move in the move list
        '''
        for move in board.generate_pseudo_legal_moves():
            #print("DEPTH:", depth,"MOVE", move)
            if(not board.is_capture(move) or self.capture_allowed):
            
                board.push(move)

                found, candidate_depth = self.king_path(board.copy(), depth+1, max_depth, time_remaining - (time.time() - now))
                if found:
                    #print(move)
                    path_found = True
                    #print(board)
                    
                    #return found, move
                    coin = random.randint(0,100)
                    if(candidate_depth < smallest_depth or (candidate_depth == smallest_depth and coin > 30)):
                        #print("DEPTH IS", candidate_depth)
                        smallest_depth = candidate_depth
                        #print("SMALLEST DEPTH:", smallest_depth)
                        best_move = move
                board.pop()
                if(board.turn != self.color):
                    board.pop()
        if depth > 0:        
            return path_found, smallest_depth
        else:
            return path_found, best_move
        
