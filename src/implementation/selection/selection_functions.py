import random


def best_fraction():
    pass


def tournament(result: list, fitness=False, rounds=1):
    # result = [(individual, score), (individual, score), ...]
    if fitness:
        scale = -1  # If fitness is selected rather than cost, lower scores is better, so swap sign
    else:
        scale = 1

    for _ in range(rounds):
        result.sort(key=lambda k: scale * k[1])
        population_size = len(result)

        # Check odd or even
        odd = population_size % 2 != 0
        if odd:
            result.pop(-1)  # Remove worst scoring individual if odd population
            population_size -= 1

        # a = [i for i in range(population_size)]
        # pair_index = []
        # for i in range(population_size):
        #     index = random.randint(0, len(a) - 1)
        #     c = a.pop(index)
        #     pair_index.append(c)
        pair_index = list(range(population_size))
        pair_index.sort(key=lambda k: (random.random() - 0.5)*k)
        pairs = [[result[pair_index[i]], result[pair_index[i + 1]]] for i in range(0, population_size, 2)]
        keep = []
        for pair in pairs:
            pair.sort(key=lambda k: scale * k[1])
            keep.append(pair[0])
        result = keep
    return sorted(result, key=lambda k: scale * k[1])


def _main(rounds=1):
    result = [([random.randint(-10, 10) for _ in range(3)], n) for n in range(10)]
    for i in range(rounds):
        result = tournament(result, fitness=True)
        print(result)


if __name__ == '__main__':
    _main(rounds=1)

