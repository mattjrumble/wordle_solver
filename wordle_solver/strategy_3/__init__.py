from os.path import join

from wordle_solver import WORDS, filter_words

MAPPING_FILENAME = join('wordle_solver', 'strategy_3', 'precalculations', 'best_guesses_complete.txt')


def load_mapping():
    mapping = {}
    with open(MAPPING_FILENAME) as fd:
        for line in fd.readlines():
            *keys, value = line.strip().split(' ')
            current_level = mapping
            for key in keys[:-1]:
                if key.isnumeric():
                    key = tuple(int(x) for x in key)
                if key not in current_level:
                    current_level[key] = {}
                current_level = current_level[key]
            current_level[tuple(int(x) for x in keys[-1])] = value
    return mapping


MAPPING = load_mapping()


class Strategy:
    """
    Use the pre-calculated complete mapping for all guesses.
    """
    def __init__(self):
        self.mapping = MAPPING
        self.last_guess = None
        self.possible_words = WORDS

    def get_guess(self):
        if isinstance(self.mapping, str):
            self.last_guess = self.mapping
        else:
            self.last_guess = list(self.mapping.keys())[0]
        return self.last_guess

    def receive_result_of_last_guess(self, result):
        self.possible_words = filter_words(words=self.possible_words, guess=self.last_guess, result=result)
        if result != (2, 2, 2, 2, 2):
            self.mapping = self.mapping[self.last_guess][result]
