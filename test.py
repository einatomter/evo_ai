test_list = [['a', 7],
             ['b', 1],
             ['c', 8],
             ['d', 4],
             ['e', 5],
             ['f', 3],
             ['g', 2],
             ['h', 10],
            ]

def bit_flip(ch):
    bit = str(1 - int(ch))
    return bit


def truncation(population: list, n: int) -> list:
    '''
        Returns list of best individuals
    '''
    
    chosen = []

    population = sorted(population, key=lambda x: x[1], reverse=1)
    for i in range (n):
        
        chosen.append(population[i])

    return chosen



def n_point_crossover(parent1: str, parent2: str, cut_points: list) -> str:
    '''
        Performs nonvariable length crossover at cut points
    '''
    offspring = ""
    start_point = 0

    for i in range(len(cut_points)):
        if i % 2 == 0:
            offspring += parent1[start_point:cut_points[i]]
        else:
            offspring += parent2[start_point:cut_points[i]]

        start_point = cut_points[i]

    print(offspring)
    return offspring

def n_point_crossover2(parent1: str, parent2: str, cut_points: list) -> str:
    '''
        Performs nonvariable length crossover at cut points
    '''
    offspring = ""
    start_point = 0
    switch = False

    for i in range(len(parent1)):
        if i in cut_points:
            switch = not switch
        if not switch:
            offspring += parent1[i]
        else:
            offspring += parent2[i]

    print(offspring)
    return offspring



result = truncation(test_list, 2)

print(result)

print(bit_flip("1"))
print(type(bit_flip("0")))

print(n_point_crossover2("1234", "00006", [2, 3]))