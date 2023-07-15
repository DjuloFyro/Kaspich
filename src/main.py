from board import Board


def main() -> None:
    chessBoard = Board()
    chessBoard.board_initialization()

    chessBoard.print_board()


if __name__ == "__main__":
    main()

