import random
import helpers.math as hmath


def random_mutation(population, mutation_rate, value_range):
    mutate_percentage = mutation_rate * 100
    for individual in range(len(population)):
        for gene in range(len(population[individual])):
            mutate = random.randint(1, 100) < mutate_percentage
            if mutate:
                population[individual][gene] = hmath.lin_map(random.random(), 0, 1, value_range[0], value_range[1])
    return population


def scaled_mutation(population, mutation_rate, value_range):
    mutate_percentage = mutation_rate * 100
    for individual in range(len(population)):
        for gene in range(len(population[individual])):
            mutate = random.randint(1, 100) < mutate_percentage
            if mutate:
                addition = hmath.lin_map(random.random(), 0, 1, value_range[0], value_range[1])
                new_value = population[individual][gene] + addition
                population[individual][gene] = hmath.constrain(new_value, value_range[0], value_range[1])
    return population


def _mutate(population, mutation_rate, value_range, function):
    mutate_percentage = mutation_rate * 100
    for individual in range(len(population)):
        for gene in range(len(population[individual])):
            mutate = random.randint(1, 100) < mutate_percentage
            if mutate:
                population[individual][gene] = function(value_range)
    return population
