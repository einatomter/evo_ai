#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
    
plt.style.use('fivethirtyeight')

def animate(i):
    data = pd.read_csv(sys.argv[1], header=None, skiprows=1)
    #data2 = np.loadtxt(sys.argv[1], delimiter=",", skiprows=1) #this is jank, but it works for scatterplot
    
    x = data[0] # generations
    y1 = data[1] # fitness average of generation
    y2 = data[2] # best fitness of generation

    plt.cla()

    plt.plot(x, y1, lw = 2, label='Average_fitness', color='black')
    plt.plot(x, y2, lw = 2, label='Max fitness')

    # for scatterplot
    # data2_x = data2[:,:1]
    # data2_y = data2[:,3:]
    # best_fit_x = []
    # best_fit_y = []
    # for xe, ye in zip(data2_x, data2_y):
    #     all_x = [xe[0]] * len(ye)
    #     plt.scatter(all_x, ye, color='red', alpha=0.5, s=2)
    #     best_fit_x.extend(all_x)
    #     best_fit_y.extend(ye)
    
    #linear regression of average fitness
    theta_ofAll = np.polyfit(x, y1, 1)
    Polynomial = np.polyval(theta_ofAll, x)
    plt.plot(x, Polynomial, '-', label = 'Polyfit of population', lw = 2, color='green')

    #linear regression of max fitness
    theta_ofBest = np.polyfit(x, y2, 1)
    Polynomial2 = np.polyval(theta_ofBest, x)
    plt.plot(x, Polynomial2, '-', label = 'Polyfit best genomes', lw = 2, color='red')

    plt.xlabel("Generations", fontsize = "small")
    plt.ylabel("Fitness score", fontsize = "small")
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.legend(loc='upper left', fontsize = "small")
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()