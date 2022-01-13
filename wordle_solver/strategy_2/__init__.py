from wordle_solver import WORDS, BaseStrategy

LETTER_FREQUENCIES = {
    'A': 5738, 'B': 1547, 'C': 1947, 'D': 2364, 'E': 6441, 'F': 1071, 'G': 1576, 'H': 1682, 'I': 3595, 'J': 270,
    'K': 1426, 'L': 3269, 'M': 1908, 'N': 2854, 'O': 4248, 'P': 1945, 'Q': 104, 'R': 4027, 'S': 6427, 'T': 3206,
    'U': 2399, 'V': 661, 'W': 1013, 'X': 268, 'Y': 1992, 'Z': 412
}
WORD_FREQUENCY_SCORES = {
    word: sum(LETTER_FREQUENCIES[letter] for letter in set(word)) for word in WORDS
}


class Strategy(BaseStrategy):
    """
    Always guess the "best" word in the list of possible words. After the result of each guess, update the list of
    possible words. The "best" word is determined based on a scoring of how common each letter in the word is - words
    with the more common letters are favoured.
    """
    def _get_guess(self):
        return self.best_word(self.possible_words)

    @staticmethod
    def best_word(words):
        best_word, best_score = None, -1
        for word in words:
            score = WORD_FREQUENCY_SCORES[word]
            if score > best_score:
                best_word = word
                best_score = score
        return best_word
