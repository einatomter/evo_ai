#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


batch_no_list = []
fitness_list = []

fig = plt.figure() 
ax = fig.add_subplot(1, 1, 1)
    
def plot_vals(x_val, y_val):
    batch_no_list.append(x_val)
    fitness_list.append(y_val)

    plt.cla()
    plt.plot(batch_no_list, fitness_list)


ani = FuncAnimation(fig, plot_vals, interval = 1000)
plt.show()
