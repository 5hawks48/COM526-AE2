import numpy as np
import pandas as pd

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

solved_board = [
    [7, 8, 5, 4, 3, 9, 1, 2, 6],
    [6, 1, 2, 8, 7, 5, 3, 4, 9],
    [4, 9, 3, 6, 2, 1, 5, 7, 8],
    [8, 5, 7, 9, 4, 3, 2, 6, 1],
    [2, 6, 1, 7, 5, 8, 9, 3, 4],
    [9, 3, 4, 1, 6, 2, 7, 8, 5],
    [5, 7, 8, 3, 9, 4, 6, 1, 2],
    [1, 2, 6, 5, 8, 7, 4, 9, 3],
    [3, 4, 9, 2, 2, 6, 8, 5, 7]
]
# https://boyet.com/blog/solving-sudoku-with-backtracking
boyet_grid = [
    [0, 6, 0, 0, 0, 0, 0, 9, 0],
    [9, 0, 0, 8, 7, 3, 0, 0, 1],
    [5, 0, 0, 0, 0, 0, 0, 0, 4],
    [2, 0, 0, 6, 0, 4, 0, 0, 8],
    [0, 0, 6, 0, 8, 0, 2, 0, 0],
    [7, 0, 0, 5, 0, 2, 0, 0, 3],
    [8, 0, 0, 0, 0, 0, 0, 0, 6],
    [6, 0, 0, 9, 3, 8, 0, 0, 7],
    [0, 2, 0, 0, 0, 0, 0, 4, 0]
]

# Designed to be hard for backtrackers, takes 69,175,252 backtracks.
# https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#/media/File:Sudoku_puzzle_hard_for_brute_force.svg
hard_for_brute_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 8, 5],
    [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 1, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 7, 3],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 9]
]

unsolvable_grid = [
    [0, 0, 9, 0, 2, 8, 7, 0, 0],
    [8, 0, 6, 0, 0, 4, 0, 0, 5],
    [0, 0, 3, 0, 0, 0, 0, 0, 4],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 7, 1, 3, 4, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2],
    [3, 0, 0, 0, 0, 0, 5, 0, 0],
    [9, 0, 0, 4, 0, 0, 8, 0, 7],
    [0, 0, 1, 2, 5, 0, 3, 0, 0]
]


def get_grids(amount):
    """
    Load grids from "sudoku.csv" as a two 9x9 arrays, one for 'quizzes' and one for 'solutions'
    :param amount:
    :return: quizzes, solutions
    """
    quizzes = np.zeros((amount, 81), np.int32)
    solutions = np.zeros((amount, 81), np.int32)
    total = 0
    with (open('sudoku.csv', 'r')) as file:
        for i, line in enumerate(file.read().splitlines()[1:]):
            if total == amount:
                break
            total = total + 1
            quiz, solution = line.split(",")
            for j, q_s in enumerate(zip(quiz, solution)):
                q, s = q_s
                quizzes[i, j] = q
                solutions[i, j] = s
        quizzes = quizzes.reshape((-1, 9, 9))
        solutions = solutions.reshape((-1, 9, 9))
    return quizzes, solutions


def get_panda_grids(amount):
    """
    Load grids from "sudoku.csv" as a pandas dataframe.
    :param amount:
    :return:
    """
    data = pd.read_csv("sudoku.csv", nrows=amount, skip_blank_lines=True)
    try:
        data = pd.DataFrame({"quizzes": data["puzzle"], "solutions": data["solution"]})
    except:
        pass
    return data
