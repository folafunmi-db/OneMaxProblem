# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 08:10:10 2020

@author: PC
"""
# =============================================================================
# An example of a Genetic Algorithm
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

    #Initialize structures
    #InitRepeat takes 3 arguments: a container class, a function to fill the container
    #and the number of times we want the function to repeat itself
    toolbox.register("individual", tools.initRepeat, creator.Individual,\
        toolbox.attr_bool, num_bits)

    #Define a population to be a list of individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    #Register Genetic Operators
    #Register the evaluation operator
    toolbox.register("evaluate", eval_func)

    #Register the crossover opertor
    toolbox.register("mate", tools.cxTwoPoint)

    #Register the mutation opertor
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

    #Register the operator for selecting individuals for breeding
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox

#This will run when the python file is executed
if __name__ == "__main__":
    #Define the number of bits
    num_bits = 75

    #Create a toolbos using the parameter above
    toolbox = create_toolbox(num_bits)

    #Seed the random number generator so as to get repeatable results
    random.seed(7)

    #Create an initial population of 500 individuals
    population = toolbox.population(n=500)

    #Define the probabilities of crossing and mutating
    probab_crossing, probab_mutating = 0.5, 0.2

    #Define the number of generations to iterate through
    num_generations = 60

    print('\nStarting the evolution process')
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    #Iterating through the generations
    print('\nEvaluated', len(population), 'individuals')
    for g in range(num_generations):
        print("\n======= Generation", g)

        #Select the next generation of individuals
        offspring = toolbox.select(population,len(population))

        #Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        #Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            #Cross two individuals
            if random.random() < probab_crossing:
                toolbox.mate(child1, child2)

                #Remove the fitness values
                del child1.fitness.values
                del child2.fitness.values
            
        #Apply mutation on the offspring
        for mutant in offspring:
            #Mutate an individual
            if random.random() < probab_mutating:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        #Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print("Evaluated", len(invalid_ind), "individuals")

        #The population is entirely replaced with the offspring
        population[:] = offspring

        #Gather all the fitnesses in one list and print the stats of the current generation
        fits = [ind.fitness.values[0] for ind in population]

        length = len(population)
        mean = sum(fits)/length
        sum2 = sum(X*X for x in fits)
        std = abs(sum2/length - mean**2)**0.5

        print('Min =', min(fits), ', Max =', max(fits))
        print('Average =', round(mean, 2), ', Standard Dev =', round(std, 2))

    print("\n==== End of evolution")

    #Print the final output
    best_ind = tools.selBest(population, 1)[0]
    print('\nBest individual: \n', best_ind)
    print('\nNumber of ones:', sum(best_ind))