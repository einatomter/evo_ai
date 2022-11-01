#!/usr/bin/env python3

import gym
import csv
from datetime import datetime

import yaml
from yaml.loader import SafeLoader

from cellular_automata import CA
from ann import ANN

class Evo_AI:
    def __init__(self, model_type: str):
        # Default values.
        # It is recommended to change parameters through the
        # config yaml file and load it through main.
        
        # general parameters            # format: default, param info
        self.enable_render = False
        self.model_type = model_type    # ca, ann

        # testing parameters
        self.genome = None
        self.iterations = 50

        # learning parameters
        self._ENABLE_SEED = False       # set specific seed
        self._SEED = 42                 # 42 seed for initial env.reset()
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
            self.model = ANN()

        else:
            print("ERROR: Unknown model, exiting...")
            exit()

    def test(self):
        '''
        Test a specific genome.
        Genome must match model used.
        '''
        print("Running test")

        print(f'Genome: {self.genome}')
        print(f'Iterations: {self.iterations}')
        time = 0
        time_total = 0

        print("Initializing environment")
        self.env_init()
        observation, info = self.env_reset()

        print("Initialization successful. Running main loop")
        for i in range(self.iterations):
            while True:
                # convert observations to model-specific format
                observation_formatted = self.model.format_observation(observation)
                # feed observations to model
                action = self.model.determine_action(self.genome, observation_formatted)

                observation, reward, terminated, truncated, info = self.env.step(action)
                time += reward

                if terminated or truncated:
                    break

            # test loop done
            print(f"Test: {i+1} \tTime: {time}")
            time_total += time
            time = 0
            observation, info = self.env_reset()

        # test count reached
        print(f"Average time: {time_total/self.iterations}")
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
        self.env_init()
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


    def parse_yaml(self, file_path: str):
        '''
        Parse yaml file containing parameters.
        '''

        print(f"Parsing yaml file: {file_path}")
        with open(file_path) as f:
            data = yaml.load(f, Loader = SafeLoader)

                    # set rendering
            try:
                self.enable_render = data["enable_render"]
            except:
                pass

            params_test = data["test"]
            params_learn = data["learn"]
            params_evo = data["evolution"]

            self.parse_parameters(params_test, params_learn)
            self.model.parse_parameters(params_evo)

    def parse_parameters(self, params_test: dict, params_learn: dict):
        '''
        Parses parameters and sets respective values
        '''

        # set test parameters
        try:
            self.genome = params_test["genome"]
            self.iterations = params_test["iterations"]
        except:
            print("No test parameters found")

        # set learn parameters
        try:
            self._ENABLE_SEED = params_learn["enable_seed"]
            self._SEED = params_learn["seed"]
            self._TESTS = params_learn["tests"]
            self._GEN_MAX = params_learn["gen_max"]
        except:
            print("No learning parameters found")


    # HELPER FUNCTIONS

    def env_init(self):
        if self.enable_render:
            self.env = gym.make("CartPole-v1", render_mode = "human")
        else:
            self.env = gym.make("CartPole-v1")

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
    env = gym.make("CartPole-v1")
    # ai_model = Evo_AI("ca", env)
    algorithm = Evo_AI("ca", env)
    algorithm.parse_yaml("config_ca.yaml")
    # ai_model.learn()
    # ai_model.test()
    algorithm.test()

if __name__ == "__main__":
    main()