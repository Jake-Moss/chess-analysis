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


def lost_piece_heat(df: pd.DataFrame, colour: bool, patterns: List[int] = list(chess.PIECE_TYPES), number_of_moves: int = 0) \
                    -> np.ndarray:
    """
    Iterates over all rows in data frame supplied. Condition it before passing.

    piece is int rather than string as python-chess uses int in backed.
    """
    frequency = gen_frequency()

    for lost_pieces in df["Lost pieces"].to_numpy():
        for piece in lost_pieces[colour]:
            if piece[0] in patterns:
                frequency[piece[1]] += 1

    return np.reshape(frequency, (8, 8))


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
    if np.size(axs) == max(grid):
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
                )
                axs[row][col].xaxis.label.set_visible(True)
                axs[row][col].yaxis.label.set_visible(True)



def normalise(data: np.ndarray) -> Tuple[np.ndarray, float]:
    normalised = data/np.sum(data)
    return normalised, np.max(normalised)


def plot_heatmap_grid(dfs: List[pd.DataFrame], pieces: List[int], \
                      cmap = sns.diverging_palette(230, 20, as_cmap=True)) \
                      -> Tuple[plt.Figure, plt.Axes]:

    """Plots a grid of heat maps. Data MUST be preconditioned."""


    grid = (len(pieces), len(dfs))

    local_maxs = []
    normalised = [[] for _ in range(grid[0])]
    for row in range(grid[0]):
        piece = pieces[row]
        for col in range(grid[1]):
            freq, local_max = normalise(lost_piece_heat(dfs[col], chess.BLACK, [piece]))
            local_maxs.append(local_max)
            normalised[row].append(freq)

    global_max = max(local_maxs)

    fig, axs = plt.subplots(nrows = grid[0], ncols = grid[1])

    fig.subplots_adjust(right=0.8)

    cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])

    for row in range(grid[0]):
        for col in range(grid[1]):
            ax = axs[row][col]
            sns.heatmap(
                normalised[row][col],
                vmin=0,
                vmax=global_max,
                cbar=True,
                ax=ax,
                cmap=cmap,
                square=True,
                cbar_ax=cbar_ax,
                xticklabels=list(ascii_letters[:8]),
                yticklabels=range(8,0,-1),
            )

    subplot_matrix_format(axs, grid, [chess.PIECE_NAMES[x].capitalize() for x in pieces], ["a", "b", "df", "sdfs", "eesfs", "testing", "long"])
    return fig, axs
