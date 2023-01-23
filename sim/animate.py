from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import time
from settings import Settings


class Animator:
    def __init__(self, ax: Axes, x_lim: int):
        self.x = []
        self.y = []
        self.ax = ax
        self.x_lim = x_lim

    def plot(self, x, y):
        self.x.append(x)
        self.y.append(y)

        # Clear previous points from graph
        self.ax.clear()
        self.ax.plot(self.x, self.y)
        self.ax.set_xlim([0, self.x_lim])

        plt.pause(0.01)
