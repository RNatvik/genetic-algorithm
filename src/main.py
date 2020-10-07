import time

import matplotlib.pyplot as plt
import implementation as impl
from algorithm.genetic_algorithm import GeneticAlgorithm

a0 = [5, 15, 23]
x_scale = 1


def generate_target():
    global a0
    xs = list(range(-75 * x_scale, 100 * x_scale, 1))
    xs = [x / x_scale for x in xs]
    ys = []
    order = len(a0) - 1
    for x in xs:
        y = 0
        for i in range(len(a0)):
            y += a0[i] * pow(x, order - i)
        ys.append(y)
    return xs, ys


def cost_func(a):
    time.sleep(0.01)
    xs, ys = generate_target()
    order = len(a) - 1
    cost = 0
    for i in range(len(xs)):
        x = xs[i]
        y = 0
        for j in range(len(a)):
            y += a[j] * pow(x, order - j)
        cost += pow(abs(ys[i] - y), 2)
    return cost


def main():
    global a0
    algorithm = GeneticAlgorithm(
        500,
        len(a0),
        0.5,
        cost_star_arg=False,
        value_range=[-500, 500],
        num_threads=2
    )
    result = algorithm.run(
        10,
        cost_func,
        impl.selection.tournament,
        impl.mating.sp_crossover,
        impl.mutation.random_mutation,
        select_kwarg={'rounds': 2},
        ensure_elitism=True,
        enable_timer=True
    )

    xs, ys = generate_target()
    legend = ['target']

    plt.figure()
    plt.plot(xs, ys)

    for i in range(5):
        solution = result[i][0]
        order = len(solution) - 1
        s = []
        for x in xs:
            y = 0
            for j in range(len(solution)):
                y += solution[j] * pow(x, order - j)
            s.append(y)
        plt.plot(xs, s)
        legend.append(f'r{i}')

    plt.grid()
    plt.legend(legend)
    plt.show()

    # x, y = generate_target()
    # plt.figure()
    # plt.plot(x, y)
    # plt.grid()
    # plt.show()


if __name__ == '__main__':
    s = time.time()
    main()
    e = time.time()
    print(f'\n\nDuration: {e-s}')
