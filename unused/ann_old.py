import gym
import numpy as np
import random


# Global variables
NUM_EPISODES = 500
TESTS = 4
MAX_POP = 10
population = []

def print_info(gen, fitness_ave, best_genome):
    print(f'gen:\t{gen}\t', end='')
    print(f'fitness ave:\t{fitness_ave:.2f}\t', end='')
    print(f'fitness max:\t{best_genome[1]:.2f}\t', end='')
    print(f'genome:\t{best_genome[0]}\t', end='')
    print()


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def perceptron(input: list, weights: list) -> float:
    output = 0
    for i in range(len(input)):
        output += input[i]*weights[i]
    return output

def output(x: float) -> bool:
    if x < 0:
        return 0
    # else
    return 1


def evolve(population: list) -> list:
    population_new = []
    learning_rate = 0.2
    mutation_prob = 0.05

    parents = tournament(population, round(len(population)/2), 3)
    
    while(len(population_new) < MAX_POP):
        choice1 = random.choice(parents)
        choice2 = random.choice(parents)

        temp = crossover(choice1[0], choice2[0])

        temp[0] = mutate(temp[0], learning_rate, mutation_prob)
        temp[1] = mutate(temp[1], learning_rate, mutation_prob)
        population_new.append([temp[0], 0])
        population_new.append([temp[1], 0])

    # add parents
    population_new.extend(parents)
    population_new = uniform(population_new, MAX_POP-1)
    population_new.append(truncation(population, 1)[0])

    return population_new


def mutate(genome: list, learning_rate: float, mutation_prob):
    '''
        learning_rate: Step size when a weight mutates
        mutation_prob: Probability of a mutation to occur
    '''
    #print(genome)
    new_genome = genome
    for i in range(len(new_genome)):
        if random.random() < mutation_prob:
            if random.random() < 0.5:
                #print("MUTATING")
                new_genome[i] += learning_rate
            else:
                new_genome[i] -= learning_rate
    
    #print(new_genome)
    return new_genome
    

def crossover(parent1: list, parent2: list):
    offspring1 = []
    offspring2 = []
    switch = False

    for i in range(len(parent1)):
        if i == int(len(parent1)/2):
            switch = not switch
        if not switch:
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])
        else:
            offspring1.append(parent2[i])
            offspring2.append(parent1[i])

    return [offspring1, offspring2]


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
        Returns n amount of individuals from population
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


gen = 0
# env = gym.make("CartPole-v1", render_mode="human")
env = gym.make("CartPole-v1")
observation, info = env.reset()

# while True:
#     last_layer = perceptron(observation, [0.0, 0.0, 0.2, 0.1])
#     action = output(last_layer)
#     observation, reward, terminated, truncated, info = env.step(action)
#     # time += reward

#     if terminated or truncated:
#         # population[i][1] += time
#         # time = 0
#         observation, info = env.reset()
#         break

for i in range(MAX_POP):
   population.append([6 * np.random.random((4,)) -3, 0])

# for i in range(MAX_POP):
#     population.append([[0.0, 0.0, 0.0, 0.0], 0])




# The main program loop
for episode in range(NUM_EPISODES):

    observation, info = env.reset()
    fitness_ave = 0
    
    time = 0
    for i in range(len(population)):
        # reset fitness scores of the whole population
        population[i][1] = 0
        # all tests      
        for _ in range(TESTS):
            # test genome
            while True:
                last_layer = perceptron(observation, population[i][0])
                action = output(last_layer)
                observation, reward, terminated, truncated, info = env.step(action)
                time += reward

                if terminated or truncated:
                    population[i][1] += time
                    time = 0
                    observation, info = env.reset()
                    break
            # /current test
        # /all tests
        population[i][1] /= TESTS
        fitness_ave += population[i][1]
    # /test whole population

    # Print generation info (fitness average, fitness max, best ruleset) 
    gen += 1
    best_genome = max(population, key=lambda x: x[1])
    fitness_ave /= len(population)
    print_info(gen, fitness_ave, best_genome)

    population = evolve(population)