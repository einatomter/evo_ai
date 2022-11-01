import gym
import csv
from datetime import datetime

from cellular_automata import CA
# import ann

class Evo_AI:
    def __init__(self, model_type: str, env):
        
        # parameters                    # format: default, param info
        self.model_type = model_type    # either ca or ann
        self.env = env

        # learning parameters
        self.tests = 4                  # 4
        self.max_generations = -1       # 100, -1 removes limit
        self.init_model(model_type)

    def init_model(self, model_type):
        if model_type == "ca":
            print("--- Building CA model ---")
            self.model = CA(self.env)

        elif model_type == "ann":
            print("--- Building ANN model ---")

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
        observation, info = self.env.reset()

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
            observation, info = self.env.reset()

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
        observation, info = self.env.reset()
        # generate starting population
        population = self.model.generate_population()

        print("Initialization successful. Running main loop")
        # main loop
        while gen != self.max_generations:

            fitness_ave = 0

            for individual in population:    # loop through population
                individual[1] = 0            # reset fitness score

                for _ in range(self.tests):     # test genome n times
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
                    observation, info = self.env.reset()
                
                # all tests genome done
                individual[1] = individual[1] / self.tests  # calculate fitness score
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

    @staticmethod
    def print_info(gen, fitness_ave, best_genome):
        print(f'gen:\t{gen}\t', end='')
        print(f'fitness ave:\t{fitness_ave:.2f}\t', end='')
        print(f'fitness max:\t{best_genome[1]}\t', end='')
        print(f'genome:\t{best_genome[0]}\t', end='')
        print()

    # def init_file(self) -> None:

    # def write_file(self, gen, ave, max, population) -> None:

#     def write_file(self) -> str:
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
    

# def plot_data(self, gen, ave, max, population):
#     '''
#         Appends a row consisting fitness data (gen#, average of gen, best of gen, fitness of all individuals).
    
#     '''
#     all_individuals = [ x[1] for x in population ]
#     with open(self.logfilename, 'a', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow([gen]+[ave]+[max] + all_individuals)

def main():
    # cellular_automaton(gen_rrs(5), 2, "101110")
    env = gym.make("CartPole-v1")
    ai_model = Evo_AI("ca", env)
    ai_model.learn()
    # ai_model.test(genome = "11100001100010011011100010101100")

if __name__ == "__main__":
    main()