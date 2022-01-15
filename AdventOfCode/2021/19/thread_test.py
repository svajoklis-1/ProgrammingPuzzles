from multiprocessing import Pool, Queue


def f(i):
    return [i + 1, 2, 3]


if __name__ == '__main__':
    with Pool(5) as p:
        tasks = []
        tasks.append(p.apply_async(f, [1]))
        tasks.append(p.apply_async(f, [2]))
        tasks.append(p.apply_async(f, [3]))

        print([res.get() for res in tasks])
