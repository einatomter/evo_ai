#!/usr/bin/env python3

import numpy as np
import random
from progress.bar import Bar
from evo_alg import GA
import csv
from datetime import datetime

# for writing yaml configs
import yaml
from yaml.loader import SafeLoader


class CA:
    def __init__(self, env) -> None:
        # Config stuff
        self._MAXPOP = 100                  # 100 maximum amount of rules of the first random population
        self._RADIUS = 2                    # 2 neighbours = radius*2
        self._ENABLE_THRESHOLD = False      # random search with (False) or without threshold (True)
        self._RANDOM_THRESHOLD_SIZE = 30    # threshold for genome to be accepted
        self._ENABLE_SEED = False            # set specific seed
        self._SEED = 42                     # 42 seed for initial env.reset()
        self._TESTS = 4                     # how many times to test evolved rules before evolving again
        
        # observation parameters
        self.resolution = 10                # bitstring size for each observation
        self.space_between_observations = 2 # zeroes between each observation
        self.min_position = -2.4
        self.max_position = 2.4
        self.min_velocity = -3
        self.max_velocity = 3
        self.min_angle = -0.2095
        self.max_angle = 0.2095
        self.min_ang_velocity = -2
        self.max_ang_velocity = 2

        self.ga_env = GA(self._MAXPOP)

    # POPULATION GENERATION

    def generate_population(self) -> list:
        '''
        Generates population.
        Returns list of individuals (genomes).
        '''

        return self.gen_pop()

    def gen_pop(self) -> list:
        population = []

        for _ in range(self._MAXPOP):
            population.append([self.gen_rrs(), 0])

        return population

    def gen_rrs(self) -> str:
        ''' 
            Generates a random ruleset based on the amount of neighbours.

            Returns: random bitstring within range (str)
        '''
        subst_size = (self._RADIUS * 2) + 1
        max_substr = 2 ** subst_size
        max_rules = (2 ** max_substr) - 1 # max 255

        rrs_dec = random.randrange(0, max_rules) # 140   10001100
        rrs_bit = format(rrs_dec, "b").zfill(max_substr)

        return rrs_bit


    # OBSERVATION FORMATTING

    def format_observation(self, observation_raw: list) -> str:
        '''
        Converts raw observations into binary CA.
        Returns a CA.
        '''
        
        # uncomment function to be used
        # return self.observe()
        return self.observe_alternate(observation_raw)

    def observe(self, observation_raw) -> str:
        '''
        Maps observations directly to binary according to each state's min/max values.
        Size of the binary string is equal to resolution set.
        Returns a CA of observations.
        '''
        observation_ca = ""

        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_position = observation_raw[0]
        dec_position = round(np.interp(dec_position, [self.min_position, self.max_position],
                                        [0, 2**self.resolution - 1])) # mapping to non-negative values                          
        bin_position = format(dec_position, "b")
        bin_position = bin_position.zfill(self.resolution)

        observation_ca += bin_position
        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_velocity = observation_raw[1]
        dec_velocity = round(np.interp(dec_velocity, [self.min_velocity, self.max_velocity],
                                        [0, 2**self.resolution - 1])) # mapping to non-negative values
        bin_velocity = format(dec_velocity, "b")
        bin_velocity = bin_velocity.zfill(self.resolution)

        observation_ca += bin_velocity
        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_angle = observation_raw[2]
        dec_angle = round(np.interp(dec_angle, [self.min_angle, self.max_angle],
                                    [0, 2**self.resolution - 1]))
        bin_angle = format(dec_angle, "b")
        bin_angle = bin_angle.zfill(self.resolution)

        observation_ca += bin_angle
        observation_ca += self.add_zeroes(self.space_between_observations)

        dec_ang_velocity = observation_raw[3]
        dec_ang_velocity = round(np.interp(dec_ang_velocity, [self.min_ang_velocity, self.max_ang_velocity],
                                    [0, 2**self.resolution - 1]))
        bin_ang_velocity = format(dec_ang_velocity, "b")
        bin_ang_velocity = bin_ang_velocity.zfill(self.resolution)
        
        observation_ca += bin_ang_velocity
        
        return observation_ca

    def observe_alternate(self, observation: list) -> str:
        '''
        Creates a number of intervals equal to resolution set.
        Observation sets the interval it is in equal to 1, the rest equal to 0.
        Entire interval range spans each state's min/max values.
        Returns a CA of observations.
        '''
        observation_ca = ""
        observation_ca += self.add_zeroes(self.space_between_observations)

        # position observation
        bin_position = self.binary_bin(observation[0], self.min_position, self.max_position, self.resolution)
        observation_ca += bin_position
        observation_ca += self.add_zeroes(self.space_between_observations)

        # velocity observation
        bin_velocity = self.binary_bin(observation[1], self.min_velocity, self.max_velocity, self.resolution)
        observation_ca += bin_velocity
        observation_ca += self.add_zeroes(self.space_between_observations)

        # angle observation
        bin_angle = self.binary_bin(observation[2], self.min_angle, self.max_angle, self.resolution)
        observation_ca += bin_angle
        observation_ca += self.add_zeroes(self.space_between_observations)

        # angular velocity observation
        bin_ang_velocity = self.binary_bin(observation[3], self.min_ang_velocity, self.max_ang_velocity, self.resolution)
        observation_ca += bin_ang_velocity
        observation_ca += self.add_zeroes(self.space_between_observations)

        return observation_ca

    def binary_bin(self, obs: float, min: float, max: float, resolution: int) -> str:
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

        bin_obs = ""
        for i in range(len(intervals)-1):
            if obs >= intervals[i] and x < intervals[i+1]:
                bin_obs += "1"
            else:
                bin_obs += "0"

        return bin_obs

    def add_zeroes(self, n: int) -> str:
        '''
            Returns a string of n zeroes
        '''
        str_zeroes = ""
        for _ in range(n):
            str_zeroes += "0"
        return str_zeroes


    # DETERMINING OUTPUT

    def determine_action(self, genome, ca) -> bool:
        '''
        Propagates the CA and runs a majority vote on the final CA.
        Returns a boolean output.
        '''

        final_ca = self.propagate(genome, self._RADIUS, ca)
        return self.majority(final_ca)

    def propagate(self, ruleset: str, radius: int, initial_CA: str) -> str:
        '''
            Propagates the CA a number of times equal to its length.

            Input:
                ruleset: state transition function
                initial_CA: initial state of CA
            Returns: 
                final state of the CA
        '''

        # variable declaration
        CA_length = len(initial_CA)
        current_CA = initial_CA
        
        # range is size of cellular automaton/initial value
        # range is how many times the CA is propagated
        for _ in range(int(CA_length)):
            new_CA = ""
            # looping through CA
            for j in range(CA_length):
                substr = ""
                for cell in range(-radius, radius+1):
                    substr += current_CA[(j + cell) % CA_length]
                # convert substr to decimal
                # used to find corresponding rule index
                rule_index = int(substr, 2)
                # print(rule_index)
                new_CA += ruleset[rule_index]
            # /loop CA
            current_CA = new_CA
        # /loop propagation
        return new_CA

    def majority(self, bitstring: str) -> bool:
        '''
            Determines action of the cart.
            Output is boolean
        '''

        ones = bitstring.count('1')
        zeros = bitstring.count('0')

        if ones >= zeros:
            return 1
        else:
            return 0


    # EVOLUTION

    def evolve(self, population) -> list:
        '''
        Evolves the population.
        Returns new population after evolution.
        '''
        return self.ga_env.overlapping_model(population)