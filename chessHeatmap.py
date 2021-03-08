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


def single_player(games: List[chess.pgn.Game]) -> Tuple[List[chess.pgn.Game], List[chess.pgn.Game]]:
    print(games[0].headers["White"])
    print(games[0].headers["Black"])
    username = input("Username to analyse: ")
    # username = "kev4chess"
    # username = "DaenaliaEvandruile"

    white_games = []
    black_games = []

    for game in games:
        if username == game.headers["White"]:
            white_games.append(game)
        elif username == game.headers["Black"]:
            black_games.append(game)
        else:
            raise ValueError("Player name did not play in game " + str(len(white_games) + len(black_games)))
    return white_games, black_games


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
    return piece_position


def frequecny_match_pattern(frequency: List[int], patterns: List[int], lost: List[Tuple[int, int, int]]):
    for piece_lost in lost:
        if piece_lost[0] in patterns:
            # print(piece_lost)
            # print("position = ", piece_lost[1])
            x = piece_lost[1]
            frequency[x] += 1
            # print(np.reshape(frequency, (8,8)))


def naive_frequency(board: chess.Board, pieces: List[str], frequency: List[List[int]]):
    boardstr = str(board)
    boardstr = boardstr.splitlines(False)
    for y in range(8):
        for x in range(8):
            # print(boardstr[y][2*x])
            if boardstr[y][2*x] in pieces:
                frequency[y][x] += 1









def lost_piece_plot(pgn: List[chess.pgn.Game], patterns: List[int]):
    white_games, black_games  = single_player(pgn)

    fig, axs = plt.subplots(ncols=2)

    frequency_black = gen_frequency()
    frequency_white = gen_frequency()

    for game in white_games:
        lost_pieces_white = game_capture(game, chess.WHITE)
        frequecny_match_pattern(frequency_white, patterns, lost_pieces_white)

    for game in black_games:
        lost_pieces_black = game_capture(game, chess.BLACK)
        frequecny_match_pattern(frequency_black, patterns, lost_pieces_black)

    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    frequencies = [frequency_white, frequency_black]


    for x in range(2):
        sns.heatmap(
            np.reshape(frequencies[x], (8,8)),
            ax=axs[x],
            cmap=cmap,
            xticklabels=list(ascii_letters[:8]),
            yticklabels=range(8,0,-1),
            square=True,
            # annot=True
        ).set_title("Black" if x else "White")

pgn = load_pgn("dad.pgn")
# single_player_plot(pgn)

# split_pattern_plot(pgn, [""])
# sns.displot(STATS["Queen lost"])
lost_piece_plot(pgn, [chess.PAWN])
plt.show(block=False)
