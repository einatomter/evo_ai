#!/usr/bin/env python3

import gym
import numpy as np
from evo_ai import *

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)

angle = 0
action = 1

time = 0

ruleset = generate_rrs(3)
print(f'ruleset:\t{ruleset}')

for _ in range(1000):
    # action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    
    angle = observation[2]

    bin_angle = format(24 + round(angle * 180/np.pi), "b")

    bin_angle = bin_angle.zfill(6)

    action = ca_output(cellular_automaton(ruleset, bin_angle))

    # print(observation)
    # print(reward)

    time += reward
    
    if terminated or truncated:
        if time > 30:
            print(f'ruleset:\t{ruleset}')
            print(f'time: {time}')
            
        ruleset = generate_rrs(3)
        
        time = 0
        observation, info = env.reset()
env.close()