from typing import List
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from matplotlib import colors

from icu import IcuBed
from patient import ScheduledPatient

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

class Animator:

    #colors
    cmap = colors.ListedColormap(['white', 'blue', 'red', 'green', 'orange', 'purple', 'magenta', 'cyan', 'olive'])

    def __init__(self, x_lim: int):
        
        #config
        plt.ion()
        self.fig, self.ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
        self.ax[0,1] = self.fig.add_subplot(2,2,2,projection='3d')

        #set x and y for occupied
        self.occup_x = []
        self.occup_y = []

        # set limit
        self.x_lim = x_lim

    def plot_occupied(self, step, value):

        # plot bed bezetting
        self.occup_x.append(step)
        self.occup_y.append(value)

        # Clear previous points from graph
        self.ax[0,0].clear()
        self.ax[0,0].plot(self.occup_x, self.occup_y)
        self.ax[0,0].set_xlim([0, self.x_lim])

        #pause
        plt.pause(0.01)

    def plot_beds(self, step, values: List[IcuBed]):

        #create array
        self.bed_occup_array = np.zeros((10, 10))

        #convert to 2d array
        for index, bed in enumerate(values):
            y_var = index % 10
            x_var = int(np.floor((index) / 10))

            # convert specialism into int
            specs = ['CAPU', 'CHIR', 'NEC', 'INT', 'NEU', 'CARD', 'OTHER']
            g_spec_i = 0
            if (bed.is_occupied()):
                g_spec = bed.get_patient().get_specialism()
                g_spec_i = specs.index(g_spec) + 1

            self.bed_occup_array[x_var][y_var] = g_spec_i

        self.ax[1,0].clear()

        # draw gridlines
        self.ax[1,0].grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        self.ax[1,0].set_xticks(np.arange(-.5, 10, 1));
        self.ax[1,0].set_yticks(np.arange(-.5, 10, 1));

        #plot
        self.ax[1,0].imshow(self.bed_occup_array, cmap = self.cmap)

    def plot_rescheduled(self, values: List[ScheduledPatient]):
        
        #filter
        rescheduled = [x for x in values if x.has_been_rescheduled]
        rescheduled.sort(key=lambda x: -x.patient_waiting_time)

        #transform
        x_arr = [index for index, x in enumerate(rescheduled)]
        y_arr = [x.patient_waiting_time for x in rescheduled]

        #display
        self.ax[1,1].clear()
        self.ax[1,1].bar(x_arr, y_arr)

    def plot_voxels(self, values: List[IcuBed]):

        size = 6

        # prepare some coordinates
        x, y, z = np.indices((size, size, 20))
        
        #create array
        bed_occup_array_3d = np.zeros((size, size, 20))
        
        #convert to 3d array
        for index, bed in enumerate(values):

            #get x and y
            y_var = index % size
            x_var = int(np.floor((index) / size))

            # set 3d range
            for i in range(20):
                is_occup = bed.is_occupied()
                disp_l = False
                if (is_occup):
                    max_hours = 120
                    curr_hours = bed.get_patient().hours_on_icu()
                    hour_i = np.floor(curr_hours / max_hours) + 1
                    disp_l = i < hour_i 
                bed_occup_array_3d[x_var][y_var][i] = is_occup & disp_l

        # and plot everything
        self.ax[0,1].clear()
        self.ax[0,1].voxels(bed_occup_array_3d, edgecolor='k')

        plt.show()