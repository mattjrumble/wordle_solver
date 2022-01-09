from wordle_solver import WORDS, LETTER_FREQUENCIES, result_of_guess


WORD_FREQUENCY_SCORES = {
    word: sum(LETTER_FREQUENCIES[l] for l in set(word)) for word in WORDS
}


def filter_words(words, guess, result):
    """
    Filter the list of words based on a guess result.
    """
    # The naive approach is to loop through every word, get the result of the guess assuming that word is correct, and
    # checking if that result matches the given result. This can be made a little quicker by working out which letters
    # from the guess are correct and which are incorrect, checking for those letters in the list of words first, and
    # only then comparing the full results.
    correct_letters = set(guess[i] for i, spot in enumerate(result) if spot in (1, 2))
    incorrect_letters = set(guess) - correct_letters

    filtered_words = []
    for word in words:
        unique_letters = set(word)
        if any(letter in unique_letters for letter in incorrect_letters):
            continue
        if all(letter in unique_letters for letter in correct_letters):
            if result_of_guess(guess, word) == result:
                filtered_words.append(word)

    return filtered_words


class Strategy:
    """
    Always guess the "best" word in the list of possible words. After the result of each guess, update the list of
    possible words. The "best" word is determined based on a scoring of how common each letter in the word is - words
    with the more common letters are favoured.
    """
    def __init__(self):
        self.last_guess = None
        self.possible_words = WORDS

    def get_guess(self):
        if not self.possible_words:
            raise Exception('No possible words found')
        self.last_guess = self.best_word(self.possible_words)
        return self.last_guess

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
        self.possible_words = filter_words(words=self.possible_words, guess=self.last_guess, result=result)
