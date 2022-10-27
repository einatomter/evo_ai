import gym
import numpy as np

class NNLayer:
    def __init__(self, input_size, output_size):
        self.input = input_size
        self.output = output_size
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    def forward(self, input):
        self.input = input
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output