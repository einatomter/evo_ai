#!/usr/bin/env python3

import gym
import csv
from datetime import datetime

from cellular_automata import CA
from ann import ANN

class Evo_AI:
    def __init__(self, model_type: str, env):
        
        # parameters                    # format: default, param info
        self.model_type = model_type    # ca, ann
        self.env = env

        # learning parameters
        self._ENABLE_SEED = False       # set specific seed
        self._SEED = 42                 # 42 seed for initial env.reset()
        self._MAX_POP = 100             # ca = 100, ann = 10, population count
        self._TESTS = 4                 # 4
        self._GEN_MAX = -1              # 100, -1 removes limit
        self.init_model(model_type)


    # MAIN FUNCTIONS

    def init_model(self, model_type):
        if model_type == "ca":
            print("--- Building CA model ---")
            self.model = CA()

        elif model_type == "ann":
            print("--- Building ANN model ---")
            self.model = ANN(random_start = True)

        else:
            print("ERROR: Unknown model, exiting...")
            exit()

    def test(self, genome, tests = 50):
        '''
        Test a specific genome.
        Genome must match model used.
        
        Input:
            genome: genome to be tested
            tests: number of test iterations
        '''
        print("Running test")

        print(f'Genome: {genome}')
        time = 0
        time_total = 0

        print("Initializing environment")
        observation, info = self.env_reset()

        print("Initialization successful. Running main loop")
        for i in range(tests):
            while True:
                # convert observations to model-specific format
                observation_formatted = self.model.format_observation(observation)
                # feed observations to model
                action = self.model.determine_action(genome, observation_formatted)

                observation, reward, terminated, truncated, info = self.env.step(action)
                time += reward

                if terminated or truncated:
                    break

            # test loop done
            print(f"Test: {i} \tTime: {time}")
            time_total += time
            time = 0
            observation, info = self.env_reset()

        # test count reached
        print(f"Average time: {time_total/tests}")
        self.env.close()        


    def learn(self):
        '''
        Learn and evolve algorithm according to model specified.

        '''

        print("Running learn")
        population = []
        time = 0
        gen = 0

        print("Initializing environment and population")
        # initialize environment
        observation, info = self.env_reset()
        # generate starting population
        population = self.model.generate_population()

        print("Initialization successful. Running main loop")
        # main loop
        while gen != self._GEN_MAX:

            fitness_ave = 0

            for individual in population:    # loop through population
                individual[1] = 0            # reset fitness score

                for _ in range(self._TESTS):     # test genome n times
                    while True:                 # keep testing until termination
                        # convert observations to model-specific format
                        observation_formatted = self.model.format_observation(observation)
                        # feed observations to model
                        action = self.model.determine_action(individual[0], observation_formatted)

                        observation, reward, terminated, truncated, info = self.env.step(action)
                        time += reward

                        if terminated or truncated:
                            break

                    # test loop done
                    individual[1] += time
                    time = 0
                    observation, info = self.env_reset()
                
                # all tests genome done
                individual[1] = individual[1] / self._TESTS  # calculate fitness score
                fitness_ave += individual[1]

            # all tests population done
            # calculate statistics
            gen += 1
            best_genome = max(population, key=lambda x: x[1])
            fitness_ave /= len(population)
            self.print_info(gen, fitness_ave, best_genome)

            # perform evolution
            population = self.model.evolve(population)

        # max generation count reached
        print("Reached generation limit, exiting...")
        self.env.close()

#     def init_file(self) -> None:
#     '''
#         Creates a log file with timestamp in its name.
#         Writes a string of some of the current parameters and a header of the 3 data points.
#         Returns str of the logfile name for plot_fitness.py
        
#     '''
#     self.fieldnames = ["generation", "average_fitness", "max_fitness"]
#     self.logfilename = "log" + str(datetime.now().strftime("%d-%m-%Y_%H_%M_%S.%f")) + ".csv"

#     with open(self.logfilename, 'w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow([f"Radius: {self._RADIUS}, Resolution: {self.resolution}, Tests: {self._TESTS}, Velocity: {self.max_velocity}, Position: {self.max_position}, Ang velocity: {self.max_ang_velocity}"])
    

    # def write_file(self, gen, ave, max, population) -> None:
    #     '''
    #         Appends a row consisting fitness data (gen#, average of gen, best of gen, fitness of all individuals).
        
    #     '''
    #     all_individuals = [ x[1] for x in population ]
    #     with open(self.logfilename, 'a', newline='') as csv_file:
    #         csv_writer = csv.writer(csv_file)
    #         csv_writer.writerow([gen]+[ave]+[max] + all_individuals)


    # HELPER FUNCTIONS

    def env_reset(self):
        '''
        Helper function. Sets seed if specified.
        '''
        if self._ENABLE_SEED:
            return self.env.reset(seed = self._SEED)
        # else
        return self.env.reset()


    def print_info(self, gen, fitness_ave, best_genome):
        '''
        Helper function. Prints learning statistics.
        '''
        print(f'gen:\t{gen}\t', end='')
        print(f'fitness ave:\t{fitness_ave:.2f}\t', end='')
        print(f'fitness max:\t{best_genome[1]}\t', end='')
        print(f'genome:\t{best_genome[0]}\t', end='')
        print()


def main():
    # cellular_automaton(gen_rrs(5), 2, "101110")
    env = gym.make("CartPole-v1")
    # ai_model = Evo_AI("ca", env)
    ai_model = Evo_AI("ca", env)
    ai_model.learn()
    # ai_model.test(genome = "11100001100010011011100010101100")
    # ai_model.test(genome = [0.03038473385456536, 0.6207902125992215, 1.4053989519326353, 2.630300372623971])

if __name__ == "__main__":
    main()