import implementation.selection.selection_functions as selection
import implementation.mating.mating_functions as mating
from helpers.math import lin_map
import decorators as deco
import random


class GeneticAlgorithm:

    def __init__(self, pop_size, num_genes, mut_rate, cost_star_arg=False, binary=False, value_range=None):
        self.cost_star_arg = cost_star_arg
        self.mut_rate = mut_rate
        self.num_genes = num_genes
        self.pop_size = pop_size
        self.binary = binary
        self.value_range = value_range
        if self.value_range is None:
            self.value_range = [-1, 1]
        self.population = self._generate_initial()
        # print(self.population)

    def run(self, max_iterations, cost_function, select_func, breed_func, mutate_func,
            cost_kwarg=None, select_kwarg=None, breed_kwarg=None, mutate_kwarg=None,
            ensure_elitism=False):

        cost_kwarg = {} if cost_kwarg is None else cost_kwarg
        select_kwarg = {} if select_kwarg is None else select_kwarg
        breed_kwarg = {} if breed_kwarg is None else breed_kwarg
        mutate_kwarg = {} if mutate_kwarg is None else mutate_kwarg

        result = self._evaluate(cost_function, self.population, **cost_kwarg)
        for _ in range(max_iterations):
            breeders = select_func(result, **select_kwarg)  # Expects breeders to be sorted in descending order
            new_population = breed_func(breeders, self.pop_size, **breed_kwarg)
            new_population = mutate_func(new_population, self.mut_rate, self.value_range, **mutate_kwarg)
            if ensure_elitism:
                new_population.pop(random.randint(0, len(new_population) - 1))
                new_population.append(breeders[0][0])
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


def mut_func(population, mutation_rate, value_range):
    mutate_percentage = mutation_rate * 100
    for individual in range(len(population)):
        for gene in range(len(population[individual])):
            mutate = random.randint(1, 100) < mutate_percentage
            if mutate:
                population[individual][gene] = lin_map(random.random(), 0, 1, value_range[0], value_range[1])
    return population


def cost_func(a, b, c):
    a0 = -1
    b0 = 4
    c0 = -3
    x = [i/100 for i in range(1000)]
    y0 = [a0*pow(i, 2) + b0*i + c0 for i in x]
    y = [a*pow(i, 2) + b*i + c for i in x]
    cost = sum([abs(target - real) for real, target in zip(y, y0)])
    return cost


@deco.dir_active(__file__)
def main():
    algorithm = GeneticAlgorithm(
        100,
        3,
        0.2,
        binary=False,
        cost_star_arg=True,
        value_range=[-5, 5]
    )
    result = algorithm.run(
        100,
        cost_func,
        selection.tournament,
        mating.sp_crossover,
        mut_func,
        select_kwarg={'rounds': 1}
    )
    print(result)


if __name__ == '__main__':
    main()
