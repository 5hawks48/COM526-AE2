import numpy as np


def normal_guesses(grid=None):
    """
    Create a list of numbers 1 through 9.
    :return:
    """
    return np.arange(1, 10)


def randomised_guesses(grid=None):
    """
    Create a list of numbers 1 through 9 in random order.
    :return:
    """
    guess_array = np.arange(1, 10)
    np.random.shuffle(guess_array)
    return guess_array


def get_order_by_most_common(grid):
    """
    Get a list of the numbers in the grid from most-least common. Zeroes are removed.
    Credit: paul-panzer @ https://stackoverflow.com/a/42186357
    :param grid:
    :return:
    """
    values, counts = np.unique(grid, return_counts=True)
    order = np.argsort(-counts)[:10]
    # order = np.argpartition(-counts, range(len(counts)))[:10]
    # Remove 0's.
    order = [x for x in order if x != 0]
    return order


def get_order_by_least_common(grid):
    """
    Inverse of get_order_by_most_common().
    https://stackoverflow.com/a/42186357
    :param grid:
    :return:
    """
    return get_order_by_most_common(grid)[::-1]
