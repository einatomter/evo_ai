#!/usr/bin/env python3

import csv
import numpy as np
import random

from evo_alg import GA

class ANN:
    def __init__(self):
        # Default values.
        # It is recommended to change parameters through the
        # config yaml file and load it through main.

        # Config stuff
        self._GA = GA("ann")

        # evolution parameters
        self.random_start = False                       # boolean
        self.rand_range = 3                             # range of values if random start is enabled
        self.max_pop = 10
        self.uniform_val = round(self.max_pop * 0.5)    # percentage of uniform selection
        self.trunc_val = round(self.max_pop * 0.2)      # percentage of truncation selection
        self.mutation_val = 0.04                        # mutation rate
        self.learning_rate = 0.2                        # learning rate



    # MAIN FUNCTIONS

    def generate_population(self) -> list:
        '''
        Generates population.
        Returns list of individuals (genomes).
        '''

        population = []

        for _ in range(self.max_pop):
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

    def determine_action(self, genome: list, observation: list) -> bool:
        '''
        Feeds observation as input to the ANN.
        Last layer has a binary step function.
        Returns a boolean output.
        '''

        last_layer = self._weighted_sum(genome, observation)
        return self._binary_step(last_layer)

    def evolve(self, population: list) -> list:
        '''
        Performs evolution. Uses same evolution process as CA evolve_overlap.
        Parents are appended to new population, which is then uniformly 
        selected until new population matches old.        
        '''

        population_new = []

        parents = self._GA.tournament(population, self.uniform_val, self.trunc_val)
        
        while(len(population_new) < self.max_pop):
            parent1, fitness = random.choice(parents)
            parent2, fitness = random.choice(parents)

            offspring = self._GA.n_point_crossover(parent1, parent2, [round(len(parent1)/2)])
            for individual in offspring:
                individual = self._GA.mutation(individual, self.mutation_val, self.learning_rate)
                population_new.append([individual, 0])

        # add parents
        population_new.extend(parents)
        population_new = self._GA.uniform(population_new, self.max_pop-1)
        population_new.append(self._GA.truncation(population, 1)[0])

        return population_new

    def parse_parameters(self, params: dict) -> None:
        '''
        Parses and sets parameters.
        '''

        print("Parsing evolutionary parameters")

        try:
            self.max_pop = params["max_pop"]
            self.random_start = params["random_start"]
            self.rand_range = params["random_range"]
            self.uniform_val = round(params["uniform_percentage"] * self.max_pop)
            self.trunc_val = round(params["truncation_percentage"] * self.max_pop)
            self.mutation_val = params["mutation_rate"]
            self.learning_rate = params["learning_rate"]

        except:
            print("Error in parsing ANN parameters, reverting to default values")

    def write_model_params(self, file_path):

        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([f"Random start: {self.random_start}, "
                                 f"Random range: {self.rand_range}, "
                                 f"Learning rate: {self.learning_rate}"])

    # HELPER FUNCTIONS

    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + np.exp(-x))

    def _weighted_sum(self, weights: list, input: list) -> float:
        '''
        Calculate weighted sum of input
        '''
        sum = 0
        for i in range(len(input)):
            sum += input[i]*weights[i]
        return sum

    def _binary_step(self, x: float) -> bool:
        if x < 0:
            return 0
        # else
        return 1
