from abc import ABC, abstractmethod


with open('words.txt') as fd:
    WORDS = [line.strip() for line in fd.readlines()]


class ImpossibleResult(Exception):
    pass


class BaseStrategy(ABC):
    def __init__(self):
        self.possible_words = WORDS
        self.last_guess = None

    @abstractmethod
    def _get_guess(self):
        pass

    def get_guess(self):
        if not self.possible_words:
            raise ImpossibleResult('No possible words found')
        self.last_guess = self._get_guess()
        return self.last_guess

    def receive_result_of_last_guess(self, result):
        self.possible_words = filter_words(words=self.possible_words, guess=self.last_guess, result=result)


def result_of_guess(guess, answer):
    """
    Return a tuple of five integers representing the result of a guess.
    2 = Correct letter, correct spot.
    1 = Correct letter, wrong spot.
    0 = Wrong letter.
    """
    result = [None, None, None, None, None]
    remaining_letters = list(answer)

    # Mark the letters which are in the correct spot.
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            result[i] = 2
            remaining_letters.remove(letter)

    # Go through the remaining letters in the guess and check if that letter is still in the answer, after the letters
    # in the correct spot have been taken out.
    for i, letter in enumerate(guess):
        if result[i] is None:
            if letter in remaining_letters:
                result[i] = 1
                remaining_letters.remove(letter)
            else:
                result[i] = 0

    return tuple(result)


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
