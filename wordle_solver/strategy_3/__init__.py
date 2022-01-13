from os.path import join

from wordle_solver import ImpossibleResult, BaseStrategy

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


class Strategy(BaseStrategy):
    """
    Use the pre-calculated complete mapping for all guesses.
    """
    def __init__(self):
        super().__init__()
        self.mapping = MAPPING

    def _get_guess(self):
        if isinstance(self.mapping, str):
            return self.mapping
        return list(self.mapping.keys())[0]

    def receive_result_of_last_guess(self, result):
        super().receive_result_of_last_guess(result)
        if result != (2, 2, 2, 2, 2):
            try:
                self.mapping = self.mapping[self.last_guess][result]
            except KeyError:
                raise ImpossibleResult()
