import pygame


class EventHandler:
    def __init__(self,screen,chess,engine):
        self.running = True
        self.screen = screen
        self.chess = chess
        self.engine = engine
        self.clicked_piece = None
        self.clicked_position = None

    def initialize(self):
        self.chess.board.print_board_pieces()

    def get_event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.quit_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up(event)

        
            
    def quit_game(self):
        self.running = False

    def mouse_button_down(self,event):
        if self.chess.promoting == False: # if not promoting
            for piece in self.chess.pieces:
                    if piece.rect.collidepoint(event.pos):
                        piece.set_clicked(True)
                        self.clicked_position = self.chess.board.get_nearest_position(event.pos)
                        self.clicked_piece = piece
                        self.engine.set_clicked_piece_and_position(piece,self.clicked_position)
                        # highlight legal move
                        self.chess.set_highlight(True)
                    
                        break


    def mouse_button_up(self,event):
        if self.chess.promoting == False:
            if self.clicked_piece != None:
                self.clicked_piece.set_clicked(False)
                self.chess.set_highlight(False)
                new_position = self.chess.board.get_nearest_position(event.pos)
                self.chess.move_piece(self.clicked_piece,self.clicked_position,new_position)
                self.clicked_piece = None
        else:
            for p in self.chess.promotion_pieces:
                if p.rect.collidepoint(event.pos):
                    self.chess.promoting_to(p)
            self.chess.set_promoting(False)

