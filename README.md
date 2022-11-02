# Evolutionary AI project

School project for Oslomet ACIT4610.

This repository contains code for solving the OpenAI Gym cartpole problem.
This has been done using evolutionary algorithms. One model uses cellular automata (CA) while the other uses an artificial neural netowork (ANN). Both of these have been evolved strictly using genetic algorithms (GA).

Tested on Windows 10/11 using python 3.9.12 and on Ubuntu 20.04 using python 3.8.10.

## Links to libraries:

Gym: https://github.com/openai/gym

Cartpole description: https://www.gymlibrary.dev/environments/classic_control/cart_pole/


## 1. Prerequisites

The python libraries can be installed by running the requirements.txt file.

`pip install -r requirements.txt`

## 2. Using the program

The format for running the program is as follows.

`python main.py <model> <operation> [OPTIONAL: path_to_config.yaml]`

The required parameters can take the following values:
 - model: ca, ann
 - operation: test, learn

The final parameter is not required for learning but is however mandatory for running tests.

The following commands can be run directly. NOTE: Only run one of them at a time:
```
python main.py ca test config_ca.yaml
python main.py ca learn config_ca.yaml

python main.py ann test config_ann.yaml
python main.py ann learn config_ann.yaml
```

Running learn also produces a csv logfile of the program's progress. The data can be viewed in real time or after learning has finished using plot fitness.py
```
python plot_fitness.py <path_to_logfile.csv>
```


## 3. Parameters

The parameters can be changed directly within the code. We do however recommend changing the yaml files instead, or alternatively make a completely new yaml file. All of the necessary parameters can be found within the sample configurations.