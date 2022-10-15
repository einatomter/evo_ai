#!/usr/bin/env python3

from ctypes import sizeof
import gym
import numpy as np
import pandas as pd
import random
from evo_alg import GA


# for writing yaml configs
import yaml
from yaml.loader import SafeLoader


class CA:
    def __init__(self, maxpop: int, seed: int, radius: int) -> None:

        # Config stuff
        self._MAXPOP = maxpop #100 maximum amount of rules of the first random population
        self._SEED = seed #42 seed for initial env.reset()
        self._RADIUS = radius #2  neighbours = radius*2
        self._TESTS = 4 # how many times to test evolved rules before evolving again
        self._RANDOM_THRESHOLD = True # random search with (False) or without threshold (True)

        # env = gym.make("CartPole-v1", render_mode="human")
        self.env = gym.make("CartPole-v1")
        self.observation, info = self.env.reset()

        self.ga_env = GA(self._MAXPOP)

        self.CA_initialize(self._RANDOM_THRESHOLD)


    def CA_initialize(self, generate_random: bool = False): #or CA_run?

        population = []
        time = 0
        batch_no = 0

        # Random rulesets generated in a list
        if generate_random:
            population = self.gen_pop()
        else:
            population = self.gen_pop_with_threshold(50)

        while True: # maybe need something better, some evolve threshold maybe
            
            # Evolve all rulesets in the population
            population = self.ga_env.evolve(population, 0.8)

            # Test the whole population x amount of times
            for _ in range(self._TESTS):
                for i in range(len(population)):
                    while True:
                        action = self.CA_majority(self.CA_propagate(population[i][0], self._RADIUS, self.observe()))
                        self.observation, reward, terminated, truncated, info = self.env.step(action)
                        time += reward

                        if terminated or truncated:
                            population[i][1] += time
                            time = 0
                            self.observation, info = self.env.reset()
                            break
                
            
            fitness_ave = 0
            # Sum of fitness averages of all individuals
            for guy in population:
                guy[1] /= self._TESTS
                fitness_ave += guy[1]

            # Print batch info (fitness average, fitness max, best ruleset) 
            batch_no += 1
            best_genome = max(population, key=lambda x: x[1])
            fitness_ave /= len(population)
            self.print_info(batch_no, fitness_ave, best_genome)

        self.env.close() #this thing wants to close stuff but not with our WHILE TRU :D

    def observe(self) -> str:
        
        min_position = -4.8
        max_position = 4.8
        min_velocity = -4
        max_velocity = 4
        min_angle = -0.42
        max_angle = 0.42
        min_ang_velocity = -4
        max_ang_velocity = 4
        resolution = 20
        space_between_observations = 2

        #might change all this to a for-loop
        observation_ca = "00"

        
        dec_position = self.observation[0]
        dec_position = round(np.interp(dec_position, [min_position, max_position],
                                        [0, 2**resolution - 1])) # mapping to non-negative values                          
        bin_position = format(dec_position, "b")
        bin_position = bin_position.zfill(resolution)

        observation_ca += bin_position
        for _ in range(space_between_observations):
            observation_ca += "0"

        dec_velocity = self.observation[1]
        dec_velocity = round(np.interp(dec_velocity, [min_velocity, max_velocity],
                                        [0, 2**resolution - 1])) # mapping to non-negative values
        bin_velocity = format(dec_velocity, "b")
        bin_velocity = bin_velocity.zfill(resolution)

        observation_ca += bin_velocity
        for _ in range(space_between_observations):
            observation_ca += "0"

        dec_angle = self.observation[2]
        dec_angle = round(np.interp(dec_angle, [min_angle, max_angle],
                                    [0, 2**resolution - 1]))
        bin_angle = format(dec_angle, "b")
        bin_angle = bin_angle.zfill(resolution)

        observation_ca += bin_angle
        for _ in range(space_between_observations):
            observation_ca += "0"

        dec_ang_velocity = self.observation[3]
        dec_ang_velocity = round(np.interp(dec_ang_velocity, [min_ang_velocity, max_ang_velocity],
                                    [0, 2**resolution - 1]))
        bin_ang_velocity = format(dec_ang_velocity, "b")
        bin_ang_velocity = bin_ang_velocity.zfill(resolution)
        
        observation_ca += bin_ang_velocity
        return observation_ca


    def gen_pop_with_threshold(self, threshold: int) -> list:
        population = []
        time = 0
        
        while len(population) < self._MAXPOP:
            
            ruleset = self.gen_rrs()
            action = self.CA_majority(self.CA_propagate(ruleset, self._RADIUS, self.observe()))
            self.observation, reward, terminated, truncated, info = self.env.step(action)
            time += reward
            
            if terminated or truncated:
                if time > threshold:
                    population.append([ruleset, time])
                
                time = 0
                self.observation, info = self.env.reset()

        return population


    def gen_pop(self) -> list:
        population = []
        
        for i in range(self._MAXPOP):
                population.append([self.gen_rrs(), 0])

        return population


    def CA_propagate(self, ruleset: str, radius: int, initial_values: str) -> str:
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


    def CA_majority(self, bitstring: str) -> bool:
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


    def gen_rrs(self) -> str:
        ''' 
            Generates a random ruleset based on the amount of neighbours.
            
            Returns: random bitsting within range (str)
        '''
        subst_size = (self._RADIUS * 2) + 1
        max_substr = 2 ** subst_size
        max_rules = (2 ** max_substr) - 1 # max 255
        
        rrs_dec = random.randrange(0, max_rules) # 140   10001100
        rrs_bit = format(rrs_dec, "b").zfill(max_substr)

        return rrs_bit

    @staticmethod
    def print_info(batch_no, fitness_ave, best_genome):
        print(f'batch:\t{batch_no}\t', end='')
        print(f'fitness ave:\t{fitness_ave:.2f}\t', end='')
        print(f'fitness max:\t{best_genome[1]:.2f}\t', end='')
        print(f'genome:\t{best_genome[0]}\t', end='')
        print()
        

insaneAI = CA(100, 42, 2)