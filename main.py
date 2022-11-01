#!/usr/bin/env python3

import sys
from evo_ai import Evo_AI

def arg_format():
    print("Format: python main.py <model> <operation> [OPTIONAL: path_to_config.yaml]")
    print("<model>: ca, ann")
    print("<operation>: learn, test")

def main():
    if len(sys.argv) > 2:
        print(sys.argv)
        algorithm = Evo_AI(sys.argv[1])
        if len(sys.argv) > 3:
            algorithm.parse_yaml(sys.argv[3])
        if sys.argv[2] == "learn":
            algorithm.learn()
        elif sys.argv[2] == "test":
            algorithm.test()

    else:
        print("Missing parameters.")
        arg_format()

if __name__ == "__main__":
    main()