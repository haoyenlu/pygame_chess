import pygame


class Piece:
    def __init__(self,block_size,color,name):
        self.block_size = block_size
        self.color = color
        self.click = False
        self.is_moved = False
        self.name = name
    
    def __str__(self):
        return f"{self.color} {self.name} at {self.rect.center}"

    def get_position(self):
        return self.rect.center
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color

    def load_image(self,image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image,(self.block_size,self.block_size))
        self.rect = self.image.get_rect()


    def drag(self):
        self.rect.center = pygame.mouse.get_pos()

    def move_to(self,position):
        self.rect.center = position
    
    def set_clicked(self,clicked):
        self.click = clicked

    def set_is_moved(self,moved):
        self.is_moved = moved

    def update(self,screen):
        if self.click == True:
            self.drag()
        screen.blit(self.image,self.rect)


    
class Pawn(Piece):
    def __init__(self,block_size,color,position):
        super().__init__(block_size,color,'pawn')
        self.load_image()
        self.move_to(position)

    def load_image(self):
        if self.color == "white":
            super().load_image('images/pawn_white.png')
        else:
            super().load_image('images/pawn_black.png')
    

    def get_legal_move_square(self):
        if self.color == 'white' and self.is_moved == False:
            legal_move = [(-1,0),(-2,0)] # first is row, second is column -> same column different row
        elif self.color == 'white' and self.is_moved == True:
            legal_move = [(-1,0)]
        elif self.color == 'black' and self.is_moved == False:
            legal_move = [(1,0),(2,0)]  # first is row, second is column -> same column different row
        elif self.color == 'black' and self.is_moved == True:
            legal_move = [(1,0)]
        
        return legal_move
    
    def get_capture_move_square(self):
        if self.color == 'white':
            capture_move = [(-1,1),(-1,-1)] # first is row, second is column -> same column different row
        elif self.color == 'black':
            capture_move = [(1,1),(1,-1)]  # first is row, second is column -> same column different row       

        return capture_move




class Horse(Piece):
    def __init__(self,block_size,color,position):
        super().__init__(block_size,color,'horse')
        self.load_image()
        self.move_to(position)

    def load_image(self):
        if self.color == "white":
            super().load_image('images/horse_white.png')
        else:
            super().load_image('images/horse_black.png')

    def get_legal_move_square(self):
        legal_move = [(1,2),(2,1),(-1,2),(2,-1),(-2,1),(1,-2),(-2,-1),(-1,-2)]

        return legal_move
    

class Bishop(Piece):
    def __init__(self,block_size,color,position):
        super().__init__(block_size,color,'bishop')
        self.load_image()
        self.move_to(position)

    def load_image(self):
        if self.color == "white":
            super().load_image('images/bishop_white.png')
        else:
            super().load_image('images/bishop_black.png')

    def get_legal_move_square(self):
        legal_move = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
        (-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6),(-7,-7),
        (-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6),(-7,7),
        (1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6),(7,-7)]

        return legal_move

class Rook(Piece):
    def __init__(self,block_size,color,position):
        super().__init__(block_size,color,'rook')
        self.load_image()
        self.move_to(position)

    def load_image(self):
        if self.color == "white":
            super().load_image('images/rook_white.png')
        else:
            super().load_image('images/rook_black.png')

    def get_legal_move_square(self):
        legal_move = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
        (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
        (0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),
        (-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0)]

        return legal_move


class King(Piece):
    def __init__(self,block_size,color,position):
        super().__init__(block_size,color,'king')
        self.load_image()
        self.move_to(position)

    def load_image(self):
        if self.color == "white":
            super().load_image('images/king_white.png')
        else:
            super().load_image('images/king_black.png')

    def get_legal_move_square(self):
        legal_move = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        return legal_move


class Queen(Piece):
    def __init__(self,block_size,color,position):
        super().__init__(block_size,color,'queen')
        self.load_image()
        self.move_to(position)

    def load_image(self):
        if self.color == "white":
            super().load_image('images/queen_white.png')
        else:
            super().load_image('images/queen_black.png')

    def get_legal_move_square(self):
        legal_move = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
        (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
        (0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),
        (-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),
        (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
        (-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6),(-7,-7),
        (-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6),(-7,7),
        (1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6),(7,-7)]

        return legal_move



        

    

