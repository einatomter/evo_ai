#!/usr/bin/env python3

import random


# for writing yaml configs
import yaml
from yaml.loader import SafeLoader

class GA:
    def __init__(self, maxpop: int) -> None:
        self._MAXPOP = maxpop

    def evolve(self, population: list):
        '''
            Performs evolution (tm)

            Input: 
                population: list containing population of genomes (rules)
                p: TODO
            Returns: 
                list containing new population
        '''

        population_new = []

        # 1. choose individuals
        chosen_ones = self.tournament(population, round(self._MAXPOP * 0.5), 20)

        # 2. reproduction
        while(len(population_new) < self._MAXPOP):   

            # choices = random.sample(chosen_ones, 2)
            choice1 = random.choice(chosen_ones)
            choice2 = random.choice(chosen_ones)
            
            temp = self.n_point_crossover(choice1[0], choice2[0], [round(len(choice1[0])/2)])
            temp[0] = self.mutation(temp[0], 0.04)
            temp[1] = self.mutation(temp[1], 0.04)
            population_new.append([temp[0], 0])
            population_new.append([temp[1], 0])

        # print(f'new population:')
        # for i in population_new:
        #     print(i)
        return population_new


    def overlapping_model(self, population: list):
        population_new = []

        # n = offspring 100, m = parents 20
        # x = n+m
        # population_new = m of x

        # 1. choose individuals
        parents = self.tournament(population, round(self._MAXPOP * 0.5), 20)

        # 2. reproduction
        while(len(population_new) < self._MAXPOP):   

            # choices = random.sample(chosen_ones, 2)
            choice1 = random.choice(parents)
            choice2 = random.choice(parents)
            
            temp = self.n_point_crossover(choice1[0], choice2[0], [round(len(choice1[0])/2)])
            temp[0] = self.mutation(temp[0], 0.04)
            temp[1] = self.mutation(temp[1], 0.04)
            population_new.append([temp[0], 0])
            population_new.append([temp[1], 0])

        # print(f'new population:')
        # for i in population_new:
        #     print(i)

        population_new.extend(parents)
        population_new = self.uniform(population_new, self._MAXPOP-1)
        population_new.append(self.truncation(population, 1)[0])

        # reset fitness score
        for individual in population_new:
            individual[1] = 0

        return population_new      

    def truncation(self, population: list, n: int) -> list:
        '''
            Returns list of n best individuals
        '''
        chosen = []
        population = sorted(population, key=lambda x: x[1], reverse=1)
        
        for i in range (n):
            chosen.append(population[i])

        return chosen


    def uniform(self, population: list, n: int) -> list:
        '''
            Returns n amount of individuals from population
        '''
        
        individual = random.sample(population, n)

        return individual


    def tournament(self, population: list, n: int, m: int) -> list:
        '''
            Returns m amount of best individuals from n size list of randomly picked individuals
        '''

        n_population = self.uniform(population, n)
        chosen_ones = self.truncation(n_population, m)

        return chosen_ones


    def mutation(self, parent: str, p: int) -> str:
        '''
            Performs mutation
        '''
        
        offspring = ""

        for bit in parent:
            if random.random() < p:
                offspring += (self.bit_flip(bit))
            else:
                offspring += (bit)

        return offspring


    def n_point_crossover(self, parent1: str, parent2: str, cut_points: list) -> str:
        '''
            Performs nonvariable length crossover at specified cut points
        '''

        offspring1 = ""
        offspring2 = ""
        switch = False

        for i in range(len(parent1)):
            if i in cut_points:
                switch = not switch
            if not switch:
                offspring1 += parent1[i]
                offspring2 += parent2[i]
            else:
                offspring1 += parent2[i]
                offspring2 += parent1[i]

        # print(offspring)
        return [offspring1, offspring2]


    def uniform_crossover(self, parent1: str, parent2: str, p: int) -> str:
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

    @staticmethod
    def bit_flip(ch: str) -> str:
        tempp = str(1 - int(ch))
        return tempp