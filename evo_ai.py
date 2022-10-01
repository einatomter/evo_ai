#!/usr/bin/env python3

from ctypes import sizeof
import gym
import numpy as np
import random

# TODO: Rename variables to match terminology from lectures





def CA_initialize(): #or CA_run?

    population = []
    time = 0
    dec_angle = 0
    i = 0

    #env = gym.make("CartPole-v1", render_mode="human")
    env = gym.make("CartPole-v1")
    observation, info = env.reset(seed=42)
    ruleset = gen_rrs(cfg_radius)

    for _ in range(10000):
        
        dec_angle = observation[2]
        bin_angle = format(24 + round(dec_angle * 180/np.pi), "b") # negative angles are 0-23, positive angles are 24-48
        bin_angle = bin_angle.zfill(6)
        action = CA_majority(CA_propagate(ruleset, cfg_radius, bin_angle))
        observation, reward, terminated, truncated, info = env.step(action)
        time += reward

        if terminated:
            if len(population) < 5:
                if time > 30:
                    print(f'ruleset:\t{ruleset} \ttime: {time}')
                    #population[ruleset] = time
                    population.append([ruleset, time])

                ruleset = gen_rrs(cfg_radius)

            else:
                # perform evolution

                # step 1: evolve rules
                if i == len(population):
                    print()
                    for rule in population:
                        # print(f'ruleset:\t{rule}')

                    population = evolve(population)
                    i = 0
                    ruleset = population[i][0]
                # step 2: loop through rules -> save new fitness score
                else:
                    population[i][1] = time
                    if i != len(population):
                        ruleset = population[i][0]
                    i += 1


            time = 0
            observation, info = env.reset()

    # print(population)
    env.close()
    



def CA_propagate(ruleset: str, radius: int, initial_values: str) -> str:
    '''
        Performs update step

        Ruleset is an array of possible rules

        Initial values is binary string from observations

        Returns: new_values
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

        Returns: 0 (left), 1 (right)
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




# TODO: terminology
def evolve(population):
    '''
        Performs evolution (tm)

        Input: list containing population of genomes (rules)
        Returns: list containing new population
    '''

    # print(f'old population: {population}')

    

    population_new = population



    # print(f'new population: {population_new}')

    return population_new




# def fitness_track(ruleset: str, total_time: float, population: dict):

#     # if population:
#     #     if total_time > population[0][1]:
#     #         population.insert(0, [ruleset, total_time])
#     # else:
#     #     population.append([ruleset, total_time])

#     # alternative to do sorting, but I guess only if we need to sort once. it will sort by time
#     population.append([ruleset, total_time])
#     population = sorted(population, key=lambda x: x[1])

# ------------------------------------
# main
# ------------------------------------




cfg_radius = 2 # neighbours = radius/2



def main():
    # cellular_automaton(gen_rrs(5), 2, "101110")
    CA_initialize()
    

if __name__ == "__main__":
    main()