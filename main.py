import chess
import chess.pgn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pandasgui import show

from aggregation import aggregate
from processing import process_game
from plotting import *


def main():
    filename = "./pgn/Dae.pgn"

    # meta data and game list
    df, games = aggregate(filename)
    # df.to_csv("./Dataframes/" + filename[6:-4] + ".csv")

    rows = []
    for game in games:
        lost_pieces = process_game(game)
        rows.append(lost_pieces)
    df["Lost pieces"] = rows



    # pieces = [chess.ROOK, chess.KNIGHT]
    pieces = list(chess.PIECE_TYPES)[1:-1]
    elo_bins = [1000, 1200, 1300, 1400, 1500]

    fig, axs = plot_heatmap_grid([df, df, df, df, df], pieces)
    plt.show()

    # df[(df["WhiteElo"] != "?") & (df["BlackElo"] != "?")].astype({"WhiteElo": 'int', "BlackElo": 'int'})

    # sns.kdeplot(data=total_count, ax=ax, fill=True, alpha=0.5, linewidth=1.5)

    # show(df)

    return df

if __name__ == "__main__":
    df = main()
