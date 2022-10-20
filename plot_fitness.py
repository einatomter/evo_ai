#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


    
plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

def animate(i):
    data = pd.read_csv('log.csv')
    x = data['generation']
    y1 = data['average_fitness']
    y2 = data['max_fitness']

    plt.cla()

    plt.plot(x, y1, label='Average_fitness')
    plt.plot(x, y2, label='Max fitness')

    plt.xlabel("Generations")
    plt.ylabel("Fitness score")

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()