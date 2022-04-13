import csv
from copy import deepcopy

import numpy as np

import grids


def solve(grid, backtracks, randomise_guesses=False):
    empty_square_pos = find_empty_square(grid)
    if not empty_square_pos:
        return (True, backtracks)
    else:
        row, col = empty_square_pos
    guess_array = np.arange(1, 10)
    if randomise_guesses:
        np.random.shuffle(guess_array)
    for i in guess_array:
        if is_valid(grid, i, (row, col)):
            grid[row][col] = i
            solved, backtracks = solve(grid, backtracks, randomise_guesses)
            if solved:
                return (True, backtracks)
            else:
                # Backtrack
                grid[row][col] = 0
                backtracks = backtracks + 1
    return (False, backtracks)


def is_valid(grid, num, pos):
    """
    Check the row, column and 3x3 box (excluding pos) for number.
    :param grid:
    :param num:
    :param pos:
    :return: True if no match found (valid).
    """
    # Check row
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(grid)):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False
    return True


def print_grid(grid):
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")


def find_empty_square(grid):
    """
    Searches a grid from left-right, top-bottom for 0.
    :param grid:
    :return: row, col
    """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                return row, col
    return None


def main():
    quiz_count = 7500
    quizzes, solutions = grids.get_grids(quiz_count)
    repetitions_per_quiz = 1
    total_backtracks = 0
    randomise_guess_array = False
    for quiz_index in range(len(quizzes)):
        total_backtracks_for_quiz = 0
        for i in range(repetitions_per_quiz):
            grid_to_solve = deepcopy(quizzes[quiz_index])
            # print_grid(grid_to_solve)
            backtracks = 0
            solved, backtracks = solve(grid_to_solve, backtracks, randomise_guess_array)
            print("> QUIZ " + str(quiz_index) + " RESULT:")
            # Compare the result to solution
            if solved is True:
                print(">> IS SOLVED")
                if not np.array_equal(grid_to_solve, solutions[quiz_index]):
                    print(">> BUT IT DIDN'T MATCH THE SOLUTION")
            else:
                print(">> CANNOT BE SOLVED!!!")
            # Display the result
            # print_grid(grid_to_solve)
            print(">>>> Backtracks = " + str(backtracks))
            total_backtracks += backtracks
            total_backtracks_for_quiz += backtracks
        avg_backtracks_for_quiz = total_backtracks_for_quiz / repetitions_per_quiz
        print(">>>>>> Average backtracks for quiz " + str(quiz_index) + ": = " + str(avg_backtracks_for_quiz))

    avg_backtracks = total_backtracks / (repetitions_per_quiz * quiz_count)
    print("Average backtracks for all = " + str(avg_backtracks))


def benchmark_time():
    import time
    quiz_count = 7500
    randomise_guess_array = False
    quizzes, solutions = grids.get_grids(quiz_count)
    total_backtracks = 0
    max_backtracks = 0
    outputs = [0 for _ in range(8)]
    outputs[0] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    outputs[1] = quiz_count
    outputs[2] = randomise_guess_array
    print("Starting benchmark w/ time")
    start_time = time.perf_counter()
    for quiz_index in range(len(quizzes)):
        backtracks = 0
        solved, backtracks = solve(quizzes[quiz_index], backtracks, randomise_guess_array)
        total_backtracks = total_backtracks + backtracks
        if backtracks > max_backtracks:
            max_backtracks = backtracks
    elapsed_time = (time.perf_counter() - start_time)
    average_backtracks = (total_backtracks / quiz_count)
    print("--- %s seconds ---" % elapsed_time)
    print("--- Average Backtracks =  %s ---" % average_backtracks)
    print("--- Max Backtracks =  %s ---" % max_backtracks)
    outputs[5] = average_backtracks
    outputs[6] = max_backtracks
    outputs[7] = elapsed_time
    print(outputs)
    with open('benchmarks.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(outputs)


def benchmark_timeit(quizzes):
    for quiz_index in range(len(quizzes)):
        backtracks = 0
        solve(quizzes[quiz_index], backtracks, False)


if __name__ == "__main__":
    # import timeit
    # print("Starting benchmark w/ timeit")
    # quizzes, solutions = grids.get_grids(7500)
    # t = timeit.Timer(lambda: benchmark_timeit(quizzes))
    # print("--- %s seconds ---" % t.timeit(1))
    benchmark_time()
    # main()

# TODO: Use the 3m puzzle set as it includes difficulty ratings + more
