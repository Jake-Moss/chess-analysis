import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

data = np.array([0, 0, 0, 0, 0, 0, 0, 0, 29, 54, 52, 16, 7, 66, 40, 34, 18, 45, 69, 67, 82, 52, 31, 22, 12, 67, 88, 228, 278, 49, 51, 12, 5, 10, 44, 110, 60, 28, 16, 5, 7, 16, 32, 21, 14, 36, 8, 7, 4, 1, 5, 4, 6, 4, 1, 0, 0, 2, 2, 4, 0, 1, 0, 4])
data1 = np.array([1000, 0, 0, 0, 0, 0, 0, 0, 29, 54, 52, 16, 7, 66, 40, 34, 18, 45, 69, 67, 82, 52, 31, 22, 12, 67, 88, 228, 278, 49, 51, 12, 5, 10, 44, 110, 60, 28, 16, 5, 7, 16, 32, 21, 14, 36, 8, 7, 4, 1, 5, 4, 6, 4, 1, 0, 0, 2, 2, 4, 0, 1, 0, 4])

data = data/np.sum(data)
data1 = data1/np.sum(data1)

maximum = np.max([data1, data])

data1 = np.reshape(data1, (8,8))
data = np.reshape(data, (8,8))
# fig = plt.figure()
# gs = GridSpec(2, 2, figure=fig)
# ax1 = fig.add_subplot(gs[0, 0])
# ax2 = fig.add_subplot(gs[0, 1])
# ax3 = fig.add_subplot(gs[1, 0])
# ax4 = fig.add_subplot(gs[1, 1])

# ax5 = fig.add_subplot(gs[:, 2])

# im1 = ax1.imshow(data)
# im2 = ax2.imshow(data, vmin=0, vmax=0.5)
# im3 = ax3.imshow(data1) # normalise to total pieces lost is good

# im4 = ax4.imshow(data1, vmin=0, vmax=maximum)

"""Normalise numbers to local max,
normalise colour to global max of normalised locals"""



# im1 = ax1.imshow(data)
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.


cmap = sns.diverging_palette(230, 20, as_cmap=True)

fig, axs = plt.subplots(nrows=2, ncols=2)

fig.subplots_adjust(right=0.8)

cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])

sns.heatmap(data, vmin=0, vmax=maximum, cbar=True, ax=axs[0][0], cmap=cmap, square=True, cbar_ax=cbar_ax)
sns.heatmap(data, vmin=0, vmax=maximum, cbar=True, ax=axs[0][1], cmap=cmap, square=True, cbar_ax=cbar_ax)
sns.heatmap(data1, vmin=0, vmax=maximum, cbar=True, ax=axs[1][0], cmap=cmap, square=True, cbar_ax=cbar_ax)
sns.heatmap(data1, vmin=0, vmax=maximum, cbar=True, ax=axs[1][1], cmap=cmap, square=True, cbar_ax=cbar_ax)

# plt.colorbar(ax=axs[0][0], cax=cbar_ax, orientation="vertical")

plt.show(block=False)
