import pygame

class Board:
    def __init__(self,block_size=30,origin_x = 0,origin_y = 0):
        self.block_size = block_size
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.surface = pygame.Surface((block_size*8,block_size*8))
        self.board_rect = [[0] * 8 for i in range(8)] # board pygame rect
        self.board_position = [[0] * 8 for i in range(8)] # pixel vector of every grid
        self.board_pieces = [['/'] * 8 for i in range(8)] # pieces
        self.board_occupied = [[0] * 8 for i in range(8)] # 0 if not occupied - 1 if occupied
        self.initialize_position()
        self.initialize_board_rect()

    def initialize_position(self):
        for i in range(8):
            for j in range(8):
                x = self.origin_x + (j + 0.5) * self.block_size
                y = self.origin_y + (i + 0.5) * self.block_size

                self.board_position[i][j] = (x,y)

    def initialize_board_rect(self):
        for i in range(8):
            for j in range(8):
                x = i * self.block_size
                y = j * self.block_size

                rect = pygame.Rect(x,y,self.block_size,self.block_size)
                self.board_rect[i][j] = rect

    def draw_board(self,screen):
        for i in range(8):
            for j in range(8):
                color = (255,255,255) if (i + j) % 2 == 0 else (127,127,127)
                pygame.draw.rect(self.surface,color,self.board_rect[i][j],0)
        screen.blit(self.surface,(self.origin_x,self.origin_y))

    def get_nearest_position(self,position): # get nearest board position
        
        def get_distance(a,b):
            distance = 0
            for x,y in zip(a,b):
                distance += (x-y) ** 2
            
            distance = distance ** 0.5
            return distance

        nearest_board_position = (0,0)
        nearest_distance = 10000
        for i in range(8):
            for j in range(8):
                distance = get_distance(self.board_position[i][j],position)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_board_position = (i,j)

        return nearest_board_position  # return board position

    def get_board_position(self,position):  # get board position by pixel vector
        board_position = (-1,-1)

        for i in range(8):
            for j in range(8):
                if position == self.board_position[i][j]:
                    board_position = (i,j)

        return board_position

    def move_piece(self,prev_position,new_position):
        self.board_pieces[new_position[0]][new_position[1]] = self.board_pieces[prev_position[0]][prev_position[1]]
        self.board_pieces[prev_position[0]][prev_position[1]] = '/'
        self.print_board_pieces()
    
    def find_unoccupied_piece_square(self,piece):
        for i in range(8):
            for j in range(8):
                if self.board_pieces[i][j] == piece and self.board_occupied[i][j] == 0:
                    self.board_occupied[i][j] = 1
                    return (i,j)

    def draw_red_circle(self,screen,positions):
        for pos in positions:
            pygame.draw.circle(screen,(255,0,0),self.board_position[pos[0]][pos[1]],7)
    
        
    def print_board_pieces(self):
        print('-'* 60)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board_pieces]))
        print('-'* 60)
    
    def print_board_position(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board_position]))

        
class OutsiedBoard:
    def __init__(self,origin_x,origin_y,block_size=50,block_row=5,block_col=5,color = (255,255,255)):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.block_size = block_size
        self.block_row = block_row
        self.block_col = block_col
        self.color = color
        self.board_occupied = [[0] * block_col for i in range(block_row)]
        self.board_position = [[0] * block_col for i in range(block_row)]

        for i in range(block_row):
            for j in range(block_col):
                x = origin_x + (i+0.5) * block_size
                y = origin_y + (j+0.5) * block_size
                self.board_position[i][j] = (x,y)
    
    def draw_board(self,screen):                
        rect = pygame.Rect(self.origin_x,self.origin_y,(self.block_size * self.block_col),(self.block_size * self.block_row))
        pygame.draw.rect(screen,self.color,rect,0)
    
    def get_first_unoccupied_position(self):
        for i in range(self.block_row):
            for j in range(self.block_col):
                if self.board_occupied[i][j] == 0:
                    return (self.board_position[i][j])


    def set_occupied(self,position):
        for i in range(self.block_row):
            for j in range(self.block_col):
                if self.board_position[i][j] == position:
                    self.board_occupied[i][j] = 1

        
        


        
