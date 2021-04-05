#!/usr/bin/env python3
import chess
import chess.pgn
import pandas as pd

from typing import List, Tuple
"""
This module pulls the games from pgn files, compiles these games into a
dataframe with meta data.
"""

COLUMNS = [
    'Event',
    'Site',
    'Date',
    'Round',
    'White',
    'Black',
    'Result',
    'BlackElo',
    'BlackRatingDiff',
    'ECO',
    'Termination',
    'TimeControl',
    'UTCDate',
    'UTCTime',
    'Variant',
    'WhiteElo',
    'WhiteRatingDiff',
]

def load_pgn(filename: str) -> List[chess.pgn.Game]:
    """
    Read pgn into list, breaks after hitting EOF
    """
    with open(filename) as pgn:
        games = []
        while True:
            game = chess.pgn.read_game(pgn)
            if game is not None:
                games.append(game)
            else:
                break
        return games


def aggregate(filename: str) -> Tuple[pd.DataFrame, List[chess.pgn.Game]]:
    with open(filename) as pgn:
        rows = []
        games = []
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            row = [dict(game.headers).get(x) for x in COLUMNS]
            rows.append(row)
            games.append(game)
            # rows.append(list(dict(game.headers).get(x) for x in COLUMNS))
        df = pd.DataFrame(rows, columns=COLUMNS)
        return df, games

if __name__ == "__main__":
    from pandasgui import show

    df, games = aggregate("./pgn/Dae.pgn")

    # show(df)
