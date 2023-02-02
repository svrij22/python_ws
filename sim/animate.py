from typing import List, Union, Tuple, Dict

import matplotlib.style as mplstyle
import numpy as np
from matplotlib import colors
from matplotlib import pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D

from icu import IcuBed
from patient import ScheduledPatient

mplstyle.use('fast')


class BaseAnimator:
    ax: Union[plt.Axes, Axes3D]
    fig: plt.Figure
    pos_in_row: int
    pos_in_col: int
    this_ax: Union[plt.Axes, Axes3D]

    def __init__(self, pos_in_row: int, pos_in_col: int):
        self.pos_in_row = pos_in_row
        self.pos_in_col = pos_in_col

        try:
            self.this_ax = self.ax[self.pos_in_row, self.pos_in_col]
        except AttributeError as attr_error:
            print("The base class has not been setup yet. Try using BaseAnimator.setup() first.")
            raise attr_error

    @classmethod
    def setup(cls, n_cols: int, n_rows: int, figsize: Tuple[int, int]) -> None:
        plt.ion()
        cls.fig, cls.ax = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=figsize)


class LineAnimator(BaseAnimator):
    """
    Animates a linechart by plotting a line between two arrays of x- and y-axes.
    """
    x: List[Union[float, int]]
    y: List[Union[float, int]]
    x_lim: int

    def __init__(self, pos_in_row: int, pos_in_col: int, x_lim: int):
        """
        Sets the x-limit and initializes the x- and y-axes of a line graph.
        :param x_lim: The maximum plottable value on the x-axis.
        """
        super().__init__(pos_in_row, pos_in_col)

        self.x = []
        self.y = []

        self.x_lim = x_lim

    def plot(self, x_coord: Union[int, float], y_coord: Union[int, float]):
        """
        Plots a new point based on an x and y coordinate.
        """
        self.x.append(x_coord)
        self.y.append(y_coord)

        self.this_ax.clear()
        self.this_ax.plot(self.x, self.y)
        self.this_ax.set_xlim(left=0, right=self.x_lim)

        # When data that should be plotted is supplied before the previous step has been plotted the UI will crash.
        # plt.pause() will make sure there is enough time to plot.
        plt.pause(0.0001)


class MatrixAnimator(BaseAnimator):
    """
    An animated matrix chart where the color in each cell is mapped to a certain specialism.
    """
    grid_size: Tuple[int, int]

    SPECIALISM_MAP: Dict[str, int] = {'CAPU': 0, 'CHIR': 1, 'NEC': 2, 'INT': 3, 'NEU': 4, 'CARD': 5, 'OTHER': 6}
    COLOR_MAP = colors.ListedColormap(['white', 'blue', 'red', 'green', 'orange', 'purple', 'magenta', 'cyan', 'olive'])

    def __init__(self, pos_in_row: int, pos_in_col: int, grid_size: Tuple[int, int]):
        super().__init__(pos_in_row, pos_in_col)

        self.grid_size = grid_size

    def plot(self, icu_beds: List[IcuBed]):
        bed_occupancy: np.ndarray = np.zeros(self.grid_size)
        x: int
        y: int

        for index, bed in enumerate(icu_beds):
            y = index % self.grid_size[0]
            x = index // self.grid_size[1]

            bed_occupancy[x][y] = self.get_grid_color(bed)

        self.this_ax.clear()
        self.this_ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        self.this_ax.set_xticks(np.arange(-.5, self.grid_size[0], 1))
        self.this_ax.set_yticks(np.arange(-.5, self.grid_size[1], 1))

        self.this_ax.imshow(bed_occupancy, cmap=self.COLOR_MAP)

    def get_grid_color(self, bed: IcuBed):
        if bed.is_occupied():
            specialism = bed.get_patient().get_specialism()

            return self.SPECIALISM_MAP[specialism] + 1

        return 0


class VoxelAnimator(BaseAnimator):
    """
    A 3d graph which displays each bed on the x- and y-axes and the time it has been occupied by a single patient on the
    z-axis.
    """
    grid_x_y: int
    grid_z: int
    max_hours_in_icu: int

    def __init__(self, pos_in_row: int, pos_in_col: int, grid_x_y: int, grid_z: int, max_hours_in_icu: int):
        super().__init__(pos_in_row, pos_in_col)

        self.grid_x_y = grid_x_y
        self.grid_z = grid_z
        self.max_hours_in_icu = max_hours_in_icu

        self.ax[pos_in_row, pos_in_col] = self.fig.add_subplot(2, 2, 2, projection='3d')

    def plot(self, icu_beds: List[IcuBed]):
        bed_occup_array_3d = np.zeros((self.grid_x_y, self.grid_x_y, self.grid_z))

        # convert to 3d array
        for index, bed in enumerate(icu_beds):
            y = index % self.grid_x_y
            x = index // self.grid_x_y

            # set 3d range
            for z in range(20):
                bed_occup_array_3d[x][y][z] = self.display_voxel(bed, z)

        self.this_ax.clear()
        self.this_ax.voxels(bed_occup_array_3d, edgecolor='k')

    def display_voxel(self, bed: IcuBed, voxel_level: int) -> bool:
        """
        Checks whether a bed is occupied and whether the limit on the z-axis has been reached.
        :param bed: The bed to check.
        :param voxel_level: The current height of the bar drawn for this bed.
        :return: True if the bed is occupied and the bar has not reached the maximum height of the graph, False if
            either of these conditions have not been met
        """
        if not bed.is_occupied():
            return False

        hours_patient_in_icu: int = bed.get_patient().hours_on_icu()
        hour_i: int = hours_patient_in_icu // self.max_hours_in_icu + 1
        display_voxel: bool = voxel_level < hour_i

        return display_voxel


class BarAnimator(BaseAnimator):
    """
    A barchart which displays the amount people have been rescheduled on the x-axis and the amount of people that have
    been rescheduled on the y-axis.
    """

    def plot(self, values: List[ScheduledPatient]):
        rescheduled = [x for x in values if x.has_been_rescheduled]
        rescheduled.sort(key=lambda x: -x.patient_waiting_time)

        x_axis = range(len(rescheduled))
        y_axis = [x.patient_waiting_time for x in rescheduled]

        self.this_ax.clear()
        self.this_ax.bar(x_axis, y_axis)
