from unittest import TestCase

import numpy as np

import grids


class Test(TestCase):
    def test_get_grids(self):
        amount = 1000
        quizzes, solutions = grids.get_grids(amount)
        self.assertEqual(len(quizzes), amount)
        self.assertEqual(len(solutions), amount)
        self.assertEqual(quizzes.size, amount * 81)
        grid_999 = [
            [0, 0, 0, 0, 0, 8, 4, 0, 7], [0, 4, 0, 0, 9, 0, 6, 0, 5], [1, 3, 7, 0, 4, 6, 0, 0, 8],
            [0, 5, 0, 2, 1, 0, 0, 8, 0], [0, 7, 0, 3, 0, 0, 9, 0, 0], [2, 0, 0, 8, 0, 0, 0, 6, 3],
            [0, 0, 0, 9, 0, 0, 0, 0, 0], [5, 0, 4, 0, 0, 2, 0, 0, 0], [6, 8, 9, 0, 0, 7, 1, 5, 0]
        ]
        self.assertTrue(np.array_equal(quizzes[999], grid_999))
