import gym
import sys
from cellular_automata import CA



if len(sys.argv) > 1:
    env = gym.make("CartPole-v1", render_mode="human")
    ca = CA(env, sys.argv[1])
    ca.CA_play()
else:
    env = gym.make("CartPole-v1")
    ca = CA(env)
    ca.CA_run()





