from wordle_solver import BaseStrategy


class Strategy(BaseStrategy):
    """
    Always guess the next word in the list of possible words. After the result of each guess, update the list of
    possible words.
    """
    def _get_guess(self):
        return self.possible_words[0]
