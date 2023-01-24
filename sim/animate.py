from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from matplotlib import colors

cmap = colors.ListedColormap(['white', 'blue'])

class Animator:

    def __init__(self, ax: Axes, x_lim: int):
        self.x = []
        self.y = []

        self.ax = ax
        self.x_lim = x_lim

    def plot(self, step, value):
        self.x.append(x)
        self.y.append(y)

        # Clear previous points from graph
        self.ax.clear()
        self.ax.plot(self.x, self.y)
        self.ax.set_xlim([0, self.x_lim])

        plt.pause(0.01)
