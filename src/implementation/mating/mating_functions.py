import random
import math


def sp_crossover(breeders: list, pop_size: int, ordered=False, fitness=False):
    scale = -1 if fitness else 1
    if ordered:
        breeders.sort(key=lambda k: scale * k[1])
    else:
        breeders.sort(key=lambda k: (random.random() - 0.5) * k[1])

    num_breeders = len(breeders)
    children_pr_breeder = math.ceil(pop_size / num_breeders)

    children = []
    for i in range(num_breeders):
        breeder = breeders[i][0]
        skip_counter = 1
        for j in range(children_pr_breeder):
            index = (i + j + skip_counter) % num_breeders
            if index == i:
                index += 1
                skip_counter += 1
                index = (i + j + skip_counter) % num_breeders
            mate = breeders[index][0]
            crossover_index = random.randint(0, len(breeders) - 1)
            child = breeder[0:crossover_index] + mate[crossover_index:]
            children.append(child)
    child_surplus = len(children) - pop_size
    for i in range(child_surplus):
        children.pop(random.randint(0, len(children) - 1))
    return children
