#!/usr/bin/env python3

import gym
import sys
import subprocess
from cellular_automata import CA

if len(sys.argv) > 1:
    input = sys.argv[1]
    env = gym.make("CartPole-v1", render_mode="human")
    ca = CA(env, input)
    ca.CA_play(input)
else:
    env = gym.make("CartPole-v1")
    ca = CA(env)
    subprocess.Popen(['python', 'plot_fitness.py', ca.write_file()])
    ca.CA_run()