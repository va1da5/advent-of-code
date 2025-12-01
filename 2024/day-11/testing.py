import functools
from multiprocessing import Pool
import time


def show(numbers):
    print(" ".join([str(number) for number in numbers]))


@functools.cache
def apply(number):
    if number == 0:
        return [1]

    n = str(number)

    if len(n) % 2 == 0:
        return [int(n[0 : round(len(n) / 2)]), int(n[round(len(n) / 2) :])]

    return [number * 2024]


def get_stones(value: str):
    return [int(x) for x in value.split(" ")]


@functools.cache
def get_individual(number):
    stones = [number]
    for i in range(75):
        print(i)
        out = []
        for number in stones:
            out.extend(apply(number))
        stones = out
    return len(stones)


def main():
    with open("input.txt", "r") as f:
        content = f.read()

    # stones = get_stones("125 17")

    # start_time = time.perf_counter()
    # stones = get_stones(content)
    # for i in range(30):
    #     # print(i)
    #     out = []
    #     for number in stones:
    #         out.extend(apply(number))
    #     stones = [*out]
    # finish_time = time.perf_counter()
    # print(f"{len(stones)=} took: {finish_time-start_time}s")

    start_time = time.perf_counter()
    stones = get_stones(content)

    with Pool() as pool:
        out = pool.map(get_individual, stones)

    finish_time = time.perf_counter()
    print(f"{sum(out)=} took: {finish_time-start_time}s")

    # start_time = time.perf_counter()
    # stones = get_stones(content)
    # for i in range(25):
    #     # print("🔥")
    #     # print(stones)
    #     # print(i)
    #     out = []
    #     with Pool() as pool:
    #         for result in pool.map(apply, stones):
    #             out = [*out, *result]
    #     stones = [*out]

    # finish_time = time.perf_counter()
    # print(f"{len(stones)=} took: {finish_time-start_time}s")


if __name__ == "__main__":
    main()
