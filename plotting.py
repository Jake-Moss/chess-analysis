#!/usr/bin/env python3
import chess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from typing import List, Tuple, Dict
from string import ascii_letters


def gen_frequency() -> List[int]:
    """
    Generates 1x64 (8x8) freq array filled with 0
    Index via 1d array notation

    [0,0,...]
    """
    return [0 for _ in range(64)]


def lost_piece_heat_single_user(df: pd.DataFrame, username: str, colour: bool, patterns: List[int] = list(chess.PIECE_TYPES), number_of_moves: int = 0) \
                                -> np.ndarray:
    """
    Iterates over all rows in data frame supplied. Condition it before passing.

    piece is int rather than string as python-chess uses int in backed.
    """
    df_username = (df["White"] == username) | (df["Black"] == username) # GETS GAMES WHERE USERNAME PLAYED REGAURD LESS OF COLOUR

    colour_played = (df[df_username]["White"] == username).to_numpy() # zip colour played and df["Lost pieces"].to_numpy
    # to get the colour played on each game with the pieces lost of that colour.
    frequency = gen_frequency()

    for lost_pieces, colour_in_game in zip(df["Lost pieces"].to_numpy(), colour_played):
        if colour_in_game == colour:
            for piece in lost_pieces[colour]:
                if piece[0] in patterns:
                    frequency[piece[1]] += 1

    return np.reshape(frequency, (8, 8))


def lost_piece_heat(df: pd.DataFrame, colour: bool, patterns: List[int] = list(chess.PIECE_TYPES), number_of_moves: int = 0) \
                    -> np.ndarray:
    """
    Iterates over all rows in data frame supplied. Condition it before passing.

    piece is int rather than string as python-chess uses int in backed.

    Modifies board such that black and whites pov's are the same
    """

    frequency = gen_frequency()

    for lost_pieces in df["Lost pieces"].to_numpy():
        for piece in lost_pieces[colour]:
           if piece[0] in patterns:
               frequency[piece[1]] += 1


    return np.reshape(frequency, (8, 8))


def lost_piece_freq_single_user(df: pd.DataFrame, username: str, colour: bool, patterns: List[int] = list(chess.PIECE_TYPES), number_of_moves: int = 0) \
                                -> np.ndarray:
    """
    Iterates over all rows in data frame supplied. Condition it before passing.

    piece is int rather than string as python-chess uses int in backed.
    """
    df_username = (df["White"] == username) | (df["Black"] == username)

    colour_played = (df[df_username]["White"] == username).to_numpy() # zip colour played and df["Lost pieces"].to_numpy
    # colour_played = df_username.to_numpy() # zip colour played and df["Lost pieces"].to_numpy
    total_count = []

    for lost_pieces, colour_in_game in zip(df["Lost pieces"].to_numpy(), colour_played):
        if colour_in_game == colour:
            for piece in lost_pieces[colour]:
                if piece[0] in patterns:
                    total_count.append(piece[2])

    return np.array(total_count)


def lost_piece_freq(df: pd.DataFrame, colour: bool, patterns: List[int] = list(chess.PIECE_TYPES), number_of_moves: int = 0) \
                    -> np.ndarray:
    """
    Iterates over all rows in data frame supplied. Condition it before passing.

    piece is int rather than string as python-chess uses int in backed.
    """
    total_count = []

    for lost_pieces in df["Lost pieces"].to_numpy():
        for piece in lost_pieces[colour]:
            if piece[0] in patterns:
                total_count.append(piece[2])

    return np.array(total_count)


def subplot_matrix_format(axs: np.ndarray, grid: Tuple[int, int], pieces_labels: list[str] , col_labels: List[str]):
    """
    Formats the sub plots grid provided such that the axis labels are only
    on the left and bottom plots. Assumes full NxM grid of subplots.
    """
    #axs is np.ndarry[np.ndarry[plt.Axes]] but type hints wont work for some reason?

    if np.size(axs) == max(grid): # Make types consistent ffs
        axs = np.reshape(axs, grid)

    for row in range(grid[0]):
        for col in range(grid[1]):
            axs[row][col].set_ylabel(pieces_labels[row], loc='center')
            axs[row][col].set_xlabel(col_labels[col], loc='center')

            if (not row == grid[0] - 1 ) and (not col == 0):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=False,
                    bottom=False,
                    labelleft=False,
                    left=False,
                    labelrotation=0
                )
                axs[row][col].xaxis.label.set_visible(False)
                axs[row][col].yaxis.label.set_visible(False)
            if (row == grid[0] - 1):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=True,
                    bottom=True,
                    labelleft=False,
                    left=False,
                    labelrotation=0
                )
                axs[row][col].xaxis.label.set_visible(True)
                axs[row][col].yaxis.label.set_visible(False)
            if (col == 0):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=False,
                    bottom=False,
                    labelleft=True,
                    left=True,
                    labelrotation=0
                )
                axs[row][col].xaxis.label.set_visible(False)
                axs[row][col].yaxis.label.set_visible(True)
            if (row == grid[0] - 1) and (col == 0):
                axs[row][col].tick_params(
                    axis='both',
                    labelbottom=True,
                    bottom=True,
                    labelleft=True,
                    left=True,
                    labelrotation=0
                )
                axs[row][col].xaxis.label.set_visible(True)
                axs[row][col].yaxis.label.set_visible(True)


def normalise(data: np.ndarray) -> Tuple[np.ndarray, float]:
    normalised = data/np.sum(data)
    return normalised, np.max(normalised)


def plot_heatmap_grid(dfs: List, pieces: List[int], col_labels: List[str], colour: bool, \
                      username: str = "", cmap = sns.diverging_palette(230, 20, as_cmap=True)) \
                      -> Tuple[plt.Figure, np.ndarray]:

    """
    Plots a grid of heat maps. Data MUST be preconditioned.
    axs is np.ndarry[np.ndarry[plt.Axes]] but type hints wont work for some reason?
    """


    grid = (len(pieces), len(dfs))

    local_maxs = []
    normalised = [[] for _ in range(grid[0])]
    for row in range(grid[0]):
        piece = pieces[row]
        for col in range(grid[1]):
            if username: # non-empty evals to true
                freq, local_max = normalise(
                    lost_piece_heat_single_user(dfs[col], username, colour, [piece])
                )
            else:
                freq, local_max = normalise(
                    lost_piece_heat(dfs[col], colour, [piece])
                )
            local_maxs.append(local_max)
            normalised[row].append(freq)

    global_max = max(local_maxs)

    fig, axs = plt.subplots(nrows = grid[0], ncols = grid[1])
    fig.suptitle("{}{} pieces captured.".format(str(username) + "'s " if username else "",['White', 'Black'][colour]))

    if np.size(axs) == max(grid): # Make types consistence smh matplotlib
        axs = np.reshape(axs, grid)

    fig.subplots_adjust(right=0.8)

    cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])

    for row in range(grid[0]):
        for col in range(grid[1]):
            sns.heatmap(
                data=normalised[row][col],
                vmin=0,
                vmax=global_max,
                cbar=True,
                ax=axs[row][col],
                cmap=cmap,
                square=True,
                cbar_ax=cbar_ax,
                xticklabels=list(ascii_letters[:8]),
                yticklabels=range(8,0,-1),
            )

    subplot_matrix_format(axs, grid, [chess.PIECE_NAMES[x].capitalize() for x in pieces], col_labels)
    fig.savefig(f"./images/{username}_HEATMAP_{'_'.join([chess.PIECE_NAMES[x].capitalize() for x in pieces])}_{['BLACK', 'WHITE'][colour]}.png")
    return fig, axs


def plot_heatmap_single_piece(df: pd.DataFrame, pieces: List[int], username: str = "", \
                              cmap = sns.diverging_palette(230, 20, as_cmap=True)) \
                              -> Tuple[plt.Figure, np.ndarray]:

    col_labels = ["Black", "White"]
    local_maxs = []
    normalised = [
         # chess.BLACK
         # chess.WHITE
    ]
    for colour in [chess.BLACK, chess.WHITE]:
        if username: # non-empty evals to true
            freq, local_max = normalise(
                lost_piece_heat_single_user(df, username, colour, pieces)
            )
        else:
            freq, local_max = normalise(
                lost_piece_heat(df, colour, pieces)
            )
        local_maxs.append(local_max)
        normalised.append(freq)

    global_max = max(local_maxs)

    fig, axs = plt.subplots(nrows = 1, ncols = 2)
    fig.suptitle("{} {} captured.".format(" and ".join(['Black', 'White']), "s, ".join([chess.PIECE_NAMES[piece].capitalize() for piece in pieces]) + "s"))

    axs = np.reshape(axs, (1, 2))

    fig.subplots_adjust(right=0.8)

    cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])

    for colour in [int(chess.BLACK), int(chess.WHITE)]: # see below for reason of werid cast
        sns.heatmap(
            data=normalised[colour],
            vmin=0,
            vmax=global_max,
            cbar=True,
            ax=axs[0][colour], # numpy arrays cannot be index by bools like normal arrays this took way to long to figure out. Normal arrays can cause the bools are duck typed to ints but not numpy arrays the special bastards
            cmap=cmap,
            square=True,
            cbar_ax=cbar_ax,
            xticklabels=list(ascii_letters[:8]),
            yticklabels=range(8,0,-1),
        )

    subplot_matrix_format(axs, (1, 2), [chess.PIECE_NAMES[piece].capitalize() for piece in pieces], col_labels)
    fig.savefig(f"./images/{username}_HEATMAP_{'_'.join([chess.PIECE_NAMES[x].capitalize() for x in pieces])}.png")
    return fig, axs


def plot_hist_grid(dfs: List, pieces: List[int], col_labels: List[str], colour: bool, \
                      username: str = "", cmap = sns.diverging_palette(230, 20, as_cmap=True), kde: bool =False) \
                      -> Tuple[plt.Figure, np.ndarray]:

    """
    Plots a grid of heat maps. Data MUST be preconditioned.
    axs is np.ndarry[np.ndarry[plt.Axes]] but type hints wont work for some reason?
    """


    grid = (len(pieces), len(dfs))

    local_greatest = []
    data = [[] for _ in range(grid[0])]
    for row in range(grid[0]):
        piece = pieces[row]
        for col in range(grid[1]):
            if username: # non-empty evals to true
                move_numbers = lost_piece_freq_single_user(dfs[col], username, colour, [piece])
            else:
                move_numbers = lost_piece_freq(dfs[col], colour, [piece])
            data[row].append(move_numbers)
            local_greatest.append(np.max(move_numbers) if move_numbers.size != 0 else 0)

    highest_move = max(local_greatest)
    fig, axs = plt.subplots(nrows = grid[0], ncols = grid[1])
    fig.suptitle("{} {} captured through time.".format(['Black', 'White'][colour], "s, ".join([chess.PIECE_NAMES[piece].capitalize() for piece in pieces]) + "s"))

    if np.size(axs) == max(grid): # Make types consistence smh matplotlib
        axs = np.reshape(axs, grid)

    if kde:
        for row in range(grid[0]):
            for col in range(grid[1]):
                sns.kdeplot(
                    data=data[row][col],
                    ax=axs[row][col],
                    # cmap=cmap,
                    fill=True,
                    common_norm=True,
                )
                axs[row][col].set_xlim(right=highest_move)
    else:
        for row in range(grid[0]):
            for col in range(grid[1]):
                sns.histplot(
                    data=data[row][col],
                    ax=axs[row][col],
                    # cmap=cmap,
                    common_norm=True,
                    binwidth=2,
                )
                axs[row][col].set_xlim(right=highest_move)

    subplot_matrix_format(axs, grid, [chess.PIECE_NAMES[x].capitalize() for x in pieces], col_labels)
    fig.savefig(f"./images/{username}_{'KDE' if kde else 'HIST'}_{'_'.join([chess.PIECE_NAMES[x].capitalize() for x in pieces])}_{['BLACK', 'WHITE'][colour]}.png")
    return fig, axs


def plot_hist_single_piece(df: pd.DataFrame, pieces: List[int], \
                      username: str = "", kde: bool = False) \
                      -> Tuple[plt.Figure, np.ndarray]:

    col_labels = ["Black", "White"]

    local_greatest = []
    data = []
    for colour in [chess.BLACK, chess.WHITE]:
        if username: # non-empty evals to true
            move_numbers = lost_piece_freq_single_user(df, username, colour, pieces)
        else:
            move_numbers = lost_piece_freq(df, colour, pieces)
        data.append(move_numbers)
        print(move_numbers)
        local_greatest.append(np.max(move_numbers) if move_numbers.size != 0 else 0)

    highest_move = max(local_greatest)
    fig, axs = plt.subplots(nrows = 1, ncols = 2)
    fig.suptitle("{} {} captured through time.".format(" and ".join(['Black', 'White']), "s, ".join([chess.PIECE_NAMES[piece].capitalize() for piece in pieces]) + "s"))

    axs = np.reshape(axs, (1, 2))

    if kde:
        for colour in [int(chess.BLACK), int(chess.WHITE)]: # see below for reason of werid cast
            sns.kdeplot(
                data=data[colour],
                ax=axs[0][colour],
                fill=True,
                common_norm=True,
            )
            axs[0][colour].set_xlim(right=highest_move)
    else:
        for colour in [int(chess.BLACK), int(chess.WHITE)]: # see below for reason of werid cast
            sns.histplot(
                data=data[colour],
                ax=axs[0][colour],
                common_norm=True,
                binwidth=2,
            )
            axs[0][colour].set_xlim(right=highest_move)

    subplot_matrix_format(axs, (1, 2), [chess.PIECE_NAMES[x].capitalize() for x in pieces], col_labels)
    fig.savefig(f"./images/{username}_{'KDE' if kde else 'HIST'}_{'_'.join([chess.PIECE_NAMES[x].capitalize() for x in pieces])}_{['BLACK', 'WHITE'][colour]}.png")
    return fig, axs
