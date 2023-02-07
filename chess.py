import pygame
import board
import piece
import engine

# Pawn - p
# Horse - h
# Bishop - b
# Rook - r
# Queen - q
# King - k

# Black - bl
# White - w


Initial_Board_Position = [['bl_r','bl_h','bl_b','bl_q','bl_k','bl_b','bl_h','bl_r'],
['bl_p','bl_p','bl_p','bl_p','bl_p','bl_p','bl_p','bl_p'],
['/','/','/','/','/','/','/','/'],
['/','/','/','/','/','/','/','/'],
['/','/','/','/','/','/','/','/'],
['/','/','/','/','/','/','/','/'],
['w_p','w_p','w_p','w_p','w_p','w_p','w_p','w_p'],
['w_r','w_h','w_b','w_q','w_k','w_b','w_h','w_r']]


class Chess:
    def __init__(self):
        self.highlight = False
        self.pieces = []
        self.board = None
        self.outside_board = None
        self.turn = "white"
        self.moves = 0
        self.win = None
    
    def instantiate_board(self,block_size =30,origin_x=0,origin_y=0):
        # Instantiate board
        self.board = board.Board(block_size,origin_x,origin_y)

    def instantiate_outside_board(self,origin_x = 10,origin_y = 10,block_size=50,block_row=5,block_col=5,color = (255,255,255)):
        self.outside_board = board.OutsiedBoard(origin_x,origin_y,block_size,block_row,block_col,color)

    def instantiate_pieces(self,block_size = 30):
        # Pawn
        for i in range(8):
            self.pieces.append(piece.Pawn(block_size,"white"))
            self.pieces.append(piece.Pawn(block_size,"black"))


        # Horse
        for i in range(2):
            self.pieces.append(piece.Horse(block_size,"white"))
            self.pieces.append(piece.Horse(block_size,"black"))

        # Bishops
        for i in range(2):
            self.pieces.append(piece.Bishop(block_size,"white"))
            self.pieces.append(piece.Bishop(block_size,"black"))

        # Rook
        for i in range(2):
            self.pieces.append(piece.Rook(block_size,"white"))
            self.pieces.append(piece.Rook(block_size,"black"))

        # Queen
        self.pieces.append(piece.Queen(block_size,"white"))
        self.pieces.append(piece.Queen(block_size,"black"))

        # King
        self.pieces.append(piece.King(block_size,"white"))
        self.pieces.append(piece.King(block_size,"black"))



    
    def initialize_pieces_position(self):

        # Board position
        self.board.board_pieces = Initial_Board_Position

        # Pieces position
        for piece in self.pieces:
            if piece.name == "pawn" and piece.color == "white" and piece.is_placed == False: # white pawn
                position = self.board.find_unoccupied_piece_square("w_p")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "pawn" and piece.color == "black" and piece.is_placed == False: # black pawn
                position = self.board.find_unoccupied_piece_square("bl_p")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "horse" and piece.color == "white" and piece.is_placed == False: # white horse
                position = self.board.find_unoccupied_piece_square("w_h")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "horse" and piece.color == "black" and piece.is_placed == False: # black horse
                position = self.board.find_unoccupied_piece_square("bl_h")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "bishop" and piece.color == "white" and piece.is_placed == False: # white bishop
                position = self.board.find_unoccupied_piece_square("w_b")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "bishop" and piece.color == "black" and piece.is_placed == False: # black bishop
                position = self.board.find_unoccupied_piece_square("bl_b")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "rook" and piece.color == "white" and piece.is_placed == False: # white rook
                position = self.board.find_unoccupied_piece_square("w_r")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "rook" and piece.color == "black" and piece.is_placed == False: # black bishop
                position = self.board.find_unoccupied_piece_square("bl_r")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "queen" and piece.color == "white" and piece.is_placed == False: # white queen
                position = self.board.find_unoccupied_piece_square("w_q")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "queen" and piece.color == "black" and piece.is_placed == False: # black queen
                position = self.board.find_unoccupied_piece_square("bl_q")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)
            
            elif piece.name == "king" and piece.color == "white" and piece.is_placed == False: # white king
                position = self.board.find_unoccupied_piece_square("w_k")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

            elif piece.name == "king" and piece.color == "black" and piece.is_placed == False: # black king
                position = self.board.find_unoccupied_piece_square("bl_k")
                piece.move_to(self.board.board_position[position[0]][position[1]])
                piece.set_placed(True)

    def move_piece(self,piece,prev_position,new_position): # Move pieces
        # check if move is legal
        if piece.is_placed == True:
            if self.check_if_move_legal(piece,prev_position,new_position) and self.is_turn(piece): # check if there is another piece on the square
                if not self.check_if_squared_occupied(new_position): # check if there is another piece on the square
                    self.ordinary_move(piece,prev_position,new_position)
                    if piece.name == "king" and abs(new_position[1] - prev_position[1]) == 2: # castle
                        self.castle(piece,new_position)

                
                else:
                    another_piece = self.get_piece_on_square(new_position)
                    if piece.color != another_piece.color: # check if the piece can be captured
                        self.ordinary_move(piece,prev_position,new_position)
                        self.capture(another_piece)
                    else:
                        piece.move_to(self.board.board_position[prev_position[0]][prev_position[1]])

            # return original position
            else:
                piece.move_to(self.board.board_position[prev_position[0]][prev_position[1]])

    def ordinary_move(self,piece,prev_position,new_position):
        piece.move_to(self.board.board_position[new_position[0]][new_position[1]])
        self.board.move_piece(prev_position,new_position)
        if not piece.is_moved : piece.set_is_moved(True)
        self.turn = "white" if piece.color == "black" else "black"

    def check_if_move_legal(self,piece,prev_position,new_position):
        # check legal move
        piece_legal_move = self.cal_piece_legal_move(piece,prev_position)
        if new_position not in piece_legal_move:
            return False
            
        return True
    
    def check_if_squared_occupied(self,new_position): 
        if self.board.board_pieces[new_position[0]][new_position[1]] == '/':
            return False

        return True

    def get_piece_on_square(self,position):
        for p in self.pieces:
            if self.board.get_board_position(p.get_position()) == position:
                return p 
        
        return None

    def cal_piece_legal_move(self,piece,position):
        piece_legal_move = piece.get_legal_move_square()
        piece_legal_move = [(position[0]+move[0],position[1]+move[1]) for move in piece_legal_move]

        # legal capture move
        if piece.name == "pawn":
            capture_squares = piece.get_capture_move_square()
            for square in capture_squares:
                pos = (square[0]+position[0],position[1]+square[1])
                another_piece = self.get_piece_on_square(pos)
                if another_piece != None and another_piece.color != piece.color:
                    piece_legal_move.append(pos)

        # legal castle move
        castle_move = self.castle_move(piece,position)
        for move in castle_move:
            piece_legal_move.append(move)


        # legal move on board
        block_square = []
        for move in piece_legal_move:
            if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0:
                block_square.append(move) 
            elif move[0] <= 7 and move[0] >= 0 and move[1] <=7 and move[1] >=0 and move not in block_square:
                if self.board.board_pieces[move[0]][move[1]] != '/':
                    another_piece = self.get_piece_on_square(move)
                    if another_piece != None and another_piece.color == piece.color: 
                        block_square.append(move)
                    if piece.name == "pawn" and move[1] == position[1] :
                        block_square.append(move)

                    # horizontal block
                    if move[0] == position[0]: # same row
                        if position[1] > move[1]:
                            for i in range(move[1]):
                                block_square.append((move[0],i))
                        elif position[1] < move[1]:
                            for i in range(move[1]+1,8):
                                block_square.append((move[0],i))

                    # vertical block
                    elif move[1] == position[1]: # same column
                        if position[0] > move[0]:
                            for i in range(move[0]):
                                block_square.append((i,move[1]))
                        elif position[0] < move[0]:
                            for i in range(move[0]+1,8):
                                block_square.append((i,move[1]))

                    # diagonal block
                    elif abs(move[0] - position[0]) == abs(move[1] - position[1]):
                        if position[0] > move[0] and position[1] > move[1]:
                            for i in range(1,move[0]+1):
                                block_square.append((move[0] - i,move[1]- i))
                        elif position[0] > move[0] and position[1] < move[1]:
                            for i in range(1,move[0]+1):
                                block_square.append((move[0] - i,move[1] + i))
                        elif position[0] <  move[0] and position[1] > move[1]:
                            for i in range(1,move[1]+1):
                                block_square.append((move[0] + i,move[1] - i))
                        elif position[0] <  move[0] and position[1] < move[1]:
                            for i in range(1,8-move[1]):
                                block_square.append((move[0] + i,move[1] + i))

        piece_legal_move_inbound = [move for move in piece_legal_move if move not in block_square]

        return piece_legal_move_inbound



    def capture(self,piece):
        if piece.name == "king":
            self.win = "white" if piece.color == "black" else "black"
            print(self.win + " win!")
        outside_pos = self.outside_board.get_first_unoccupied_position()
        piece.move_to(outside_pos)
        piece.set_placed(False)
        self.outside_board.set_occupied(outside_pos)

    def castle_move(self,piece,position):
        castle_move = []
        if piece.name == "king" and piece.is_moved == False:
            rook_1 = self.get_piece_on_square((position[0],position[1]+3))
            rook_2 = self.get_piece_on_square((position[0],position[1]-4))
            if rook_1 != None and rook_1.is_moved == False and self.board.board_pieces[position[0]][position[1]+1] == '/' and  self.board.board_pieces[position[0]][position[1]+2] == '/':
                castle_move.append((position[0],position[1]+2))
            if rook_2 != None and rook_2.is_moved == False and self.board.board_pieces[position[0]][position[1]-1] == '/' and  self.board.board_pieces[position[0]][position[1]-2] == '/' and  self.board.board_pieces[position[0]][position[1]-3] == '/':
                castle_move.append((position[0],position[1]-2))

        return castle_move
                

    def castle(self,piece,position):
        if position[1] == 6: # kingside
            rook = self.get_piece_on_square((position[0],7)) # kingside rook
            rook.move_to(self.board.board_position[position[0]][5])
            self.board.move_piece((position[0],7),(position[0],5))
        elif position[1] == 2:
            rook = self.get_piece_on_square((position[0],0)) # queenside rook
            rook.move_to(self.board.board_position[position[0]][3])
            self.board.move_piece((position[0],0),(position[0],3))


    def is_turn(self,clicked_piece):
        if clicked_piece.color == self.turn: return True
        return False


    def set_highlight(self,bool):
        self.highlight = bool

    def update(self,screen):
        self.board.draw_board(screen)
        self.outside_board.draw_board(screen)


    def print_piece_position_on_board(self):
        for p in self.pieces:
            print(f"{p.color} {p.name} on {self.board.get_board_position(p.get_position())}")

    def show_highlight(self,screen,piece,position):
        # highlight legal move position
        if piece.is_placed == True:
            piece_legal_move = self.cal_piece_legal_move(piece,position)
            self.board.draw_red_circle(screen,piece_legal_move)

        
