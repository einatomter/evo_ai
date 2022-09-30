#!/usr/bin/env python3

import gym
import numpy as np
import random

# TODO: Rename variables to match terminology from lectures

fitness_list = []
    
def CA_propagate(ruleset: str, radius: int, initial_values: str) -> str:
    '''
        Performs update step

        Ruleset is an array of possible rules

        Initial values is binary string from observations

        Returns: new_values

        TODO: Add parameter for substr size (should be odd value?)
    '''

    # variable declaration
    CA_length = len(initial_values)
    new_values = ""

    #print(f'initial values:\t{initial_values}')
    #print(f'ruleset:\t{ruleset}')
    
    # range is size of cellular automaton/initial value
    for i in range(CA_length):
        substr = ""
        for cell in range(-radius, radius+1):
            substr += initial_values[(i + cell) % CA_length]

        # convert substr = decimal
        substr_10 = int(substr, 2)
        new_values += ruleset[substr_10]
    # /loop

    #print(f'new values:\t{new_values}')
    
    return new_values


def CA_majority(bitstring: str) -> bool:
    '''
        Determines action of the cart.
        Currently decides based on majority vote.

        0 = left, 1 = right
    '''
    
    ones = bitstring.count('1')
    zeros = bitstring.count('0')

    if ones >= zeros:
        return 1
    else:
        return 0


def gen_rrs(radius: int) -> str:
    ''' 
        Generates a random ruleset based on the amount of neighbours.
        
        Input: size of substring (int)
        Returns: random bitsting within range (str)
    '''
    subst_size = (radius * 2) + 1
    max_substr = 2 ** subst_size
    max_rules = (2 ** max_substr) - 1 # max 255
    
    rrs_dec = random.randrange(0, max_rules) # 140   10001100
    rrs_bit = format(rrs_dec, "b").zfill(max_substr)

    return rrs_bit


def fitness_track(ruleset: str, total_time: float):

    if fitness_list:
        if total_time > fitness_list[0][1]:
            fitness_list.insert(0, [ruleset, total_time])
    else:
        fitness_list.append([ruleset, total_time])

    # alternative to do sorting, but I guess only if we need to sort once. it will sort by time
    #fitness_list.append([ruleset, total_time])
    #fitness_list = sorted(fitness_list, key=lambda x: x[1])
    

def print_fitness():
    print(f'fitness list: {fitness_list}')
    




#def main():
    #cellular_automaton(gen_rrs(5), 2, "101110")



#if __name__ == "__main__":
    #main()