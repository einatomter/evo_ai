#!/usr/bin/env python3

import gym
import numpy as np
from time import sleep

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)

angle = 0
action = 1

for _ in range(1000):
    # action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    
    angle = observation[2]
    # if angle < 0:
    #     action = 0
    # else:
    #     action = 1

    # print(observation)
    # print(reward)

    # convert observation states to binary forms with resolution n
    # print(24 + round(angle * 180/np.pi))

    # offset starts from min observable angle (-24)
    bin_angle = format(24 + round(angle * 180/np.pi), "b")

    bin_angle = bin_angle.zfill(6)
    
    print(bin_angle)
    
    if terminated or truncated:
        observation, info = env.reset()
env.close()