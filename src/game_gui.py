import pygame as p
from board import *
from button import Button
import sys
from chess_bot import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

p.init()
SCREEN = p.display.set_mode((WIDTH, HEIGHT))
BG = p.image.load("src/images/chess_back.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return p.font.Font("src/images/font.ttf", size)


def load_images():
    """Load chess piece images."""
    pieces = ["P", "R", "N", "B", "K", "Q", "p", "r", "n", "b", "k", "q"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("src/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


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


def handle_mouse_click(board, location, dragging, selected_piece, possible_moves):
    file = location[0] // SQ_SIZE
    rank = 7 - (location[1] // SQ_SIZE)
    selected_piece = board.piece_on(Square(rank * 8 + file))
    selected_piece_square = Square(rank * 8 + file)
    if selected_piece is not None:
        possible_moves = generate_legal_moves(board)
        dragging = True
    return selected_piece, possible_moves, dragging, selected_piece_square

def handle_mouse_release(board, dragging, selected_piece, possible_moves, selected_piece_square):
    if dragging and selected_piece is not None:
        location = p.mouse.get_pos()
        file = location[0] // SQ_SIZE
        rank = 7 - (location[1] // SQ_SIZE)
        target_square = Square(rank * 8 + file)
        move = Move(selected_piece_square, target_square)

        if move in possible_moves:
            if selected_piece.to_char().lower() == 'p' and target_square.rank in [0, 7]:
                # Automatically promote the pawn to a queen
                move.promo = PieceType.QUEEN
                board = board.apply_move(move=move)
            else:
                board = board.apply_move(move=move)
        selected_piece = None
        possible_moves = []
        dragging = False
    return board, selected_piece, possible_moves, dragging

def play(config):
    """Main function to run the chess game."""
    p.display.set_caption("game")

    SCREEN = p.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill("white")

    load_images()

    board = Board()
    board.board_initialization()

    selected_piece = None
    selected_piece_square = None
    possible_moves = []
    dragging = False
    x, y = 0, 0  # Initialize x and y outside the event loop

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
        
        if config == None: # CASE PLAYER VS PLAYER
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                selected_piece, possible_moves, dragging, selected_piece_square = handle_mouse_click(board, location, dragging, selected_piece, possible_moves)
            elif e.type == p.MOUSEBUTTONUP:
                board, selected_piece, possible_moves, dragging = handle_mouse_release(board, dragging, selected_piece, possible_moves, selected_piece_square)
            elif e.type == p.MOUSEMOTION:
                if dragging and selected_piece is not None:
                    location = p.mouse.get_pos()
                    x = location[0] - SQ_SIZE // 2
                    y = location[1] - SQ_SIZE // 2
        elif config[0] == "random": # CASE PLAYER VS RANDOM IA
            if board.color_turn == config[1]:
                board = random_bot(board=board, color=Color.BLACK)
            else:
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    selected_piece, possible_moves, dragging, selected_piece_square = handle_mouse_click(board, location, dragging, selected_piece, possible_moves)
                elif e.type == p.MOUSEBUTTONUP:
                    board, selected_piece, possible_moves, dragging = handle_mouse_release(board, dragging, selected_piece, possible_moves, selected_piece_square)
                elif e.type == p.MOUSEMOTION:
                    if dragging and selected_piece is not None:
                        location = p.mouse.get_pos()
                        x = location[0] - SQ_SIZE // 2
                        y = location[1] - SQ_SIZE // 2
        else: # CASE PLAYER VS MTCS IA
            continue
            # TODO
            
        draw_game_state(screen=SCREEN, board=board)
        if dragging:
            if board.color_turn == Color.WHITE:
                SCREEN.blit(IMAGES[selected_piece.to_char().upper()], p.Rect(x, y, SQ_SIZE, SQ_SIZE))
            else:
                SCREEN.blit(IMAGES[selected_piece.to_char()], p.Rect(x, y, SQ_SIZE, SQ_SIZE))

        p.display.flip()

def bot_color_option(config):
    while True:
        OPTIONS_MOUSE_POS = p.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(60).render("Choose color for the AI", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(256, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        IA_WHITE = Button(image=None, pos=(156, 300), 
                            text_input="WHITE", font=get_font(55), base_color="Black", hovering_color="Green")
        IA_BLACK = Button(image=None, pos=(400, 300), 
                            text_input="BLACK", font=get_font(55), base_color="Black", hovering_color="Green")
        OPTIONS_BACK = Button(image=None, pos=(256, 456), 
                            text_input="BACK", font=get_font(60), base_color="Black", hovering_color="Green")

        for button in [IA_WHITE, IA_BLACK, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    bot_algorithm_option()
                if IA_WHITE.checkForInput(OPTIONS_MOUSE_POS):
                    config = (config[0], Color.WHITE)
                    play(config)
                if IA_BLACK.checkForInput(OPTIONS_MOUSE_POS):
                    config = (config[0], Color.BLACK)
                    play(config)

        p.display.update()

def bot_algorithm_option():
    while True:
        OPTIONS_MOUSE_POS = p.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(60).render("Choose ALGO for the AI", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(256, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        IA_RANDOM = Button(image=None, pos=(156, 300), 
                            text_input="RANDOM", font=get_font(55), base_color="Black", hovering_color="Green")
        IA_MCTS = Button(image=None, pos=(400, 300), 
                            text_input="MCTS", font=get_font(55), base_color="Black", hovering_color="Green")
        OPTIONS_BACK = Button(image=None, pos=(256, 456), 
                            text_input="BACK", font=get_font(60), base_color="Black", hovering_color="Green")

        for button in [IA_RANDOM, IA_MCTS, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                elif IA_RANDOM.checkForInput(OPTIONS_MOUSE_POS):
                    bot_color_option(("random", None))
                elif IA_MCTS.checkForInput(OPTIONS_MOUSE_POS):
                    # TODO
                    continue

        p.display.update()

def main_menu():
    p.display.set_caption("Menu")

    while True:
        
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = p.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(256, 100))

        PLAY_IA_VS_PLAYER = Button(image=None, pos=(256, 250), 
                            text_input="PLAYER VS IA", font=get_font(60), base_color="black", hovering_color="White")
        PLAY_PLAYER_VS_PLAYER = Button(image=None, pos=(256, 350), 
                            text_input="PLAYER VS PLAYER", font=get_font(60), base_color="black", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(256, 450), 
                            text_input="EXIT", font=get_font(60), base_color="black", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_IA_VS_PLAYER, PLAY_PLAYER_VS_PLAYER, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if PLAY_IA_VS_PLAYER.checkForInput(MENU_MOUSE_POS):
                    bot_algorithm_option()
                if PLAY_PLAYER_VS_PLAYER.checkForInput(MENU_MOUSE_POS):
                    play(None)
                    continue
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    p.quit()
                    sys.exit()

        p.display.update()

def main():
    main_menu()


if __name__ == "__main__":
    main()
