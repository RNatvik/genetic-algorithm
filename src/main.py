import matplotlib.pyplot as plt
import implementation as impl
from algorithm.genetic_algorithm import GeneticAlgorithm

a0 = [-10, 15, 23, 10, -50]
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
    xs, ys = generate_target()
    order = len(a) - 1
    cost = 0
    for i in range(len(xs)):
        x = xs[i]
        y = 0
        for j in range(len(a)):
            y += a[j] * pow(x, order - j)
        cost += abs(ys[i] - y)
    return cost


def main():
    global a0
    algorithm = GeneticAlgorithm(
        100,
        len(a0),
        0.5,
        cost_star_arg=False,
        value_range=[-500, 500]
    )
    result = algorithm.run(
        1000,
        cost_func,
        impl.selection.tournament,
        impl.mating.sp_crossover,
        impl.mutation.random_mutation,
        select_kwarg={'rounds': 2},
        ensure_elitism=True
    )

    xs, ys = generate_target()
    legend = ['target']

    plt.figure()
    plt.plot(xs, ys)

    for i in range(1):
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
    main()
