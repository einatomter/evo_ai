#!/usr/bin/env python3

import gym
import numpy as np
from evo_ai import *

cfg_radius = 1 # neighbours = radius/2

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)

# TODO: separate initialize function?

#action = 1 we shouldn't pass this as the first step, right?
time = 0
dec_angle = 0
ruleset = gen_rrs(cfg_radius)

print(f'ruleset:\t{ruleset}')

for _ in range(1000):
    # action = env.action_space.sample()
    
    dec_angle = observation[2]
    bin_angle = format(24 + round(dec_angle * 180/np.pi), "b") # negative angles are 0-23, positive angles are 24-48
    bin_angle = bin_angle.zfill(6)
    
    action = ca_output(cellular_automaton(ruleset, cfg_radius, bin_angle))
    
    observation, reward, terminated, truncated, info = env.step(action)
    
    # print(observation)
    # print(reward)

    time += reward
    
    if terminated or truncated:
        if time > 30:
            print(f'ruleset:\t{ruleset}')
            print(f'time: {time}')
            
        ruleset = gen_rrs(cfg_radius)
        time = 0
        observation, info = env.reset()
env.close()