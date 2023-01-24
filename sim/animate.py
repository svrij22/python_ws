"""This module contains classes and functions to create animated matplotlib plots."""
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


class Animator:
    """Contains methods to help repeatedly draw a linegraph."""
    x_axis: list[int]
    y_axis: list[int]
    ax: Axes
    x_axis_limit: int

    def __init__(self, ax: Axes, x_axis_limit: int):
        """
        Initializes the animator by setting the x-limit of the graph and creating empty lists for the x- and y-axes.

        :param ax: A matplotlib.axes.Axes instance.
        :param x_axis_limit: The largest point displayed on the x-axis of the graph
        """
        self.x_axis = []
        self.y_axis = []
        self.ax = ax
        self.x_axis_limit = x_axis_limit

    def plot(self, x: int, y: int):
        """
        Clears and redraws the graph with a new point.

        :param x: The x coord of the new point.
        :param y: The y coord of the new point.
        """
        self.x_axis.append(x)
        self.y_axis.append(y)

        # Clear previous points from graph
        self.ax.clear()
        self.ax.plot(self.x_axis, self.y_axis)
        self.ax.set_xlim(0, self.x_axis_limit)

        # Pauses the graph for a small amount of time to give it time to draw. If this is removed the simulation will
        # finish before any point can be drawn causing the window to crash.
        plt.pause(0.01)
