#!/usr/bin/env python3

import random


class GA:
    '''
    Provides functions to perform evolution of genetic algorithms
    '''
    def __init__(self, model) -> None:
        self.model = model

    # MAIN FUNCTIONS

    def truncation(self, population: list, n: int) -> list:
        '''
        Returns n percent of best individuals
        '''

        chosen = []
        population = sorted(population, key=lambda x: x[1], reverse=1)
        
        for i in range (n):
            chosen.append(population[i])

        return chosen

    def uniform(self, population: list, n: int) -> list:
        '''
        Returns n percent of individuals from population
        '''
        individual = random.sample(population, n)

        return individual

    def tournament(self, population: list, n: float, m: float) -> list:
        '''
        Performs tournament selection from population.
        Population is first uniformly selected to size n.
        Truncation is then performed to size m.
        Returns truncated population.
        '''

        n_population = self.uniform(population, n)
        chosen_ones = self.truncation(n_population, m)

        return chosen_ones


    def mutation(self, parent: str, p = 0.05, lr = 0.2) -> str:
        '''
        Performs mutation.
        Input:
            p: Probability for a mutation to occur
            lr: Learning rate (only used for ANN model)
        '''

        if self.model == "ca":
            return self.mutation_ca(parent, p)
        elif self.model == "ann":
            return self.mutation_ann(parent, p, lr)

    def n_point_crossover(self, parent1, parent2, cut_points: list) -> list:
        '''
        Performs nonvariable length crossover at specified cut points
        '''
        offspring1 = []
        offspring2 = []
        switch = False

        for i in range(len(parent1)):
            if i in cut_points:
                switch = not switch
            if not switch:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            else:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])

        return [offspring1, offspring2]

    def uniform_crossover(self, parent1, parent2, p: int) -> list:
        '''
        Performs crossover with probability p for genes to be copied from the opposite parent.
        '''

        offspring1 = []
        offspring2 = []

        for i in range(len(parent1)):
            if random.random() < p:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            else:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])
        
        return [offspring1, offspring2]


    # HELPER FUNCTIONS

    def mutation_ca(self, parent: str, p: int) -> str:
        '''
        Mutation for CAs
        '''
        
        offspring = ""

        for bit in parent:
            if random.random() < p:
                offspring += (self.bit_flip(bit))
            else:
                offspring += (bit)

        return offspring

    def mutation_ann(self, genome: list, p, lr: float):
        '''
        Mutation for ANNs
        '''
        #print(genome)
        new_genome = genome
        for i in range(len(new_genome)):
            if random.random() < p:
                if random.random() < 0.5:
                    #print("MUTATING")
                    new_genome[i] += lr
                else:
                    new_genome[i] -= lr
        
        #print(new_genome)
        return new_genome



    def bit_flip(self, gene: str) -> str:
        '''
        CA helper function. Flips bit.
        '''
        gene_flipped = str(1 - int(gene))
        return gene_flipped

    def list_to_string(self, ca_list: list) -> str:
        '''
        Helper function for CAs to convert list back to string.
        '''
        ca_str = ''.join((x) for x in ca_list)
        return ca_str