class Engine:
    def __init__(self,chess,screen):
        self.screen = screen
        self.chess = chess
        self.clicked_piece = None
        self.clicked_position = None
            
    
    def update(self):
        self.chess.update(self.screen)

        for piece in self.chess.pieces:
            piece.update(self.screen)

        if self.chess.highlight == True and self.clicked_piece != None:
            self.chess.show_highlight(self.screen,self.clicked_piece,self.clicked_position)

        if self.chess.promoting == True:
            self.chess.promotion(self.screen,self.clicked_piece)

    def set_clicked_piece_and_position(self,piece,position):
        self.clicked_piece = piece
        self.clicked_position = position

        