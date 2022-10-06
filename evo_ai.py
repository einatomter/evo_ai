#!/usr/bin/env python3

from ctypes import sizeof
import gym
import numpy as np
import pandas as pd
import random


# for writing yaml configs
import yaml
from yaml.loader import SafeLoader

# TODO: Rename variables to match terminology from lectures

# phenotype: ruleset
# genotype: 100101101101

# max population
POPULATION = 100
SEED = 42

def CA_initialize(generate_random: bool = False): #or CA_run?

    population = []
    time = 0
    dec_angle = 0
    i = 0
    batch_no = 0
    tests = 4
    j = 0

    min_position = -4.8
    max_position = 4.8
    min_velocity = -4
    max_velocity = 4
    min_angle = -0.42
    max_angle = 0.42
    min_ang_velocity = -4
    max_ang_velocity = 4
    resolution = 10
    space_between_observations = 2

    # env = gym.make("CartPole-v1", render_mode="human")
    env = gym.make("CartPole-v1")
    observation, info = env.reset()
    ruleset = gen_rrs(cfg_radius)

    if generate_random:
        for i in range(POPULATION):
            population.append([gen_rrs(cfg_radius), 0])


    #for _ in range(10000):
    while True:
        observation_ca = "00"

        dec_position = observation[0]
        dec_position = round(np.interp(dec_position, [min_position, max_position],
                                         [0, 2**resolution - 1])) # mapping to non-negative values
        bin_position = format(dec_position, "b")
        bin_position = bin_position.zfill(resolution)

        observation_ca += bin_position
        for _ in range(space_between_observations):
            observation_ca += "0"

        dec_velocity = observation[1]
        dec_velocity = round(np.interp(dec_velocity, [min_velocity, max_velocity],
                                         [0, 2**resolution - 1])) # mapping to non-negative values
        bin_velocity = format(dec_velocity, "b")
        bin_velocity = bin_velocity.zfill(resolution)

        observation_ca += bin_velocity
        for _ in range(space_between_observations):
            observation_ca += "0"

        dec_angle = observation[2]
        dec_angle = round(np.interp(dec_angle, [min_angle, max_angle],
                                     [0, 2**resolution - 1]))
        bin_angle = format(dec_angle, "b")
        bin_angle = bin_angle.zfill(resolution)

        observation_ca += bin_angle
        for _ in range(space_between_observations):
            observation_ca += "0"

        dec_ang_velocity = observation[3]
        dec_ang_velocity = round(np.interp(dec_ang_velocity, [min_ang_velocity, max_ang_velocity],
                                     [0, 2**resolution - 1]))
        bin_ang_velocity = format(dec_ang_velocity, "b")
        bin_ang_velocity = bin_ang_velocity.zfill(resolution)
        
        observation_ca += bin_ang_velocity

        # print(f'observation: {observation}')
        # print(f'length: {len(observation_ca)} observation: {observation_ca}')

        action = CA_majority(CA_propagate(ruleset, cfg_radius, observation_ca))
        observation, reward, terminated, truncated, info = env.step(action)
        time += reward

        if terminated or truncated:
            if len(population) < POPULATION:
                if time > 50:
                    population.append([ruleset, time])

                ruleset = gen_rrs(cfg_radius)

            else:
                # perform evolution

                # print("doing evolution")

                # step 1: evolve rules
                if i == len(population):
                    # if max number of tries reached, evolve population
                    if j == tests:
                        # reset tries
                        j = 0
                        fitness_ave = 0

                        # calculate average fitness score
                        for individual in population:
                            individual[1] /= tests
                            fitness_ave += individual[1]

                        batch_no += 1
                        best_genome = max(population, key=lambda x: x[1])
                        fitness_ave /= len(population)

                        print_info(batch_no, fitness_ave, best_genome)

                        population = evolve(population, 0.8)

                    # else continue testing    
                    else:
                        j += 1

                    i = 0
                    ruleset = population[i][0]

                # step 2: loop through rules -> save new fitness score
                else:
                    population[i][1] += time
                    if i != len(population):
                        ruleset = population[i][0]
                    i += 1

            time = 0
            observation, info = env.reset()

    # print(population)
    env.close()

def print_info(batch_no, fitness_ave, best_genome):
    print(f'batch:\t{batch_no}\t', end='')
    print(f'fitness ave:\t{fitness_ave:.2f}\t', end='')
    print(f'fitness max:\t{best_genome[1]:.2f}\t', end='')
    print(f'genome:\t{best_genome[0]}\t', end='')
    print()

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
        # print(current_values)
        current_values = new_values
    # /loop through new CA

    # print(f'new values:\t{new_values}')
    
    return new_values




def CA_majority(bitstring: str) -> bool:
    '''
        Determines action of the cart.
        Currently decides based on majority vote.

        Returns: 
            0 (left)
            1 (right)
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
def evolve(population: list, p):
    '''
        Performs evolution (tm)

        Input: 
            population: list containing population of genomes (rules)
            p: TODO
        Returns: 
            list containing new population
    '''

    population_new = []

    # print(f'old population: {population}')

    # 1. choose individuals

    chosen_ones = tournament(population, round(POPULATION * 0.5), 20)

    # 2. reproduction
    while(len(population_new) < len(population)):
        #print(f"population_new: {len(population_new)} \t population: {len(population)}")       

        # choices = random.sample(chosen_ones, 2)
        choice1 = random.choice(chosen_ones)
        choice2 = random.choice(chosen_ones)
        #print(f"choices: {choices}")
        temp = n_point_crossover(choice1[0], choice2[0], [round(len(choice1[0])/2)])
        temp = mutation(temp, 0.04)
        population_new.append([temp, 0])

    # print(f'new population:')
    # for i in population_new:
    #     print(i)

    return population_new





def truncation(population: list, n: int) -> list:
    '''
        Returns list of n best individuals
    '''
    chosen = []

    population = sorted(population, key=lambda x: x[1], reverse=1)
    
    for i in range (n):
        chosen.append(population[i])

    return chosen



def uniform(population: list, n: int) -> list:
    '''
        Returns a randomly picked individual
    '''
    
    individual = random.sample(population, n)

    return individual

def tournament(population: list, n: int, m: int) -> list:
    '''
        Returns m amount of best individuals from n size list of randomly picked individuals
    '''

    n_population = uniform(population, n)
    
    chosen_ones = truncation(n_population, m)

    return chosen_ones


def mutation(parent: str, p: int) -> str:
    '''
        Performs mutation
    '''
    
    offspring = ""

    for bit in parent:
        if random.randrange(10000)/100 <= p:
            offspring += (bit_flip(bit))
        else:
            offspring += (bit)

    return offspring

def n_point_crossover(parent1: str, parent2: str, cut_points: list) -> str:
    '''
        Performs nonvariable length crossover at specified cut points
    '''

    offspring = ""
    switch = False

    for i in range(len(parent1)):
        if i in cut_points:
            switch = not switch
        if not switch:
            offspring += parent1[i]
        else:
            offspring += parent2[i]

    # print(offspring)
    return offspring



def uniform_crossover(parent1: str, parent2: str, p: int) -> str:
    '''
        Performs a crossover with cut points placed  at each index with probability p  
    '''

    offspring1 = ""
    offspring2 = ""

    for i in range(len(parent1)):
        if random.random() < p:
            offspring1 += parent1[i]
            offspring2 += parent2[i]
        else:
            offspring1 += parent2[i]
            offspring2 += parent1[i]
    
    return offspring1, offspring2


def bit_flip(ch: str) -> str:
    bit = str(1 - int(ch))
    return bit

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




cfg_radius = 2 # neighbours = radius*2



def main():
    # cellular_automaton(gen_rrs(5), 2, "101110")
    CA_initialize(True)
    

if __name__ == "__main__":
    main()