from wordle_solver import WORDS, filter_words


class Strategy:
    """
    Always guess the next word in the list of possible words. After the result of each guess, update the list of
    possible words.
    """
    def __init__(self):
        self.last_guess = None
        self.possible_words = WORDS

    def get_guess(self):
        if not self.possible_words:
            raise Exception('No possible words found')
        self.last_guess = self.possible_words[0]
        return self.last_guess

    def receive_result_of_last_guess(self, result):
        self.possible_words = filter_words(words=self.possible_words, guess=self.last_guess, result=result)
