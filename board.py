import pygame
import color

class Board:
    def __init__(self,block_size=30,origin_x = 0,origin_y = 0):
        self.block_size = block_size
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.surface = pygame.Surface((block_size*9,block_size*9))
        self.board_rect = [[0] * 8 for i in range(8)] # board pygame rect
        self.board_position = [[0] * 8 for i in range(8)] # pixel vector of every grid
        self.board_pieces = [['/'] * 8 for i in range(8)] # pieces
        self.initialize_position()
        self.initialize_board_rect()
        self.font = pygame.font.SysFont('arial',int(self.block_size/2))

    def initialize_position(self):
        # initialize pixel position
        for i in range(8):
            for j in range(8):
                x = self.origin_x + (j + 0.5) * self.block_size
                y = self.origin_y + (i + 0.5) * self.block_size

                self.board_position[i][j] = (x,y)

    def initialize_board_rect(self):
        # initialize board rect
        for i in range(8):
            for j in range(8):
                x = i * self.block_size
                y = j * self.block_size

                rect = pygame.Rect(x,y,self.block_size,self.block_size)
                self.board_rect[i][j] = rect

    def draw_board(self,screen):
        # draw board rect
        for i in range(8):
            for j in range(8):
                c = color.WHITE if (i + j) % 2 == 0 else color.GRAY
                pygame.draw.rect(self.surface,c,self.board_rect[i][j],0)
        # draw board number 
        for i in range(8):
            number_block = self.font.render(str(i+1),True,(255,255,255))
            number_rect = number_block.get_rect(center=((i+0.5) * self.block_size,(8.3) * self.block_size))
            self.surface.blit(number_block,number_rect)
            alpha_block = self.font.render(chr(i+ord('A')),True,(255,255,255))
            alpha_rect = alpha_block.get_rect(center=((8.3) * self.block_size,(i+0.5) * self.block_size))
            self.surface.blit(alpha_block,alpha_rect)
        screen.blit(self.surface,(self.origin_x,self.origin_y))

    def get_nearest_position(self,position):
        # get nearest board pixel position
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

    def get_board_position(self,position):  
        # get board square by pixel position
        board_position = (-1,-1)

        for i in range(8):
            for j in range(8):
                if position == self.board_position[i][j]:
                    board_position = (i,j)

        return board_position

    def move_piece(self,prev_position,new_position):
        # move piece on board piece
        self.board_pieces[new_position[0]][new_position[1]] = self.board_pieces[prev_position[0]][prev_position[1]]
        self.board_pieces[prev_position[0]][prev_position[1]] = '/'

    def draw_red_circle(self,screen,positions):
        # draw red circle on board for highlight
        for pos in positions:
            pygame.draw.circle(screen,(255,0,0),self.board_position[pos[0]][pos[1]],7)

    def draw_promotion_square(self,screen,position):
        # draw promotion square
        rect_positions = []
        prev_x = position[0]
        prev_y = position[1] - self.block_size
        screen_x,screen_y = screen.get_size()
        for i in range(4):
            c = color.BROWN if i % 2 == 0 else color.LIGHT_BROWN
            x = prev_x
            y = prev_y +  self.block_size
            if y > screen_y:
                x = prev_x + self.block_size
                y = position[1]
            rect = pygame.Rect(x,y,self.block_size,self.block_size)
            pygame.draw.rect(screen,c,rect,0)
            rect_positions.append((x,y))
            prev_x = x
            prev_y = y
    
        return rect_positions
        
    def print_board_pieces(self):
        # print board pieces on console
        print('-'* 60)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board_pieces]))
        print('-'* 60)
    
    def print_board_position(self):
        # print board pixel position on console
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

        
        


        
