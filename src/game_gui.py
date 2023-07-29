import pygame as p
from board import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    """Load chess piece images."""
    pieces = ["P", "R", "N", "B", "K", "Q", "p", "r", "n", "b", "k", "q"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("/home/djulo/Source/PersonnalProjects/Kaspich/src/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen: p.Surface, board: Board):
    """Draw the current game state on the screen.

    Parameters:
        screen (pygame.Surface): The screen to draw on.
        board (Board): The chessboard state to be drawn.
    """
    draw_board(screen)
    draw_pieces(screen, board)


def draw_board(screen: p.Surface):
    """Draw the chessboard squares on the screen.

    Parameters:
        screen (pygame.Surface): The screen to draw on.
    """
    colors = [p.Color("white"), p.Color((50, 50, 50))]
    for rank in range(DIMENSION):
        for file in range(DIMENSION):
            color = colors[((rank + file) % 2)]
            p.draw.rect(screen, color, p.Rect(file * SQ_SIZE, rank * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen: p.Surface, board: Board):
    """Draw chess pieces on the screen.

    Parameters:
        screen (pygame.Surface): The screen to draw on.
        board (Board): The chessboard state with pieces to be drawn.
    """
    for rank in range(DIMENSION - 1, -1, -1):
        for file in range(DIMENSION):
            white_piece = board.piece_on(Square(rank * 8 + file), color=Color.WHITE)
            black_piece = board.piece_on(Square(rank * 8 + file), color=Color.BLACK)
            if white_piece is not None:
                screen.blit(IMAGES[white_piece.to_char().upper()], p.Rect(file * SQ_SIZE, (7 - rank) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if black_piece is not None:
                screen.blit(IMAGES[black_piece.to_char()], p.Rect(file * SQ_SIZE, (7 - rank) * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    """Main function to run the chess game."""
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    load_images()

    board = Board()
    board.board_initialization()

    selected_piece = None
    possible_moves = []
    dragging = False
    x, y = 0, 0  # Initialize x and y outside the event loop

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
                    dragging = True

            elif e.type == p.MOUSEBUTTONUP:
                if dragging and selected_piece is not None:
                    location = p.mouse.get_pos()
                    file = location[0] // SQ_SIZE
                    rank = 7 - (location[1] // SQ_SIZE)
                    target_square = Square(rank * 8 + file)
                    move = Move(selected_piece_square, target_square)

                    if move in possible_moves:
                        board = board.apply_move(move=move)
                    selected_piece = None
                    possible_moves = []
                    dragging = False

            elif e.type == p.MOUSEMOTION:
                if dragging and selected_piece is not None:
                    location = p.mouse.get_pos()
                    x = location[0] - SQ_SIZE // 2
                    y = location[1] - SQ_SIZE // 2

        draw_game_state(screen=screen, board=board)
        if dragging:
            if board.color_turn == Color.WHITE:
                screen.blit(IMAGES[selected_piece.to_char().upper()], p.Rect(x, y, SQ_SIZE, SQ_SIZE))
            else:
                screen.blit(IMAGES[selected_piece.to_char()], p.Rect(x, y, SQ_SIZE, SQ_SIZE))

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
