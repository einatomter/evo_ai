#!/usr/bin/env python3

import gym
import numpy as np
from evo_ai import *

cfg_radius = 1 # neighbours = radius/2

# first initialization
env = gym.make("CartPole-v1", render_mode="human")
#env = gym.make("CartPole-v1")

observation, info = env.reset(seed=42)
#action = 1 we shouldn't pass this as the first step, right? I just put env.step() bit lower when an action has been found by CA
time = 0
dec_angle = 0
ruleset = gen_rrs(cfg_radius)

print(f'ruleset:\t{ruleset}')

for _ in range(1000):
    # action = env.action_space.sample()
    
    dec_angle = observation[2]
    bin_angle = format(24 + round(dec_angle * 180/np.pi), "b") # negative angles are 0-23, positive angles are 24-48
    bin_angle = bin_angle.zfill(6)
    
    action = CA_majority(CA_propagate(ruleset, cfg_radius, bin_angle))
    observation, reward, terminated, truncated, info = env.step(action)
    time += reward
    
    # print(observation)
    # print(reward)
    
    if terminated:
        if time > 30:
            print(f'ruleset:\t{ruleset}')
            print(f'time: {time}')
            fitness_track(ruleset, time)
            
        ruleset = gen_rrs(cfg_radius)
        time = 0
        observation, info = env.reset()

print_fitness()
env.close()