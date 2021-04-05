import chess
import chess.pgn
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from string import ascii_letters

from typing import List, Tuple, Dict


def gen_frequency() -> List[int]:
    """
    Generates 1x64 (8x8) freq array filled with 0
    Index via 1d array notation

    [0,0,...]
    """
    return [0 for _ in range(64)]


def uci_to_1d_array_index(uci: str) -> int:
    """"
    Converts uci notation to 1d array indexing.

      a b c
     ------
    8|1 2 3   -->  [1, 2, 3, 4, 5, 6, 7, 8, 9]
    7|4 5 6
    6|7 8 9

    Also attempts to account for en pasenant
    """
    if len(uci) == 5:
        uci = uci[:-1]
    return abs(int(uci[-1]) - 8)*8 + (ord(uci[-2]) - ord('a'))


def load_pgn(filename: str) -> List[chess.pgn.Game]:
    """
    Read pgn into list, breaks after hitting EOF
    """
    with open(filename) as pgn:
        games =[]
        while True:
            game = chess.pgn.read_game(pgn)
            if game is not None:
                games.append(game)
            else:
                break
        return games


# reimplement using dataframe
def single_player(games: List[chess.pgn.Game], username = '') -> Tuple[List[chess.pgn.Game], List[chess.pgn.Game], str]:
    """
    Splits list of games into black and white games based on the POV of the selected player.

    Attempts to guess the player based on most freq name unless given a username.

    Rasies value error if the player did not play in a particular game.
    """
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
    """
    Advance game to end state
    """
    count = 0
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        count += 1
        if (count >= number_of_moves) and number_of_moves:
            break


def game_capture(game: chess.pgn.Game, colour: bool, number_of_moves: int = 0) -> List[Tuple[int, int, int]]:
    """
    Steps through game and checks if a piece has been lost via piece_delta

    Can hanldle en passant :pog:
    """
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
                else: # needs seperate code path
                    piece = (1, uci_to_1d_array_index(move.uci()), count)
                    board.push(move)
                lost.append(piece)

            else:
                board.push(move)

        else:
            board.push(move)

        count += 1
        if (count >= number_of_moves) and number_of_moves: # Stop after moving n times and n is non-zero
            break
    return lost


def piece_delta(board: chess.Board, count: int, piece_count: Dict[int, int], colour: bool) -> Tuple[int, int, int]:
    """
    Returns a tuple of the key (int piece code), restult from uci_to_1d_array_index, and move the piece
    was lost on.

    Detects when a piece is lost by counting the number of ones on the piece board mask and tracking
    the previous value.

    Would be really nice if the deves merged this :|
    https://github.com/niklasf/python-chess/pull/296/commits/498dd015cbffffb57bc7ef2a6d097fb6d9340eed
    """
    piece_position = (0, 0, 0)
    for key, value in piece_count.items():
        current_count = bin(board.pieces_mask(key, colour)).count('1')
        if current_count < value: # Detects lost based on previous state
            piece_position = (key, uci_to_1d_array_index(board.peek().uci()), count)
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
    """
    Plots a heat 8x8 heat map of where a pattern of pieces where lost.
    """

    frequency = gen_frequency()

    for game in games:
        lost_pieces = game_capture(game, colour, number_of_moves)
        for piece in lost_pieces:
            if piece[0] in patterns:
                x = piece[1]
                frequency[x] += 1

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    print(frequency)
    sns.heatmap(
        np.reshape(frequency, (8,8)),
        ax=ax,
        cmap=cmap,
        xticklabels=list(ascii_letters[:8]),
        yticklabels=range(8,0,-1),
        square=True,
        cbar=False
    )


def lost_piece_hist(ax: np.ndarray, games: List[chess.pgn.Game], colour: bool, \
                    patterns: List[int], number_of_moves: int = 0):
    """
    Plots a kernel density plot of what move number the particular piece was
    lost on.

    piece is int rather than string as python-chess uses int in backed.
    """
    total_count = []
    for game in games:
        lost_pieces = game_capture(game, colour, number_of_moves)
        for piece in lost_pieces:
            if piece[0] in patterns:
                total_count.append(piece[2])

    sns.kdeplot(data=total_count, ax=ax, fill=True, alpha=0.5, linewidth=1.5)


def subplot_matrix_format(axs: np.ndarray, grid: Tuple[int, int]):
    """
    Formats the sub plots grid provided such that the axis labels are only
    on the left and bottom plots. Assumes full NxM grid of subplots.
    """
    #axs is np.ndarry[np.ndarry[plt.Axes]] but type hints wont work for some reason?
    if np.size(axs) == max(grid):
        axs = np.reshape(axs, grid)

    for row in range(grid[0]):
        piece = chess.PIECE_TYPES[row]
        for col in range(grid[1]):
            if (not row == grid[0] - 1 ) and (not col == 0):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=False,
                    bottom=False,
                    labelleft=False,
                    left=False,
                )
                axs[row][col].yaxis.label.set_visible(False)
            if (row == grid[0] - 1):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=True,
                    bottom=True,
                    labelleft=False,
                    left=False,
                )
                axs[row][col].yaxis.label.set_visible(False)
            if (col == 0):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=False,
                    bottom=False,
                    labelleft=True,
                    left=True,
                )
                axs[row][col].yaxis.label.set_visible(True)
            if (row == grid[0] - 1) and (col == 0):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=True,
                    bottom=True,
                    labelleft=True,
                    left=True,
                )
                axs[row][col].yaxis.label.set_visible(True)
            axs[row][col].set_ylabel(chess.PIECE_NAMES[piece].capitalize())


def main():
    pgn = load_pgn("pgn/Dae.pgn")

    white_games, black_games, username  = single_player(pgn)
    grid = (5,2)
    fig, axs = plt.subplots(grid[0], grid[1])

    games = [white_games,black_games]
    # games = [white_games, black_games, white_games, black_games, white_games]

    subplot_matrix_format(axs, grid)


    # # kde plot for feq thing
    # for row in range(grid[0]):
    #     piece = chess.PIECE_TYPES[row]
    #     for col in range(grid[1]):
    #         lost_piece_hist(axs[row][col], games[col], chess.WHITE, [piece]) # plotting happens here


    # Normal heat plot thing
    # lost_piece_heat(axs[0], white_games, chess.WHITE, [chess.KNIGHT])
    # lost_piece_heat(axs[1], black_games, chess.BLACK, [chess.KNIGHT])
    # axs[0].set_title("White")
    # axs[1].set_title("Black")

    # fig.suptitle("Positions of " + chess.PIECE_NAMES[chess.PAWN] + " when lost from whites POV")
    # fig.savefig("Lost piece plot pawns")

    # heat plot on matrix plot thingo below
    for row in range(grid[0]):
        piece = chess.PIECE_TYPES[row]
        for col in range(grid[1]):
            lost_piece_hist(axs[row][col], games[col], chess.WHITE, [piece]) # plotting happens here
            lost_piece_heat(axs[row][col], games[col], chess.WHITE, [piece])

    # filename = "testing.png"

    # fig.savefig(filename)
    fig.show()

if __name__ == "__main__":
    main()
