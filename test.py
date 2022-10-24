#!/usr/bin/env python3

import numpy as np
import pandas as pd


test_list = [['a', 7],
             ['b', 1],
             ['c', 8],
             ['d', 4],
             ['e', 5],
             ['f', 3],
             ['g', 2],
             ['h', 10],
            ]

def bit_flip(ch):
    bit = str(1 - int(ch))
    return bit


def truncation(population: list, n: int) -> list:
    '''
        Returns list of best individuals
    '''
    
    chosen = []

    population = sorted(population, key=lambda x: x[1], reverse=1)
    for i in range (n):
        
        chosen.append(population[i])

    return chosen



def n_point_crossover(parent1: str, parent2: str, cut_points: list) -> str:
    '''
        Performs nonvariable length crossover at cut points
    '''
    offspring = ""
    start_point = 0

    for i in range(len(cut_points)):
        if i % 2 == 0:
            offspring += parent1[start_point:cut_points[i]]
        else:
            offspring += parent2[start_point:cut_points[i]]

        start_point = cut_points[i]

    print(offspring)
    return offspring

def n_point_crossover2(parent1: str, parent2: str, cut_points: list) -> str:
    '''
        Performs nonvariable length crossover at cut points
    '''
    offspring = ""
    start_point = 0
    switch = False

    for i in range(len(parent1)):
        if i in cut_points:
            switch = not switch
        if not switch:
            offspring += parent1[i]
        else:
            offspring += parent2[i]

    print(offspring)
    return offspring

def CA_propagate(ruleset: str, radius: int, initial_values: str) -> str:
    '''
        Performs update step

        Ruleset is an array of possible rules

        Initial values is binary string from observations

        Returns: 
            new_values
    '''

    # variable declaration
    CA_length = len(initial_values)
    current_values = initial_values

    print(initial_values)

    #print(f'initial values:\t{initial_values}')
    #print(f'ruleset:\t{ruleset}')
    
    # range is size of cellular automaton/initial value
    for _ in range(CA_length):
        new_values = ""
        for j in range(CA_length):
            substr = ""
            for cell in range(-radius, radius+1):
                substr += current_values[(j + cell) % CA_length]

            # convert substr = decimal
            substr_10 = int(substr, 2)
            new_values += ruleset[substr_10]
        # /loop through CA row
        print(new_values)
        current_values = new_values
    # /loop through new CA

    #print(f'new values:\t{new_values}')
    
    return new_values


# ca = CA_propagate("01101110", 1, "00111101101010")
# print()
# print(ca)

# dec_angle = 0.42

# min_angle = -0.42
# max_angle = 0.42
# resolution = 10

# dec_angle = round(np.interp(dec_angle, [min_angle, max_angle], [0, 2**resolution - 1]))
# print(dec_angle)

# bin_angle = format(dec_angle, "b")
# bin_angle = bin_angle.zfill(resolution)

# print(bin_angle)

# result = truncation(test_list, 2)

# print(result)

# print(bit_flip("1"))
# print(type(bit_flip("0")))

# print(n_point_crossover2("1234", "00006", [2, 3]))

min_angle = -0.2095
max_angle = 0.2095
resolution = 20

# print(intervals)

# # print(list)
# bins_angle = pd.cut([min_angle, max_angle], resolution, retbins = True)
# print(bins_angle)
# # print(pd.value_counts(bins_angle))

intervals = np.linspace(min_angle, max_angle+0.1*max_angle, 20)

observation = 0.1

bin_observation = ""
for i in range(len(intervals)-1):
    if observation >= intervals[i] and observation < intervals[i+1]:
        bin_observation += "1"
    else:
        bin_observation += "0"

print(bin_observation)

# best genome for seed 42 so far: 11100001100010011011100010101100
# best genome random: 01101001101000111101101010110001
# best genome random rad 3: 11100111100001100111000011010001110001000100101001000111111100001100000000011111111100011100101011110100101000000100001011010010

# over night, random rad 3
# best genome that stagneted latest (378, 356 avg test): 11101100000100001011101000011010111101110001111010111010010010000101110001101001101010011010101010010010000111111011010001010000
# a genome that stagnated for longer but earlier (338, 311 avg test): 11100100010001111011101110101001010100100011110110111011110000010110100010101001111010001011000110010110001001110010000101011101

# 1,5 hour, random rad 3, velocity 5
# (390, 410 avg test): 10011010010000100011111110101010100000101110011110110100100111101101110010100010101010100100010010101000110011001010110111110001

# over night, random rad 2, old evolve model
# randomly picked gen (around 1600) with high max out of total 2k gens, (280avg test): 10001100110001111001110010000011
# same training as last one, but genome from the latest generation that stagnated for a while (100avg test): 01011110101010001011010001100010

