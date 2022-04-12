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
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                return row, col
    return None


quiz_count = 1
quizzes, solutions = grids.get_grids(quiz_count)
repetitions = 10
total_backtracks = 0
randomise_guess_array = True

for quiz_index in range(len(quizzes)):
    total_backtracks_for_quiz = 0
    for j in range(repetitions):
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
    avg_backtracks_for_quiz = total_backtracks_for_quiz / repetitions
    print(">>>>>> Average backtracks for quiz " + str(quiz_index) + ": = " + str(avg_backtracks_for_quiz))

avg_backtracks = total_backtracks / (repetitions * quiz_count)
print("Average backtracks for all = " + str(avg_backtracks))


# TODO: Use the 3m puzzle set as it includes difficulty ratings + more
