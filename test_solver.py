import unittest
from copy import deepcopy

import numpy as np

import grids
from solver import find_empty_square, is_valid, solve


class Test(unittest.TestCase):
    GRIDS = 10
    quizzes: any
    solutions: any

    @classmethod
    def setUpClass(cls):
        cls.quizzes, cls.solutions = grids.get_grids(cls.GRIDS)

    def test_find_empty_square(self):
        grid_to_solve = deepcopy(self.quizzes[2])
        row, col = find_empty_square(grid_to_solve)
        self.assertEqual(row, 0)
        self.assertEqual(col, 1)

    def test_is_valid(self):
        grid_to_solve = deepcopy(self.quizzes[0])
        # Test row
        self.assertFalse(is_valid(grid_to_solve, 4, (0, 1)))
        # Test box
        self.assertFalse(is_valid(grid_to_solve, 4, (1, 1)))
        # Test col
        self.assertFalse(is_valid(grid_to_solve, 4, (6, 2)))
        # Test valid
        self.assertTrue(is_valid(grid_to_solve, 8, (0, 0)))

    def test_solve(self):
        grid_to_solve = deepcopy(self.quizzes[0])
        backtracks = 0
        solved, backtracks = solve(grid_to_solve, backtracks, False)
        self.assertEqual(backtracks, 135)
        self.assertTrue(np.array_equal(grid_to_solve, self.solutions[0]))
        self.assertTrue(solved)
