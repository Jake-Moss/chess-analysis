import chess
import chess.pgn
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from string import ascii_letters

from typing import List, Tuple, Dict


def gen_frequency() -> List[int]:
    return [0 for _ in range(64)]


def uci_to_grid(uci: str) -> int:
    if len(uci) == 5:
        uci = uci[:-1]
    return abs(int(uci[-1]) - 8)*8 + (ord(uci[-2]) - ord('a'))


def load_pgn(filename: str) -> List[chess.pgn.Game]:
    with open(filename) as pgn:
        games =[]
        while True:
            game = chess.pgn.read_game(pgn)
            if game is not None:
                games.append(game)
            else:
                break
        return games


def single_player(games: List[chess.pgn.Game], username = '') -> Tuple[List[chess.pgn.Game], List[chess.pgn.Game], str]:
    print(games[0].headers["White"])
    print(games[0].headers["Black"])

    if not username:
        names = []
        for game in games:
            names.extend([game.headers["White"], game.headers["Black"]])
        username = max(set(names), key = names.count)
        print("Guessed player is", username)

    white_games = []
    black_games = []

    for game in games:
        if username == game.headers["White"]:
            white_games.append(game)
        elif username == game.headers["Black"]:
            black_games.append(game)
        else:
            raise ValueError("Player name did not play in game " + str(len(white_games) + len(black_games)))
    return white_games, black_games, username


def progress_game(game: chess.pgn.Game, number_of_moves: int = 0):
    count = 0
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        count += 1
        if (count >= number_of_moves) and number_of_moves:
            break


def game_capture(game: chess.pgn.Game, colour: bool, number_of_moves: int = 0) -> List[Tuple[int, int, int]]:
    count = 0
    lost = []
    board = game.board()
    piece_count = {
        chess.PAWN: 8,
        chess.KNIGHT: 2,
        chess.BISHOP: 2,
        chess.ROOK: 2,
        chess.QUEEN: 1
    }
    for move in game.mainline_moves():
        if board.turn == colour: # is our colour
            if board.is_capture(move): # move is capture, including en passnat
                if not board.is_en_passant(move): # is it not en passant, the norm
                    board.push(move)
                    piece = piece_delta(board, count, piece_count, board.turn)
                    lost.append(piece)
                else: # needs seperate code path
                    board.push(move)
                    print("en passant hit", colour)

            else:
                board.push(move)

        else:
            board.push(move)

        count += 1
        if (count >= number_of_moves) and number_of_moves: # Stop after moving n times and n is non-zero
            break
    return lost


def piece_delta(board: chess.Board, count: int, piece_count: Dict[int, int], colour: bool) -> Tuple[int, int, int]:
    piece_position = (0, 0, 0)
    for key, value in piece_count.items():
        current_count = bin(board.pieces_mask(key, colour)).count('1')
        if current_count < value: # Detects lost based on previous state
            piece_position = (key, uci_to_grid(board.peek().uci()), count)
            # print(board.peek().uci())
            piece_count[key] = current_count # Modify by object-reference
        elif current_count > value: # Accounts for promotion
            piece_count[key] = current_count # Modify by object-reference
    return piece_position # piece id, position, count


def frequecny_match_pattern(frequency: List[int], patterns: List[int], lost: List[Tuple[int, int, int]]):
    for piece_lost in lost:
        if piece_lost[0] in patterns:
            # print(piece_lost)
            # print("position = ", piece_lost[1])
            x = piece_lost[1]
            frequency[x] += 1
            # print(np.reshape(frequency, (8,8)))






def lost_piece_heat(ax: np.ndarray, games: List[chess.pgn.Game], colour: bool,  patterns: List[int], number_of_moves: int = 0):

    frequency = gen_frequency()

    for game in games:
        lost_pieces = game_capture(game, colour, number_of_moves)
        for piece in lost_pieces:
            if piece[0] in patterns:
                x = piece[1]
                frequency[x] += 1

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(
        np.reshape(frequency, (8,8)),
        ax=ax,
        cmap=cmap,
        xticklabels=list(ascii_letters[:8]),
        yticklabels=range(8,0,-1),
        square=True
    )


def lost_piece_hist(ax: np.ndarray, games: List[chess.pgn.Game], colour: bool,  patterns: List[int], number_of_moves: int = 0):

    # pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
    # g = sns.FacetGrid(aspect=15, height=.5, palette=pal)
    # moves_pieces_lost_on = [None]
    #


    total_count = []
    for game in games:
        lost_pieces = game_capture(game, colour, number_of_moves)
        for piece in lost_pieces:
            if piece[0] in patterns:
                total_count.append(piece[2])

    sns.kdeplot(data=total_count, ax=ax, fill=True, alpha=0.5, linewidth=1.5)

def main():
    pgn = load_pgn("Dae.pgn")

    white_games, black_games, username  = single_player(pgn)
    grid = (5,5)
    fig, axs = plt.subplots(grid[0], grid[1])

    # lost_piece_heat(axs[0], white_games, chess.WHITE, [chess.PAWN])
    # axs[0].set_title("White")

    x = 0
    for piece in chess.PIECE_TYPES[:5]:
        for y in range(grid[1]):
            lost_piece_hist(axs[x][y], white_games, chess.WHITE, [piece])
            if (not x == grid[1] - 1 ) and (not y == 0):
                axs[x][y].tick_params(
                    axis='both',
                    labelbottom=False,
                    labelleft=False
                )
                axs[x][y].yaxis.label.set_visible(False)
            if (x == grid[1] - 1 ):
                axs[x][y].tick_params(
                    axis='y',
                    labelbottom=True,
                    labelleft=False
                )
                axs[x][y].yaxis.label.set_visible(False)
            if (y == 0):
                axs[x][y].tick_params(
                    axis='x',
                    labelbottom=False,
                    labelleft=True
                )
                axs[x][y].yaxis.label.set_visible(True)
            if (x == grid[1] - 1 ) and (y == 0):
                axs[x][y].tick_params(
                    axis='both',
                    labelbottom=True,
                    labelleft=True
                )
                axs[x][y].yaxis.label.set_visible(True)
            axs[x][y].set_ylabel(chess.PIECE_NAMES[piece].capitalize())
        x += 1
    # lost_piece_heat(axs[1], black_games, chess.BLACK, [chess.PAWN])
    # axs[1].set_title("Black")

    # fig.suptitle("Positions of " + chess.PIECE_NAMES[chess.PAWN] + " when lost from whites POV")
    # fig.savefig("Lost piece plot pawns")
    fig.show()

    # fig, axs = plt.subplots(1, 2)
    # lost_piece_plot(axs[0], white_games, chess.WHITE, [chess.KNIGHT])
    # lost_piece_plot(axs[1], black_games, chess.BLACK, [chess.KNIGHT])
    # fig.show()

    # filename = "testing.png"

    # fig.savefig(filename)
    fig.show()

if __name__ == "__main__":
    main()
