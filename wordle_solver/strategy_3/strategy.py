from wordle_solver import WORDS, LETTER_FREQUENCIES, filter_words
from wordle_solver.strategy_3 import BEST_FIRST_GUESS, BEST_SECOND_GUESSES_FILENAME


def load_best_second_guess_mapping():
    mapping = {}
    with open(BEST_SECOND_GUESSES_FILENAME) as fd:
        for line in fd.readlines():
            result_string, word = line.strip().split(' ')
            mapping[tuple(int(x) for x in result_string)] = word
    return mapping


BEST_SECOND_GUESS_MAPPING = load_best_second_guess_mapping()

WORD_FREQUENCY_SCORES = {
    word: sum(LETTER_FREQUENCIES[l] for l in set(word)) for word in WORDS
}


class Strategy:
    """
    Use a pre-calculated mapping for the first two guesses. After the first two guesses, act like Strategy 2.
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
            # After the first two guesses, act like Strategy 2
            guess = self.best_word(self.possible_words)

        self.last_guess = guess
        return guess

    @staticmethod
    def best_word(words):
        best_word, best_score = None, -1
        for word in words:
            score = WORD_FREQUENCY_SCORES[word]
            if score > best_score:
                best_word = word
                best_score = score
        return best_word

    def receive_result_of_last_guess(self, result):
        self.last_result = result
        self.possible_words = filter_words(words=self.possible_words, guess=self.last_guess, result=result)
