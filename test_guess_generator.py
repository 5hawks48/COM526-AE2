from copy import deepcopy
from unittest import TestCase

import numpy as np

import grids
from guess_generator import get_order_by_most_common, get_order_by_least_common, randomised_guesses, normal_guesses


class Test(TestCase):
    GRIDS = 10
    quizzes: any
    solutions: any

    @classmethod
    def setUpClass(cls):
        cls.quizzes, cls.solutions = grids.get_grids(cls.GRIDS)

    def test_get_order_by_most_common(self):
        grid_to_solve = deepcopy(self.quizzes[0])
        order = get_order_by_most_common(grid_to_solve)
        expected = [3, 9, 1, 4, 5, 6, 2, 7, 8]
        self.assertTrue(np.array_equal(order, expected))

    def test_get_order_by_least_common(self):
        grid_to_solve = deepcopy(self.quizzes[0])
        order = get_order_by_least_common(grid_to_solve)
        expected = [3, 9, 1, 4, 5, 6, 2, 7, 8][::-1]
        self.assertTrue(np.array_equal(order, expected))

    def test_randomised_guesses(self):
        guesses = randomised_guesses()
        self.assertEqual(9, len(guesses))

    def test_normal_guesses(self):
        guesses = normal_guesses()
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertTrue(np.array_equal(guesses, expected))
