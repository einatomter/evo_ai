#!/usr/bin/env python3

import numpy as np
import random
from evo_alg import GA

class ANN:
    def __init__(self, max_pop = 10, random_start = True):
        # Config stuff
        self._MAXPOP = max_pop
        self._GA = GA("ann")

        self.random_start = random_start    # boolean
        self.rand_range = 3                 # range of values if random start is enabled

        # evolution parameters
        self.uniform_val = round(self._MAXPOP * 0.5)    # percentage of uniform selection
        self.trunc_val = round(self._MAXPOP * 0.2)      # percentage of truncation selection
        self.p = 0.04                                   # mutation probability
        self.lr = 0.2                                   # learning rate



    # MAIN FUNCTIONS

    def generate_population(self) -> list:
        '''
        Generates population.
        Returns list of individuals (genomes).
        '''

        population = []

        for _ in range(self._MAXPOP):
            if self.random_start:
                population.append([self.rand_range * 2 * np.random.random((4,)) -self.rand_range, 0])
            else:
                population.append([[0.0, 0.0, 0.0, 0.0], 0])

        return population

    def format_observation(self, observation_raw: list) -> list:
        '''
        Formats observation.
        For ANN model, no additional formatting is currently done.
        Returns list of observations.
        '''
        return observation_raw

    def determine_action(self, genome, observation):
        '''
        Feeds observation as input to the ANN.
        Last layer has a binary step function.
        Returns a boolean output.
        '''

        last_layer = self.weighted_sum(genome, observation)
        return self.binary_step(last_layer)

    def evolve(self, population: list) -> list:
        '''
        Performs evolution. Uses same evolution process as CA evolve_overlap.
        Parents are appended to new population, which is then uniformly 
        selected until new population matches old.        
        '''

        population_new = []

        parents = self._GA.tournament(population, self.uniform_val, self.trunc_val)
        
        while(len(population_new) < self._MAXPOP):
            parent1, fitness = random.choice(parents)
            parent2, fitness = random.choice(parents)

            offspring = self._GA.n_point_crossover(parent1, parent2, [round(len(parent1)/2)])
            for individual in offspring:
                individual = self._GA.mutation(individual, self.p, self.lr)
                population_new.append([individual, 0])

        # add parents
        population_new.extend(parents)
        population_new = self._GA.uniform(population_new, self._MAXPOP-1)
        population_new.append(self._GA.truncation(population, 1)[0])

        return population_new



    # HELPER FUNCTIONS

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def weighted_sum(self, weights: list, input: list) -> float:
        '''
        Calculate weighted sum of input
        '''
        sum = 0
        for i in range(len(input)):
            sum += input[i]*weights[i]
        return sum

    def binary_step(self, x: float) -> bool:
        if x < 0:
            return 0
        # else
        return 1
