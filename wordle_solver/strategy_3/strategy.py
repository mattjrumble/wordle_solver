from os.path import join

from wordle_solver import WORDS, filter_words
from wordle_solver.strategy_3 import find_best_next_guess

BEST_FIRST_GUESS = 'LARES'
BEST_SECOND_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_second_guesses.txt')
BEST_THIRD_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_third_guesses.txt')


def load_best_second_guess_mapping():
    mapping = {}
    with open(BEST_SECOND_GUESSES_FILENAME) as fd:
        for line in fd.readlines():
            _, first_result_string, second_guess = line.strip().split(' ')
            first_result = tuple(int(x) for x in first_result_string)
            mapping[first_result] = second_guess
    return mapping


def load_best_third_guess_mapping():
    mapping = {}
    with open(BEST_THIRD_GUESSES_FILENAME) as fd:
        for line in fd.readlines():
            _, first_result_string, _, second_result_string, third_guess = line.strip().split(' ')
            first_result = tuple(int(x) for x in first_result_string)
            second_result = tuple(int(x) for x in second_result_string)
            if first_result in mapping:
                mapping[first_result][second_result] = third_guess
            else:
                mapping[first_result] = {second_result: third_guess}
    return mapping


BEST_SECOND_GUESS_MAPPING = load_best_second_guess_mapping()
BEST_THIRD_GUESS_MAPPING = load_best_third_guess_mapping()


class Strategy:
    """
    Use a pre-calculated mapping for the first three guesses. After the first three guesses, pick the guess that gives
    the lower number of remaining possible answers, when averaged across all possible answers.
    """
    def __init__(self):
        self.guess_count = 0
        self.last_guess = None
        self.first_result = None
        self.second_result = None
        self.possible_words = WORDS

    def get_guess(self):
        self.guess_count += 1

        if self.guess_count == 1:
            guess = BEST_FIRST_GUESS
        elif self.guess_count == 2:
            guess = BEST_SECOND_GUESS_MAPPING[self.first_result]
        elif self.guess_count == 3:
            guess = BEST_THIRD_GUESS_MAPPING[self.first_result][self.second_result]
        else:
            guess = find_best_next_guess(words=self.possible_words)

        self.last_guess = guess
        return guess

    def receive_result_of_last_guess(self, result):
        if self.guess_count == 1:
            self.first_result = result
        elif self.guess_count == 2:
            self.second_result = result
        self.possible_words = filter_words(words=self.possible_words, guess=self.last_guess, result=result)
