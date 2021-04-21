#!/usr/bin/env python3
import chess
import chess.pgn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import List, Tuple, Dict, Union




def uci_to_1d_array_index(uci: str) -> int:
    """"
    Converts uci notation to 1d array indexing.

      a b c
     ------
    8|1 2 3   -->  [1, 2, 3, 4, 5, 6, 7, 8, 9]
    7|4 5 6
    6|7 8 9

    # I've actually forgotten what corner it starts in :|

    Also accounts for promotions
    """
    if len(uci) == 5:
        uci = uci[:-1]
    return abs(int(uci[-1]) - 8)*8 + (ord(uci[-2]) - ord('a'))


def piece_delta(board: chess.Board, count: int, piece_count: Dict[int, int],
                colour: bool) -> Tuple[int, int, int]:
    """
    Returns a tuple of the key (e.g. chess.PAWN), restult from
    uci_to_1d_array_index, and move the piece was lost on.

    Detects when a piece is lost by counting the number of ones on the piece
    board mask and tracking the previous value.

    Would be really nice if the devs merged this :|
    https://github.com/niklasf/python-chess/pull/296/commits/498dd015cbffffb57bc7ef2a6d097fb6d9340eed
    """
    piece_position = (0, 0, 0)
    # print(piece_count)
    for key, value in piece_count.items():
        # print(key, value)
        current_count = bin(board.pieces_mask(key, colour)).count('1')  # REQUIRES THE MOVE BE MADE (CAPTURED)
        if current_count < value: # Detects lost based on previous state
            piece_position = (key, uci_to_1d_array_index(board.peek().uci()), count)
            piece_count[key] = current_count # Modify by object-reference
            break
        elif current_count > value: # Accounts for promotion
            piece_count[key] = current_count # Modify by object-reference
            piece_count[chess.PAWN] = bin(board.pieces_mask(chess.PAWN, colour)).count('1')  # Account for pawn count change
            break
    return piece_position # piece id, position, count


def get_captures(board: chess.Board, prev_moce: chess.Move, count: int, piece_count: Dict[int, int]) \
                -> Tuple[int, int, int]:

    if not board.is_en_passant(prev_moce): # is it not en passant, the norm
        piece = piece_delta(board, count, piece_count, board.turn)
    else: # needs seperate code path
        piece = (1, uci_to_1d_array_index(prev_moce.uci()), count)
    return piece


def process_game(game: chess.pgn.Game, number_of_moves: int = 0) \
                -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:

    board = game.board()
    piece_count = (
        # chess.BLACK
        {
            chess.BISHOP: 2,
            chess.ROOK: 2,
            chess.KNIGHT: 2,
            chess.QUEEN: 1,
            chess.PAWN: 8,
        },
        # chess.WHITE
        {
            chess.BISHOP: 2,
            chess.ROOK: 2,
            chess.KNIGHT: 2,
            chess.QUEEN: 1,
            chess.PAWN: 8,
        }
 )
    lost_pieces = ([], # chess.BLACK
                   []) # chess.WHITE

    for move in game.mainline_moves():
        count = len(board.move_stack)
        board.push(move)
        turn = board.turn

        # Get captures on this turn
        if board.is_capture(board.peek()):
            piece = get_captures(board, board.peek(), count, piece_count[turn])
            # print(board.is_capture(board.peek()))
            if piece[0]:
                lost_pieces[turn].append(piece)
        if (count >= number_of_moves) and number_of_moves: # Stop after moving n times and n is non-zero
            break

    return lost_pieces


def in_range(lower: Union[int, pd.Timestamp], df, upper: Union[int, pd.Timestamp]):
    return (df > lower) & (df <= upper)
