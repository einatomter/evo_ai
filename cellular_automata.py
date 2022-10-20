#!/usr/bin/env python3

from ctypes import sizeof
import gym
import numpy as np
import random
from progress.bar import Bar
from evo_alg import GA


# for writing yaml configs
import yaml
from yaml.loader import SafeLoader


class CA:
    def __init__(self) -> None:
        # Config stuff
        self._MAXPOP = 100                  # 100 maximum amount of rules of the first random population
        self._RADIUS = 2                    # 2 neighbours = radius*2
        self._ENABLE_THRESHOLD = False      # random search with (False) or without threshold (True)
        self._RANDOM_THRESHOLD_SIZE = 30    # threshold for genome to be accepted
        self._ENABLE_SEED = True            # set specific seed
        self._SEED = 42                     # 42 seed for initial env.reset()
        self._TESTS = 1                     # how many times to test evolved rules before evolving again

        # observation parameters
        self.resolution = 20                # bitstring size for each observation
        self.space_between_observations = 4 # zeroes between each observation
        self.min_position = -2.4
        self.max_position = 2.4
        self.min_velocity = -3
        self.max_velocity = 3
        self.min_angle = -0.2095
        self.max_angle = 0.2095
        self.min_ang_velocity = -2
        self.max_ang_velocity = 2

        # env = gym.make("CartPole-v1", render_mode="human")
        self.env = gym.make("CartPole-v1")
        if self._ENABLE_SEED:
            self.observation, info = self.env.reset(seed = self._SEED)
        else:
            self.observation, info = self.env.reset()

        self.ga_env = GA(self._MAXPOP)
        self.CA_run()


    def CA_run(self):
        population = []
        time = 0
        gen = 0

        # Random rulesets generated in a list
        if self._ENABLE_THRESHOLD:
            population = self.gen_pop_with_threshold()
        else:
            population = self.gen_pop()

        while True: # maybe need something better, some evolve threshold maybe to end the evolution cycle
            # Evolve all rulesets in the population
            population = self.ga_env.overlapping_model(population)

            # Test the whole population x (self._TESTS) amount of times
            for i in range(len(population)):
                population[i][1] = 0
                for _ in range(self._TESTS):
                    while True:
                        action = self.majority(self.propagate(population[i][0], self._RADIUS, self.observe_alternate()))
                        self.observation, reward, terminated, truncated, info = self.env.step(action)
                        time += reward

                        if terminated or truncated:
                            population[i][1] += time
                            time = 0
                            if self._ENABLE_SEED:
                                self.observation, info = self.env.reset(seed = self._SEED)
                            else:
                                self.observation, info = self.env.reset()
                            break
                        
            fitness_ave = 0
            # Sum of fitness averages of all individuals
            for guy in population:
                guy[1] /= self._TESTS
                fitness_ave += guy[1]

            # Print batch info (fitness average, fitness max, best ruleset) 
            gen += 1
            best_genome = max(population, key=lambda x: x[1])
            fitness_ave /= len(population)
            self.print_info(gen, fitness_ave, best_genome)

        #self.env.close() this thing wants to close stuff but not with WHILE TRU :D

    
    def gen_pop_with_threshold(self) -> list:
        population = []
        time = 0
        
        with Bar('Generating random population', max=self._MAXPOP, fill='#') as bar:
            while len(population) < self._MAXPOP:
                ruleset = self.gen_rrs()
                action = self.majority(self.propagate(ruleset, self._RADIUS, self.observe_alternate()))
                self.observation, reward, terminated, truncated, info = self.env.step(action)
                time += reward
                
                if terminated or truncated:
                    if time > self._RANDOM_THRESHOLD_SIZE:
                        population.append([ruleset, time])
                        bar.next()
                    time = 0
                    if self._ENABLE_SEED:
                        self.observation, info = self.env.reset(seed = self._SEED)
                    else:
                        self.observation, info = self.env.reset()

        return population


    def gen_pop(self) -> list:
        population = []
        
        for i in range(self._MAXPOP):
            population.append([self.gen_rrs(), 0])

        return population


    def observe(self) -> str:
        observation_ca = ""

        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_position = self.observation[0]
        dec_position = round(np.interp(dec_position, [self.min_position, self.max_position],
                                        [0, 2**self.resolution - 1])) # mapping to non-negative values                          
        bin_position = format(dec_position, "b")
        bin_position = bin_position.zfill(self.resolution)

        observation_ca += bin_position
        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_velocity = self.observation[1]
        dec_velocity = round(np.interp(dec_velocity, [self.min_velocity, self.max_velocity],
                                        [0, 2**self.resolution - 1])) # mapping to non-negative values
        bin_velocity = format(dec_velocity, "b")
        bin_velocity = bin_velocity.zfill(self.resolution)

        observation_ca += bin_velocity
        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_angle = self.observation[2]
        dec_angle = round(np.interp(dec_angle, [self.min_angle, self.max_angle],
                                    [0, 2**self.resolution - 1]))
        bin_angle = format(dec_angle, "b")
        bin_angle = bin_angle.zfill(self.resolution)

        observation_ca += bin_angle
        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_ang_velocity = self.observation[3]
        dec_ang_velocity = round(np.interp(dec_ang_velocity, [self.min_ang_velocity, self.max_ang_velocity],
                                    [0, 2**self.resolution - 1]))
        bin_ang_velocity = format(dec_ang_velocity, "b")
        bin_ang_velocity = bin_ang_velocity.zfill(self.resolution)
        
        observation_ca += bin_ang_velocity
        
        return observation_ca

    # alternative method for building the observation CA
    def observe_alternate(self) -> str:
        observation_ca = ""
        observation_ca += self.add_zeroes(self.space_between_observations)

        # position observation
        bin_position = self.binary_bin(self.observation[0], self.min_position, self.max_position, self.resolution)
        observation_ca += bin_position
        observation_ca += self.add_zeroes(self.space_between_observations)

        # velocity observation
        bin_velocity = self.binary_bin(self.observation[1], self.min_velocity, self.max_velocity, self.resolution)
        observation_ca += bin_velocity
        observation_ca += self.add_zeroes(self.space_between_observations)

        # angle observation
        bin_angle = self.binary_bin(self.observation[2], self.min_angle, self.max_angle, self.resolution)
        observation_ca += bin_angle
        observation_ca += self.add_zeroes(self.space_between_observations)

        # angular velocity observation
        bin_ang_velocity = self.binary_bin(self.observation[3], self.min_ang_velocity, self.max_ang_velocity, self.resolution)
        observation_ca += bin_ang_velocity
        observation_ca += self.add_zeroes(self.space_between_observations)

        return observation_ca

    def propagate(self, ruleset: str, radius: int, initial_values: str) -> str:
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
        
        # range is size of cellular automaton/initial value
        # range is how many times the CA is propagated
        for _ in range(int(CA_length)):
            new_values = ""
            # looping through CA
            for j in range(CA_length):
                substr = ""
                for cell in range(-radius, radius+1):
                    substr += current_values[(j + cell) % CA_length]
                # convert substr to decimal
                # used to find corresponding rule index
                rule_index = int(substr, 2)
                # print(rule_index)
                new_values += ruleset[rule_index]
            # /loop CA
            current_values = new_values
        # /loop propagation
        return new_values


    def majority(self, bitstring: str) -> bool:
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
    def binary_bin(x: float, min: float, max: float, resolution: int) -> str:
        '''
            Creates equally sized bins and puts x within corresponding bin.
            Bin with x equals 1, the rest of the values equal 0

            Input:
                x: value to be evaluated
                min: minimum interval value
                max: maximum interval value
                resolution: number of intervals
            Returns:
                binary string of binned result
        '''

        intervals = np.linspace(min, max+0.1*max, resolution)

        bin_x = ""
        for i in range(len(intervals)-1):
            if x >= intervals[i] and x < intervals[i+1]:
                bin_x += "1"
            else:
                bin_x += "0"

        return bin_x

    @staticmethod
    def add_zeroes(n: int) -> str:
        '''
            returns a string of n zeroes
        '''
        str_zeroes = ""
        for _ in range(n):
            str_zeroes += "0"
        return str_zeroes

    @staticmethod
    def print_info(gen, fitness_ave, best_genome):
        print(f'gen:\t{gen}\t', end='')
        print(f'fitness ave:\t{fitness_ave:.2f}\t', end='')
        print(f'fitness max:\t{best_genome[1]:.2f}\t', end='')
        print(f'genome:\t{best_genome[0]}\t', end='')
        print()
        

insaneAI = CA()