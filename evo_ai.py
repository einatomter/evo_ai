#!/usr/bin/env python3

import gym
import numpy as np
import random

# TODO: Rename variables to match terminology from lectures



def cellular_automaton(ruleset: str, radius, initial_values: str):
    '''
        Performs update step

        Ruleset is an array of possible rules

        Initial values is binary string from observations

        TODO: Add parameter for substr size (should be odd value?)
    '''

    # variable declaration
    new_values = ""


    print(f'initial values:\t{initial_values}')
    print(f'ruleset:\t{ruleset}')
    

    # TODO: range based on size of initial_values
    # range is size of cellular automaton
    for i in range(6):
        substr = ""
        for cell in range(radius, (radius+1)):
            substr += initial_values[(i + cell) % 6]

        # convert substr = decimal
        substr_10 = int(substr, 2)

        new_values += ruleset[substr_10]
    # /loop

    print(f'new values:\t{new_values}')
    
    return new_values

def ca_output(bitstring: str) -> bool:
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



# Generate random ruleset
# returns bitstring
def generate_rrs(subst_size):
    ''' 
        Generates a random ruleset based on the amount of neighbours.
        
        Input: size of substring (int)
        Returns: random bitsting within range (str)
    '''

    max_substrings = 2 ** subst_size
    max_rules = (2 ** max_substrings) - 1 # max 255
    
    rrs_dec = random.randrange(0, max_rules) # 140   10001100
    rrs_bit = format(rrs_dec, "b").zfill(max_substrings)

    return rrs_bit


def main():
    cellular_automaton(generate_rrs(5), 2, "101110")



if __name__ == "__main__":
    main()