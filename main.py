import chess
import chess.pgn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pandasgui import show

from aggregation import aggregate
from processing import process_game, in_range
from plotting import *


def main():
    filename = "./pgn/Dae.pgn"
    # filename = "./pgn/testing.pgn"

    # meta data and game list
    df, games = aggregate(filename)
    # df.to_csv("./Dataframes/" + filename[6:-4] + ".csv")

    rows = []
    for game in games:
        lost_pieces = process_game(game)
        rows.append(lost_pieces)
    df["Lost pieces"] = rows



    # pieces = [chess.ROOK, chess.KNIGHT]
    pieces = list(chess.PIECE_TYPES)[:-1][::-1]

    df_elo  = df[(df["WhiteElo"] != "?") & (df["BlackElo"] != "?")].astype({"WhiteElo": 'int', "BlackElo": 'int'})
    minimum, low, mid, high, maximum = df_elo["WhiteElo"].quantile([0, 0.25, 0.5, 0.75, 1])

    elo_bins = [minimum, low, mid, high, maximum]

    bins = []
    col_labels = []
    for lower, upper in zip(elo_bins[:-1], elo_bins[1:]):
        print(f"Elo in range {lower}-{upper}")
        bins.append(df_elo[in_range(lower, df_elo["WhiteElo"], upper)])
        col_labels.append(f"Elo in range {lower}-{upper}\nQ{len(bins)-1}-Q{len(bins)}")


    # bins = [df_elo, df_elo, df_elo, df_elo, df_elo]

    plt.rcParams['figure.figsize'] = (15, 10)

    fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK, username="DaenaliaEvandruile")
    fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.WHITE, username="DaenaliaEvandruile")
    fig, axs = plot_heatmap_single_piece(df, [chess.PAWN], username="DaenaliaEvandruile")
    fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, username="DaenaliaEvandruile")
    fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, username="DaenaliaEvandruile", kde=True)

    # for piece in chess.PIECE_TYPES:
    #     fig, axs = plot_heatmap_single_piece(df, [piece], username="DaenaliaEvandruile")

    plt.show()

    # show(df_elo)

    return df

if __name__ == "__main__":
    df = main()
