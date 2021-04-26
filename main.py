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
    filename = "./Dataframes/" + "The big one" + ".csv"

    # patterns = ["World", "Champ", "Candidates", "Interzonal", "PCA"]
    # patterns = ["2000"]
    # patterns = ["World"]
    patterns = ["Dae"]
    # directory = r'/home/jake/Downloads/pgn/'
    directory = r'./pgn/'
    # directory = r'./pgn/FISC'
    dfs = []
    list_of_games = []
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
            list_of_games.extend(games)

    df = pd.concat(dfs, ignore_index=True)
    # filename = "./pgn/DeLaBourdonnais.pgn"

    # filename = "./pgn/testing.pgn"

    # meta data and game list
    # df.to_csv(filename)

    # pieces = [chess.ROOK, chess.KNIGHT]
    pieces = list(chess.PIECE_TYPES)[:-1][::-1]

    # Type casting and filtering
    df_elo = df[df["WhiteElo"].apply(lambda x: x not in ["", "?", None, np.nan]) & \
                df["BlackElo"].apply(lambda x: x not in ["", "?", None, np.nan])]  \
                .astype({"WhiteElo": 'int', "BlackElo": 'int'}) # type casts elo to ints and filters out the various non-int things
    df["Date"] = pd.to_datetime(df["Date"].apply(lambda x: x.replace("?", "")[:4].replace(".", ""))) # type cast dates to dates, assumes year is present in all data

    plt.rcParams['figure.figsize'] = (8, 7)

    # # ELO
    # minimum, low, low_mid, mid, mid_high, high, maximum = df_elo["WhiteElo"].quantile([0, 0.028, 0.1587, 0.5, 0.8413, 0.9772, 1])
    # bins_ranges = [minimum, low, low_mid, mid, mid_high, high, maximum]
    # bins = []
    # col_labels = []
    # for lower, upper in zip(bins_ranges[:-1], bins_ranges[1:]):
    #     print(f"Elo in range {lower:.0f}-{upper:.0f}")
    #     bins.append(df_elo[in_range(lower, df_elo["WhiteElo"], upper)])
    #     col_labels.append(f"Elo in range\n{lower:.0f}-{upper:.0f}\n{len(bins)-4 if len(bins) != 1 else '-inf'}σ-{len(bins)-3 if len(bins) != 6 else 'inf'}σ")
    # bintype = "ELO"


    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK, bintype, username="DaenaliaEvandruile")
    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.WHITE, bintype, username="DaenaliaEvandruile")

    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, bintype, username="DaenaliaEvandruile")
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.WHITE, bintype, username="DaenaliaEvandruile")


    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK, bintype)
    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.WHITE, bintype)
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, bintype)
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.WHITE, bintype)



    # # DATE
    # minimum, low, mid, high, maximum = df["Date"].quantile([0, 0.25, 0.5, 0.75, 1])
    # bins_ranges = [minimum, low, mid, high, maximum]
    # # bins_ranges = [pd.to_datetime("1700"), pd.to_datetime("1900"), pd.to_datetime("1980"), pd.to_datetime("2010"), pd.to_datetime("2025")]

    # bins = []
    # col_labels = []
    # for lower, upper in zip(bins_ranges[:-1], bins_ranges[1:]):
    #     print(f"Date in range {lower.year}-{upper.year}")
    #     bins.append(df[in_range(lower, df["Date"], upper)])
    #     col_labels.append(f"Date in range\n{lower.year} to {upper.year}\nQ{len(bins)-1}-Q{len(bins)}")
    # bintype = "DATE"

    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK, bintype, username="DaenaliaEvandruile")
    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.WHITE, bintype, username="DaenaliaEvandruile")

    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, bintype, username="DaenaliaEvandruile")
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.WHITE, bintype, username="DaenaliaEvandruile")

    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK, bintype)
    # fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.WHITE, bintype)
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.BLACK, bintype)
    # fig, axs = plot_hist_grid(bins, pieces, col_labels, chess.WHITE, bintype)







    # fig, axs = plot_heatmap_single_piece(df, [chess.PAWN], username="DaenaliaEvandruile")
    # fig, axs = plot_heatmap_single_piece(df, [chess.PAWN], bintype)

    # for piece in chess.PIECE_TYPES[:-1]:
        # fig, axs = plot_heatmap_single_piece(df, [piece], username="DaenaliaEvandruile")
        # fig, axs = plot_heatmap_single_piece(df, [piece])

        # fig, axs = plot_hist_single_piece(df, [piece], username="DaenaliaEvandruile")
        # fig, axs = plot_hist_single_piece(df, [piece])



    # plt.show()

    # show(df)

    print(len(df))
    return df, list_of_games

if __name__ == "__main__":
    df, games = main()

# def animate(i):
#     fig, axs = plot_heatmap_grid(bins, pieces, col_labels, chess.BLACK)
