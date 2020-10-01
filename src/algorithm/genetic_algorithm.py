import implementation.selection.selection_functions as selection
import decorators as deco
import random


class GeneticAlgorithm:

    def __init__(self, pop_size, num_genes, mut_rate, survival_rate, binary=False, value_range=None):
        self.survival_rate = survival_rate
        self.mut_rate = mut_rate
        self.num_genes = num_genes
        self.pop_size = pop_size
        self.binary = binary
        self.value_range = value_range
        if self.value_range is None:
            self.value_range = [-1, 1]
        self.population = self._generate_initial()
        print(self.population)

    def run(self, max_iterations, cost_function, select_func, breed_func, mutate_func,
            cost_kwarg=None, select_kwarg=None, breed_kwarg=None, mutate_kwarg=None, ensure_elitism=False):

        for _ in range(max_iterations):
            result = self._evaluate(cost_function, self.population, **cost_kwarg)
            breeders = select_func(result, **select_kwarg)  # Expects breeders to be sorted in descending order
            new_population = breed_func(breeders, self.pop_size, **breed_kwarg)
            new_population = mutate_func(new_population, self.mut_rate)
            if ensure_elitism:
                new_population.pop(random.randint(0, len(new_population)-1))
                new_population.append(breeders[0][0])
            self.population = new_population

    def _evaluate(self, cost_function, population, **kwargs):
        costs = []
        for individual in population:
            cost = cost_function(individual, **kwargs)
            costs.append(cost)
        return zip(population, costs)

    def _generate_initial(self):
        def lin_map(x, x0, x1, y0, y1):
            y = x * (y1 - y0) / (x1 - x0) - y0
            return y

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


def mut_func():
    pass


def mat_func():
    pass


def cost_func(population):
    score = list(range(len(population)))
    return [(p, s) for p, s in zip(population, score)]


@deco.dir_active(__file__)
def main():
    selection_func = selection.tournament
    mutation_func = mut_func
    mating_func = mat_func
    algorithm = GeneticAlgorithm(10, 5, 1, 0.5, binary=True)


if __name__ == '__main__':
    main()
