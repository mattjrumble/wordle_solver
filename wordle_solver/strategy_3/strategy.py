from os.path import join
from sys import maxsize

from wordle_solver import WORDS, filter_words, result_of_guess


BEST_FIRST_GUESS = 'LARES'
BEST_SECOND_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_second_guesses.txt')


def load_best_second_guess_mapping():
    mapping = {}
    with open(BEST_SECOND_GUESSES_FILENAME) as fd:
        for line in fd.readlines():
            _, result_string, word = line.strip().split(' ')
            mapping[tuple(int(x) for x in result_string)] = word
    return mapping


BEST_SECOND_GUESS_MAPPING = load_best_second_guess_mapping()


class Strategy:
    """
    Use a pre-calculated mapping for the first two guesses. After the first two guesses, pick the word from the list
    of remaining possible answers that gives the lower number of remaining possible words, when averaged across all
    possible answers.
    """
    def __init__(self):
        self.guess_count = 0
        self.last_guess = None
        self.last_result = None
        self.possible_words = WORDS

    def get_guess(self):
        self.guess_count += 1

        if self.guess_count == 1:
            guess = BEST_FIRST_GUESS
        elif self.guess_count == 2:
            guess = BEST_SECOND_GUESS_MAPPING[self.last_result]
        else:
            best_guess = None
            best_total = maxsize
            for possible_guess in self.possible_words:
                total = sum(len(filter_words(
                    words=self.possible_words,
                    guess=possible_guess,
                    result=result_of_guess(guess=possible_guess, answer=answer)
                )) for answer in self.possible_words)
                if total < best_total:
                    best_guess = possible_guess
                    best_total = total
            guess = best_guess

        self.last_guess = guess
        return guess

    def receive_result_of_last_guess(self, result):
        self.last_result = result
        self.possible_words = filter_words(words=self.possible_words, guess=self.last_guess, result=result)
