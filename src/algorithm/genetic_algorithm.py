from helpers.math import lin_map
import random


class GeneticAlgorithm:

    def __init__(self, pop_size, num_genes, mut_rate, cost_star_arg=False, binary=False, value_range=None):
        """
        Construct genetic algorithm population parameters
        :param pop_size: The population size
        :param num_genes: The number of variables in each solution
        :param mut_rate: How often to mutate variables (set a value between 0 and 1)
        :param cost_star_arg: specify if the variables of a solution should be passed
                              to the cost function as *args or a list
        :param binary: specify if variables should be binary values. Default false
        :param value_range: specify range of values to be used. Default [0, 1]
        """
        self.cost_star_arg = cost_star_arg
        self.mut_rate = mut_rate
        self.num_genes = num_genes
        self.pop_size = pop_size
        self.binary = binary
        self.value_range = value_range
        if self.value_range is None:
            self.value_range = [0, 1]
        self.population = self._generate_initial()

    def run(self, max_iterations, cost_function, select_func, breed_func, mutate_func,
            cost_kwarg=None, select_kwarg=None, breed_kwarg=None, mutate_kwarg=None,
            ensure_elitism=False):

        cost_kwarg = {} if cost_kwarg is None else cost_kwarg
        select_kwarg = {} if select_kwarg is None else select_kwarg
        breed_kwarg = {} if breed_kwarg is None else breed_kwarg
        mutate_kwarg = {} if mutate_kwarg is None else mutate_kwarg

        result = self._evaluate(cost_function, self.population, **cost_kwarg)
        for i in range(max_iterations):
            print(i)
            breeders = select_func(result, **select_kwarg)  # Expects breeders to be sorted in descending order
            new_population = breed_func(breeders, self.pop_size, **breed_kwarg)
            new_population = mutate_func(new_population, self.mut_rate, self.value_range, **mutate_kwarg)
            if ensure_elitism:
                new_population.pop(random.randint(0, len(new_population) - 1))
                new_population.append(breeders[0][0])
            if self.binary:
                new_population = self._make_binary(new_population)
            self.population = new_population
            result = self._evaluate(cost_function, self.population, **cost_kwarg)
        result.sort(key=lambda k: k[1])
        return result

    def _evaluate(self, cost_function, population, **kwargs):
        costs = []
        for individual in population:
            if self.cost_star_arg:
                cost = cost_function(*individual, **kwargs)
            else:
                cost = cost_function(individual, **kwargs)
            costs.append(cost)
        return list(zip(population, costs))

    def _make_binary(self, population):
        for individual in range(len(population)):
            for gene in range(len(population[individual])):
                population[individual][gene] = int(population[individual][gene] >= 0.5)
        return population


    def _generate_initial(self):

        if self.binary:
            population = [
                [random.randint(0, 1) for _ in range(self.num_genes)] for _ in range(self.pop_size)
            ]
        else:
            population = [
                [
                    lin_map(random.random(), 0, 1, self.value_range[0], self.value_range[1])
                    for _ in range(self.num_genes)
                ]
                for _ in range(self.pop_size)
            ]
        return population
