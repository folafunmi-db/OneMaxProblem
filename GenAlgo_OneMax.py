# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 08:10:10 2020

@author: PC
"""
# =============================================================================
# Genetic Algorithm
# Solving the One Max Problem
# The One Max problem is about generating a bit string that 
# contains the maximum number of ones.
# =============================================================================

import random

from deap import base, creator, tools

#Evaluation function
def eval_func(individual):
    target_sum = 45
    return len(individual) - abs(sum(individual) - target_sum)

#Create the toolbox with the right parameters
#Such that the fitness function can keep track of the individuals
def create_toolbox(num_bits):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
# Initialize the toolbox
# Toolbox is used to store various functions
toolbox = base.Toolbox()

#To register various functions to to this toolbox
#Generate random attributes
toolbox.register('attr_bool', random.randint, 0, 1)