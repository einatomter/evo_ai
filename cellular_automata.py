#!/usr/bin/env python3

import numpy as np
import random
from evo_alg import GA

class CA:
    def __init__(self):
        # Default values.
        # It is recommended to change parameters through the
        # config yaml file and load it through main.

        # Config stuff
        self._GA = GA("ca")

        # evolution parameters
        self.max_pop = 100             
        self.radius = 2                                 # 2 neighbours = radius*2
        self.uniform_val = round(self.max_pop * 0.5)    # uniform selection
        self.trunc_val = round(self.max_pop * 0.2)      # truncation selection
        self.mutation_val = 0.04                        # mutation probability
        
        # observation parameters
        self.resolution = 10                    # bitstring size for each observation
        self.space_between_observations = 2     # zeroes between each observation
        self.min_position = -2.4
        self.max_position = 2.4
        self.min_velocity = -3
        self.max_velocity = 3
        self.min_angle = -0.2095
        self.max_angle = 0.2095
        self.min_ang_velocity = -2
        self.max_ang_velocity = 2



    # MAIN FUNCTIONS

    def generate_population(self) -> list:
        '''
        Generates population.
        Returns list of individuals (genomes).
        '''

        population = []

        for _ in range(self.max_pop):
            population.append([self.gen_rrs(), 0])

        return population

    def format_observation(self, observation_raw: list) -> str:
        '''
        Converts raw observations into binary CA.
        Returns a CA.
        '''
        
        # uncomment function to be used
        # return self.observe()
        return self.observe_alternate(observation_raw)

    def determine_action(self, genome, ca) -> bool:
        '''
        Propagates the CA and runs a majority vote on the final CA.
        Returns a boolean output.
        '''

        final_ca = self.propagate(genome, self.radius, ca)
        return self.majority(final_ca)

    def evolve(self, population) -> list:
        '''
        Evolves the population.
        Returns new population after evolution.
        '''

        return self.evolve_overlap(population)

    def parse_parameters(self, params: dict):
        '''
        Parses and sets parameters.
        '''

        print("Parsing evolutionary parameters")

        try:
            self.max_pop = params["max_pop"]
            self.radius = params["radius"]
            self.uniform_val = round(params["uniform_percentage"] * self.max_pop)
            self.trunc_val = round(params["truncation_percentage"] * self.max_pop)
            self.mutation_val = params["mutation_rate"]

            # observation parameters
            params_obs = params["observation"]
            self.resolution = params_obs["resolution"]
            self.space_between_observations = params_obs["space"]
            self.min_position = params_obs["min_position"]
            self.max_position = params_obs["max_position"]
            self.min_velocity = params_obs["min_velocity"]
            self.max_velocity = params_obs["max_velocity"]
            self.min_angle = params_obs["min_angle"]
            self.max_angle = params_obs["max_angle"]
            self.min_ang_velocity = params_obs["min_ang_velocity"]
            self.max_ang_velocity = params_obs["max_ang_velocity"]

        except:
            print("Error in parsing CA parameters, reverting to default values")

    # HELPER FUNCTIONS

    def gen_rrs(self) -> str:
        ''' 
        Generates a random ruleset based on the amount of neighbours.
        Returns: random bitstring within range (str)
        '''
        subst_size = (self.radius * 2) + 1
        max_substr = 2 ** subst_size
        max_rules = (2 ** max_substr) - 1 # max 255

        rrs_dec = random.randrange(0, max_rules) # 140   10001100
        rrs_bit = format(rrs_dec, "b").zfill(max_substr)

        return rrs_bit



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
            if obs >= intervals[i] and obs < intervals[i+1]:
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



    def evolve_overlap(self, population: list) -> list:
        '''
        New evolution algorithm. 
        Parents are appended to new population, which is then uniformly 
        selected until new population matches old.

        Input: 
            old population
        Returns: 
            new population
        '''

        population_new = []

        # n = offspring 100, m = parents 20
        # x = n+m
        # population_new = uniform(x - 1) + best individual

        # 1. choose individuals
        parents = self._GA.tournament(population, self.uniform_val, self.trunc_val)

        # 2. reproduction
        while(len(population_new) < self.max_pop):

            parent1, fitness = random.choice(parents)
            parent2, fitness = random.choice(parents)

            offspring = self._GA.n_point_crossover(parent1, parent2, [round(len(parent1)/2)])
            for individual in offspring:
                individual = self._GA.list_to_string(individual)
                individual = self._GA.mutation(individual, self.mutation_val)
                population_new.append([individual, 0])

        # print(f'new population:')
        # for i in population_new:
        #     print(i)

        # add parents to population
        population_new.extend(parents)
        # uniform selection of new population until count matches old population
        population_new = self._GA.uniform(population_new, self.max_pop-1)
        # append best individual from previous generation
        population_new.append(self._GA.truncation(population, 1)[0])

        return population_new

    def evolve_no_overlap(self, population: list) -> list:
        '''
        Performs evolution (tm)

        Input: 
            old population
        Returns: 
            new population
        '''

        population_new = []

        # 1. choose individuals
        chosen_ones = self._GA.tournament(population, self.uniform_val, self.trunc_val)

        # 2. reproduction
        while(len(population_new) < self.max_pop):   

            parent1, fitness = random.choice(chosen_ones)
            parent2, fitness = random.choice(chosen_ones)
            
            offspring = self._GA.n_point_crossover(parent1, parent2, [round(len(parent1)/2)])
            for individual in offspring:
                individual = self._GA.list_to_string(individual)
                individual = self._GA.mutation(individual, 0.04)
                population_new.append([individual, 0])

        # print(f'new population:')
        # for i in population_new:
        #     print(i)
        return population_new