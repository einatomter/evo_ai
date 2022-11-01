#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import numpy as np


    
plt.style.use('fivethirtyeight')

def animate(i):
    data = pd.read_csv(sys.argv[1], header=None, skiprows=1)
    data2 = np.loadtxt(sys.argv[1], delimiter=",", skiprows=1) #this is jank, but it works
    
    x = data[0]
    y1 = data[1]
    y2 = data[2]

    data2_x = data2[:,:1]
    data2_y = data2[:,3:]

    plt.cla()

    plt.plot(x, y1, lw = 2, label='Average_fitness', color='black')
    plt.plot(x, y2, lw = 2, label='Max fitness')

    best_fit_x = []
    best_fit_y = []

    for xe, ye in zip(data2_x, data2_y):
        all_x = [xe[0]] * len(ye)
        plt.scatter(all_x, ye, color='red', alpha=0.5, s=2)
        best_fit_x.extend(all_x)
        best_fit_y.extend(ye)
    
    #polynomial regression, 2nd order
    theta_ofAll = np.polyfit(best_fit_x, best_fit_y, 2)
    Polynomial = np.polyval(theta_ofAll, data2_x)
    plt.plot(data2_x, Polynomial, '-', label = 'Polyfit of population', lw = 2, color='grey')

    theta_ofBest = np.polyfit(x, y2, 2)
    Polynomial2 = np.polyval(theta_ofBest, x)
    plt.plot(x, Polynomial2, '-', label = 'Polyfit best genomes', lw = 2, color='green')

    plt.xlabel("Generations", fontsize = "small")
    plt.ylabel("Fitness score", fontsize = "small")
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.legend(loc='upper left', fontsize = "small")
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()