import csv

import numpy as np

import grids
from guess_generator import get_order_by_most_common, get_order_by_least_common, randomised_guesses, normal_guesses
from solver import solve


def benchmark_time(quiz_count,
                   guess_method,
                   randomise_search):
    import time
    quizzes, solutions = grids.get_grids(quiz_count)
    total_backtracks = 0
    max_backtracks = 0
    outputs = [0 for _ in range(7)]
    outputs[0] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    outputs[1] = quiz_count
    outputs[2] = guess_method.__name__
    outputs[3] = randomise_search
    print("Starting benchmark w/ time")
    start_time = time.perf_counter()
    for quiz_index in range(len(quizzes)):
        backtracks = 0
        solved, backtracks = solve(quizzes[quiz_index], backtracks, guess_method, randomise_search)
        total_backtracks = total_backtracks + backtracks
        if solved is False:
            raise ValueError("Quiz %s failed! " % quiz_index)
        if backtracks > max_backtracks:
            max_backtracks = backtracks
    elapsed_time = (time.perf_counter() - start_time)
    average_backtracks = (total_backtracks / quiz_count)
    print("--- %s seconds ---" % elapsed_time)
    print("--- Average Backtracks =  %s ---" % average_backtracks)
    print("--- Max Backtracks =  %s ---" % max_backtracks)
    outputs[4] = average_backtracks
    outputs[5] = max_backtracks
    outputs[6] = elapsed_time
    print(outputs)
    with open('benchmarks.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(outputs)


# def benchmark_timeit(quizzes):
#     for quiz_index in range(len(quizzes)):
#         backtracks = 0
#         solve(quizzes[quiz_index], backtracks, False, False)


# import timeit
# print("Starting benchmark w/ timeit")
# quizzes, solutions = grids.get_grids(1)
# t = timeit.Timer(lambda: benchmark_timeit(quizzes))
# print("--- %s seconds ---" % t.timeit(1))

quiz_count = 1


benchmark_time(quiz_count, normal_guesses, False)
