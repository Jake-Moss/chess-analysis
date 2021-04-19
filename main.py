import chess
import chess.pgn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns
import os

from pandasgui import show

from aggregation import aggregate
from processing import process_game, in_range
from plotting import *


def main():

    # patterns = ["World", "Champ"]
    patterns = ["Dae"]
    # directory = r'/home/jake/Downloads/pgn/'
    directory = r'./pgn/'
    dfs = []
    for entry in os.scandir(directory):
        if (entry.path.endswith(".pgn") and entry.is_file()) and any(True for pattern in patterns \
                                                                 if pattern in entry.name[:-4]):
            print(entry.path)
            df, games = aggregate(entry.path)

            rows = []
            for game in games:
                lost_pieces = process_game(game)
                rows.append(lost_pieces)
            df["Lost pieces"] = rows

            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    # filename = "./pgn/DeLaBourdonnais.pgn"

    # filename = "./pgn/testing.pgn"

    # meta data and game list
    # df.to_csv("./Dataframes/" + filename[6:-4] + ".csv")




    # pieces = [chess.ROOK, chess.KNIGHT]
    pieces = list(chess.PIECE_TYPES)[:-1][::-1]

    # Type casting and filtering
    df_elo = df[df["WhiteElo"].apply(lambda x: True if x not in ["", "?", None] else False) & \
                df["BlackElo"].apply(lambda x: True if x not in ["", "?", None] else False)]  \
                .astype({"WhiteElo": 'int', "BlackElo": 'int'}) # type casts elo to ints and filters out the various non-int things
    df["Date"] = pd.to_datetime(df["Date"].apply(lambda x: x.replace("?", ""))) # type cast dates to dates, assumes year is present in all data

    # ELO
    minimum, low, mid, high, maximum = df_elo["WhiteElo"].quantile([0, 0.25, 0.5, 0.75, 1])
    bins_ranges = [minimum, low, mid, high, maximum]
    bins = []
    col_labels = []
    for lower, upper in zip(bins_ranges[:-1], bins_ranges[1:]):
        print(f"Elo in range {lower}-{upper}")
        bins.append(df_elo[in_range(lower, df_elo["WhiteElo"], upper)])
        col_labels.append(f"Elo in range {lower}-{upper}\nQ{len(bins)-1}-Q{len(bins)}")


    # # DATE
    # minimum, low, mid, high, maximum = df["Date"].quantile([0, 0.25, 0.5, 0.75, 1])
    # bins_ranges = [minimum, low, mid, high, maximum]
    # # bins_ranges = [pd.to_datetime("1800"), pd.to_datetime("1950"), pd.to_datetime("2005"), pd.to_datetime("2010"), pd.to_datetime("2025")]
    # bins = []
    # col_labels = []
    # for lower, upper in zip(bins_ranges[:-1], bins_ranges[1:]):
    #     print(f"Date in range {lower.year}-{upper.year}")
    #     bins.append(df[in_range(lower, df["Date"], upper)])
    #     col_labels.append(f"Date in range {lower.year}-{upper.year}\nQ{len(bins)-1}-Q{len(bins)}")


    # bins = [df_elo, df_elo, df_elo, df_elo, df_elo]

    plt.rcParams['figure.figsize'] = (15, 10)

    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK, username="DaenaliaEvandruile")
    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.WHITE, username="DaenaliaEvandruile")
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, username="DaenaliaEvandruile")
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, username="DaenaliaEvandruile", kde=True)

    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK)
    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.WHITE)
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK)
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, kde=True)

    # fig, axs = plot_heatmap_single_piece(df, [chess.PAWN], username="DaenaliaEvandruile")
    # for piece in chess.PIECE_TYPES:
    #     fig, axs = plot_heatmap_single_piece(df, [piece], username="DaenaliaEvandruile")

    fig, axs = plot_hist_single_piece(df, [chess.PAWN], username="DaenaliaEvandruile")
    for piece in chess.PIECE_TYPES:
        fig, axs = plot_hist_single_piece(df, [piece], username="DaenaliaEvandruile")

    plt.show()





    # show(df)

    return df

if __name__ == "__main__":
    df = main()

# def animate(i):
#     fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK)
