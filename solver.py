import csv
from copy import deepcopy

import numpy as np
import pandas as pd
import grids

from guess_generator import get_order_by_most_common, get_order_by_least_common, randomised_guesses, normal_guesses


def solve(grid, backtracks, guess_method, randomise_search=False):
    """
    Sudoku Solver, based off of:
    Credit: techwithtim @  https://github.com/techwithtim/Sudoku-GUI-Solver
    :param grid:
    :param backtracks:
    :param guess_method: expects a method that returns an array of numbers 1 through 9.
    :param randomise_search:
    :return: Pass/Fail, No. of backtracks
    """
    # Find empty square
    if randomise_search:
        empty_square_pos = find_random_empty_square(grid)
    else:
        empty_square_pos = find_empty_square(grid)
    if not empty_square_pos:
        return (True, backtracks)
    else:
        row, col = empty_square_pos
    guess_array = guess_method(grid)
    for i in guess_array:
        if is_valid(grid, i, (row, col)):
            grid[row][col] = i
            solved, backtracks = solve(grid, backtracks, guess_method, randomise_search)
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


def find_random_empty_square(grid):
    """
    Search the grid randomly for empty squares.
    :param grid:
    :return: row, col
    """
    rows = np.arange(0, len(grid))
    cols = np.arange(0, len(grid[0]))
    np.random.shuffle(rows)
    np.random.shuffle(cols)
    for row in rows:
        for col in cols:
            if grid[row][col] == 0:
                return row, col
    return None


def parallelize_dataframe(df, func):
    """
    Credit: https://www.kaggle.com/code/yashchoudhary/deep-sudoku-solver-multiple-approaches/notebook
    """
    from multiprocessing import Pool
    num_partitions = len(df)
    num_cores = 4
    df_split = np.vsplit(df, num_partitions)
    pool = Pool(num_cores)
    results = pool.map(func, df_split)
    pool.close()
    pool.join()
    return results


def solve_and_verify(data):
    """
    Credit: https://www.kaggle.com/code/yashchoudhary/deep-sudoku-solver-multiple-approaches/notebook
    """
    total_backtracks = 0
    for row in data.iterrows():
        backtracks = 0
        quiz = np.fromiter(row[1]["quizzes"], dtype=int).reshape(9, 9)
        solved, backtracks = solve(quiz, backtracks, normal_guesses, False)
        assert solved is True
        total_backtracks = total_backtracks + backtracks
    return total_backtracks


def run_multithreaded(quiz_count):
    """
    Credit: https://www.kaggle.com/code/yashchoudhary/deep-sudoku-solver-multiple-approaches/notebook
    """
    # TODO: Specify guess type
    data = grids.get_panda_grids(quiz_count)
    results = parallelize_dataframe(data.head(quiz_count), solve_and_verify)
    return results


def run(quiz_count, repetitions_per_quiz, guess_method, randomise_search):
    try:
        quizzes, solutions = grids.get_grids(quiz_count)
    except ValueError:
        raise ValueError("Error: Quiz count exceeded total quizzes!")
    total_backtracks = 0
    for quiz_index in range(len(quizzes)):
        total_backtracks_for_quiz = 0
        for i in range(repetitions_per_quiz):
            grid_to_solve = deepcopy(quizzes[quiz_index])
            # print_grid(grid_to_solve)
            backtracks = 0
            solved, backtracks = solve(grid_to_solve, backtracks, guess_method, randomise_search)
            print("> QUIZ " + str(quiz_index) + " RESULT:")
            # Compare the result to solution
            if solved is True:
                print(">> IS SOLVED")
                if not np.array_equal(grid_to_solve, solutions[quiz_index]):
                    print(">> BUT IT DIDN'T MATCH THE SOLUTION")
            else:
                print(">> CANNOT BE SOLVED!!!")
            # Display the result
            print_grid(grid_to_solve)
            print(">>>> Backtracks = " + str(backtracks))
            total_backtracks += backtracks
            total_backtracks_for_quiz += backtracks
        avg_backtracks_for_quiz = total_backtracks_for_quiz / repetitions_per_quiz
        print(">>>>>> Average backtracks for quiz " + str(quiz_index) + ": = " + str(avg_backtracks_for_quiz))

    avg_backtracks = total_backtracks / (repetitions_per_quiz * len(quizzes))
    print("Average backtracks for all = " + str(avg_backtracks))
