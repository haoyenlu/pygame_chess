# Importing the library
import pygame

# Importing Class
import chess
import engine
import game_event
import color
 
# Initializing Pygame
pygame.init()
 

screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
screen.fill(color.WHITE)

block_size = 60
origin_x = 50
origin_y = 50
 
chess = chess.Chess()
chess.instantiate_board(block_size,origin_x,origin_y)
chess.instantiate_outside_board(origin_x + 8.5 * block_size,origin_y,block_size,5,5,(0,200,200,0.5))
chess.initialize_pieces_position(block_size)

engine = engine.Engine(chess,screen)

event_handler = game_event.EventHandler(screen,chess,engine)


# message
font = pygame.font.Font('fonts/Pacifico.ttf',50)


while event_handler.running:
    
    event_handler.get_event()

    screen.fill(color.BLACK)

    if chess.win == None:
        turnmsg = font.render(f"{chess.turn} turn !",True,(255,255,255))
        turnmsg_rect = turnmsg.get_rect(center=(origin_x + 11 * block_size,origin_y + 6 * block_size))
        movemsg = font.render(f"move {chess.moves}",True,(255,255,255))
        movemsg_rect = movemsg.get_rect(center=(origin_x + 12 * block_size,origin_y + 7 * block_size))
        screen.blit(turnmsg,turnmsg_rect)
        screen.blit(movemsg,movemsg_rect)
    else:
        winmsg = font.render(f"{chess.win} win !",True,(255,255,255))
        winmsg_rect = winmsg.get_rect(center=(origin_x + 11 * block_size,origin_y + 6 * block_size))
        screen.blit(winmsg,winmsg_rect)

    engine.update()
    
    pygame.display.update()