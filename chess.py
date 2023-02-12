import pygame
import board
import piece
import position
import color

# Pawn - p
# Horse - h
# Bishop - b
# Rook - r
# Queen - q
# King - k

# Black - bl
# White - w



class Chess:
    def __init__(self):
        self.highlight = False
        self.promoting = False
        self.promoting_pawn = None
        self.pieces = []
        self.promotion_pieces = []
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


    def initialize_pieces_position(self,block_size):

        # Board position
        self.board.board_pieces = position.INITIAL_POSITION
        self.turn = "white"

        # Pieces position
        for i in range(8):
            for j in range(8):
                if self.board.board_pieces[i][j] == "w_p": # white pawn
                    self.pieces.append(piece.Pawn(block_size,"white",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "bl_p": # black pawn
                    self.pieces.append(piece.Pawn(block_size,"black",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "w_h": # white horse
                    self.pieces.append(piece.Horse(block_size,"white",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "bl_h": # black horse
                    self.pieces.append(piece.Horse(block_size,"black",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "w_b": # white bishop
                    self.pieces.append(piece.Bishop(block_size,"white",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "bl_b": # black bishop
                    self.pieces.append(piece.Bishop(block_size,"black",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "w_r": # white rook
                    self.pieces.append(piece.Rook(block_size,"white",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "bl_r": # black rook
                    self.pieces.append(piece.Rook(block_size,"black",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "w_q": # white queen
                    self.pieces.append(piece.Queen(block_size,"white",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "bl_q": # black queen
                    self.pieces.append(piece.Queen(block_size,"black",(self.board.board_position[i][j])))
                
                elif self.board.board_pieces[i][j] == "w_k": # white king
                    self.pieces.append(piece.King(block_size,"white",(self.board.board_position[i][j])))

                elif self.board.board_pieces[i][j] == "bl_k": # black king
                    self.pieces.append(piece.King(block_size,"black",(self.board.board_position[i][j])))
        
        # calculate legal move beforehand
        self.cal_all_piece_legal_move()


    def move_piece(self,piece,prev_position,new_position): 
        # Move pieces to new square

        # check if move is legal
        if self.check_if_move_legal(piece,prev_position,new_position) and self.is_turn(piece): 
            # check if there is another piece on the square
            if not self.check_if_squared_occupied(new_position): # no piece
                self.ordinary_move(piece,prev_position,new_position)
                # castle
                if piece.name == "king" and abs(new_position[1] - prev_position[1]) == 2: 
                    self.castle(piece,new_position)

                # en passant capture
                if piece.name == "pawn" and abs(new_position[0]-prev_position[0]) == 1 and abs(new_position[1] - prev_position[1]) == 1:
                    if piece.color == "white" :
                        if self.board.board_pieces[new_position[0] + 1][new_position[1]] == "bl_p":
                            black_pawn = self.get_piece_on_square((new_position[0] + 1,new_position[1]))
                            self.capture(black_pawn)
                            self.board.board_pieces[new_position[0] + 1][new_position[1]] = '/'
                    elif piece.color == "black" :
                        if self.board.board_pieces[new_position[0] - 1][new_position[1]] == "w_p":
                            white_pawn = self.get_piece_on_square((new_position[0] - 1,new_position[1]))
                            self.capture(white_pawn)
                            self.board.board_pieces[new_position[0]-1][new_position[1]] = '/'
                    
                
                # promotion
                if piece.name == 'pawn' and piece.color == 'white' and new_position[0] == 0:
                    self.promoting = True
                elif piece.name == 'pawn' and piece.color == "black" and new_position[0] == 7:
                    self.promoting = True
                
                # calculate legal move for every piece
                self.cal_all_piece_legal_move()
                # add en passant square 
                if piece.name == "pawn" and abs(new_position[0] - prev_position[0]) == 2:
                    if piece.color == "white":
                        if self.board.board_pieces[new_position[0]][new_position[1]-1] == "bl_p":
                            black_pawn = self.get_piece_on_square((new_position[0]+1,new_position[1]-1))
                            black_pawn.add_legal_move((new_position[0]+1,new_position[1]+1))
                        if self.board.board_pieces[new_position[0]][new_position[1]+1] == "bl_p":
                            black_pawn = self.get_piece_on_square((new_position[0],new_position[1]+1))
                            black_pawn.add_legal_move((new_position[0]+1,new_position[1]))
                    elif piece.color == "black":
                        if self.board.board_pieces[new_position[0]][new_position[1]-1] == "w_p":
                            white_pawn = self.get_piece_on_square((new_position[0],new_position[1]-1))
                            white_pawn.add_legal_move((new_position[0]-1,new_position[1]))
                        if self.board.board_pieces[new_position[0]][new_position[1]+1] == "w_p":
                            white_pawn = self.get_piece_on_square((new_position[0],new_position[1]+1))
                            white_pawn.add_legal_move((new_position[0]-1,new_position[1]))
                

                # update move
                self.moves += 1
                # print move and piece
                print(f"move {self.moves}")
                self.board.print_board_pieces()
            
            else:
                another_piece = self.get_piece_on_square(new_position)
                if piece.color != another_piece.color: # check if the piece can be captured
                    # Capture peice
                    self.ordinary_move(piece,prev_position,new_position) 
                    self.capture(another_piece)

                    # promotion
                    if piece.name == 'pawn' and piece.color == 'white' and new_position[0] == 0:
                        self.promoting = True
                    elif piece.name == 'pawn' and piece.color == "black" and new_position[0] == 7:
                        self.promoting = True

                    # calculate all legal move for every piece
                    self.cal_all_piece_legal_move()
                    # update move and history
                    self.moves += 1

                    # print moves and piece
                    print(f"move {self.moves}")
                    self.board.print_board_pieces()

                else: # return original position
                    piece.move_to(self.board.board_position[prev_position[0]][prev_position[1]])

        # return original position
        else:
            piece.move_to(self.board.board_position[prev_position[0]][prev_position[1]])

    def ordinary_move(self,piece,prev_position,new_position):
        # ordinary move
        piece.move_to(self.board.board_position[new_position[0]][new_position[1]])
        self.board.move_piece(prev_position,new_position)
        if not piece.is_moved : piece.set_is_moved(True)
        self.turn = "white" if piece.color == "black" else "black"

    def check_if_move_legal(self,piece,prev_position,new_position):
        # check legal move
        if len(piece.legal_move) == 0:
            piece.set_legal_move(self.cal_piece_legal_move(piece,prev_position))
        if new_position not in piece.legal_move:
            return False
            
        return True
    
    def check_if_squared_occupied(self,new_position): 
        # check if squared is occupied by other pieces
        if self.board.board_pieces[new_position[0]][new_position[1]] == '/':
            return False

        return True

    def get_piece_on_square(self,position):
        # get the piece on square
        for p in self.pieces:
            if self.board.get_board_position(p.get_position()) == position:
                return p 
        
        return None

    def cal_all_piece_legal_move(self):
        for p in self.pieces:
            p.set_legal_move(self.cal_piece_legal_move(p,self.board.get_board_position(p.get_position())))

    def cal_piece_legal_move(self,piece,position):
        # calculate legal move
        piece_legal_move = piece.get_legal_move_square()
        piece_legal_move = [(position[0]+move[0],position[1]+move[1]) for move in piece_legal_move]

        # pawn legal capture move and en passant
        if piece.name == "pawn":
            # capture move
            capture_squares = piece.get_capture_move_square()
            for square in capture_squares:
                pos = (square[0]+position[0],position[1]+square[1])
                another_piece = self.get_piece_on_square(pos)
                if another_piece != None and another_piece.color != piece.color:
                    piece_legal_move.append(pos)


            

        # king legal castle move
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
        piece.set_legal_move(piece_legal_move_inbound)

        return piece_legal_move_inbound



    def capture(self,piece):
        # capture piece
        if piece.name == "king":
            self.win = "white" if piece.color == "black" else "black"
            print(self.win + " win!")
        outside_pos = self.outside_board.get_first_unoccupied_position()
        piece.move_to(outside_pos)
        piece.set_is_moved(True)
        self.outside_board.set_occupied(outside_pos)

    def promotion(self,screen,promoting_pawn):
        # promotion process
        self.promoting_pawn = promoting_pawn
        position = promoting_pawn.get_position()
        col = promoting_pawn.color
        block_s = promoting_pawn.block_size
        rect_positions = self.board.draw_promotion_square(screen,position)
        self.promotion_pieces = [piece.Queen(block_s,col,position = (rect_positions[0][0] + 0.5* block_s,rect_positions[0][1]  + 0.5* block_s)),
        piece.Rook(block_s,col,position = (rect_positions[1][0]  + 0.5* block_s,rect_positions[1][1]  + 0.5* block_s)),
        piece.Horse(block_s,col,position =(rect_positions[2][0]  + 0.5* block_s,rect_positions[2][1]  + 0.5* block_s)),
        piece.Bishop(block_s,col,position = (rect_positions[3][0]  + 0.5* block_s,rect_positions[3][1] + 0.5* block_s))]
        for p in self.promotion_pieces:
            screen.blit(p.image,p.rect)


    def promoting_to(self,promoting_piece):
        # pawn promoting to (promoting_piece)
        promoting_position = self.promoting_pawn.get_position()
        promoting_square = self.board.get_board_position(promoting_position)
        # delete promoting pawn
        for i,p in enumerate(self.pieces):
            if p.get_position() == promoting_position:
                del self.pieces[i]
                break
        
        self.pieces.append(promoting_piece)
        promoting_piece.move_to(promoting_position)

        # update board pieces
        if self.promoting_pawn.color == "white":
            if promoting_piece.name == "queen":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'w_q'
            elif promoting_piece.name == "horse":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'w_h'
            elif promoting_piece.name == "bishop":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'w_b'
            elif promoting_piece.name == "rook":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'w_r'
        elif self.promoting_pawn.color == "black":
            if promoting_piece.name == "queen":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'bl_q'
            elif promoting_piece.name == "horse":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'bl_h'
            elif promoting_piece.name == "bishop":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'bl_b'
            elif promoting_piece.name == "rook":
                self.board.board_pieces[promoting_square[0]][promoting_square[1]] = 'bl_r'



    def castle_move(self,piece,position):
        # return castle move
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
        # castle 
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

    def set_promoting(self,bool):
        self.promoting = bool

    def update(self,screen):
        self.board.draw_board(screen)
        self.outside_board.draw_board(screen)


    def print_piece_position_on_board(self):
        for p in self.pieces:
            print(f"{p.color} {p.name} on {self.board.get_board_position(p.get_position())}")

    def show_highlight(self,screen,piece):
        # highlight legal move position
        self.board.draw_red_circle(screen,piece.legal_move)

        
