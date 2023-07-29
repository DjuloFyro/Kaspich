import pygame as p
from board import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ["P", "R", "N", "B", "K", "Q", "p", "r", "n", "b", "k", "q"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("/home/djulo/Source/PersonnalProjects/Kaspich/src/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, board):
    draw_board(screen)
    draw_pieces(screen, board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color((50,50,50))]
    for rank in range(DIMENSION):
        for file in range(DIMENSION):
            color = colors[((rank + file ) % 2)]
            p.draw.rect(screen, color, p.Rect(file*SQ_SIZE, rank*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for rank in range(DIMENSION - 1, -1, -1):
        for file in range(DIMENSION):
            white_piece = board.piece_on(Square(rank*8 + file), color=Color.WHITE)
            black_piece = board.piece_on(Square(rank*8 + file), color=Color.BLACK)
            if white_piece != None:
                screen.blit(IMAGES[white_piece.to_char().upper()], p.Rect(file*SQ_SIZE, (7-rank)*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if black_piece != None:
                screen.blit(IMAGES[black_piece.to_char()], p.Rect(file*SQ_SIZE, (7-rank)*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    load_images()
    
    board = Board()
    board.board_initialization()

    sq_selected = None # Keep track of the last click of the user (rank, file)
    player_clicks = []

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                file = location[0] // SQ_SIZE
                rank = 7 - (location[1] // SQ_SIZE)
                selected_piece = board.piece_on(Square(rank * 8 + file))
                selected_piece_square = Square(rank * 8 + file)
                if selected_piece is not None:
                    possible_moves = generate_legal_moves(board)

            elif e.type == p.MOUSEBUTTONUP:
                if selected_piece is not None:
                    location = p.mouse.get_pos()
                    file = location[0] // SQ_SIZE
                    rank = 7 - (location[1] // SQ_SIZE)
                    target_square = Square(rank * 8 + file)
                    move = Move(selected_piece_square, target_square)
                    
                    if move in possible_moves:
                        board = board.apply_move(move=move)
                    selected_piece = None
                    possible_moves = []

        draw_game_state(screen=screen, board=board)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()