from collections import defaultdict
from itertools import combinations
from string import ascii_uppercase
from sys import maxsize

from wordle_solver import result_of_guess, WORDS


def build_letters_in_words_mapping():
    """
    Map 'A' to all words containing the letter 'A'.
    Map 'AB' to all words containing the letters 'A' and 'B'.
    Etc.
    """
    mapping = defaultdict(set)
    for word in WORDS:
        for i in range(1, 6):
            for key in combinations(word, i):
                mapping[''.join(sorted(key))].add(word)
    return mapping


def build_letters_not_in_words_mapping():
    """
    Map 'A' to all words without the letter 'A'. Only do this with single letters and not groups of letters,
    otherwise this mapping will become massive.
    """
    mapping = defaultdict(set)
    for word in WORDS:
        for letter in ascii_uppercase:
            if letter not in word:
                mapping[letter].add(word)
    return mapping


LETTERS_IN_WORDS_MAPPING = build_letters_in_words_mapping()
LETTERS_NOT_IN_WORDS_MAPPING = build_letters_not_in_words_mapping()


class WorseTotal(Exception):
    pass


def words_remaining_for_given_result(words, guess, result):
    """
    Return the words that would remain after the given guess and corresponding result.
    """
    correct_letters = set(guess[i] for i, spot in enumerate(result) if spot)
    incorrect_letters = list(set(guess) - correct_letters)

    # These are the words that can be ruled out based on the letters we know are correct.
    if correct_letters:
        deduced_from_correct_letters = LETTERS_IN_WORDS_MAPPING[''.join(sorted(correct_letters))]
    else:
        deduced_from_correct_letters = None

    # These are the words that can be ruled out based on the letters we know are incorrect.
    if incorrect_letters:
        deduced_from_incorrect_letters = LETTERS_NOT_IN_WORDS_MAPPING[incorrect_letters[0]]
        for letter in incorrect_letters[1:]:
            deduced_from_incorrect_letters = deduced_from_incorrect_letters.intersection(
                LETTERS_NOT_IN_WORDS_MAPPING[letter]
            )
    else:
        deduced_from_incorrect_letters = None

    if deduced_from_correct_letters is None:
        possible_words = deduced_from_incorrect_letters
    elif deduced_from_incorrect_letters is None:
        possible_words = deduced_from_correct_letters
    else:
        possible_words = deduced_from_correct_letters.intersection(deduced_from_incorrect_letters)

    possible_words = possible_words.intersection(words)

    return set(word for word in possible_words if result_of_guess(guess, word) == result)


def check_for_better_total(words, guess, current_best_total=None):
    """
    Calculate the total number of remaining words after the given guess, summed across all possible remaining words.
    Raise a `WorseAverage` exception if this number is larger than the current best total.
    Return the new total if it's lower.
    """
    # Maintain a mapping of results to the remaining words. There's no point recalculating all the words
    # that are ruled out by a result we've already calculated it for.
    result_to_remaining_words_cache = {}
    total = 0
    for answer in words:
        result = result_of_guess(guess=guess, answer=answer)
        remaining_words = result_to_remaining_words_cache.get(result)
        if remaining_words is None:
            remaining_words = words_remaining_for_given_result(words=words, guess=guess, result=result)
            result_to_remaining_words_cache[result] = remaining_words
        total += len(remaining_words)
        if current_best_total and total > current_best_total:
            raise WorseTotal()
    return total


def find_best_next_guess(words):
    """
    Given a list of remaining possible answers, find the best guess to narrow this list down, based on the number
    of remaining words after the guess, summed across all possible answers.
    """
    if len(words) <= 2:
        return next(iter(words))

    best_guess, best_total = None, maxsize
    for i, guess in enumerate(WORDS):
        if i == 5000:
            print(f'Deep search required for: {words}')
        try:
            total = check_for_better_total(words=words, guess=guess, current_best_total=best_total)
        except WorseTotal:
            pass
        else:
            best_guess = guess
            best_total = total
            # If the total is equal to the length of possible answers, then this guess guarantees the word can be found
            # next round (if it hasn't been found already). The only way we can improve on this is by finding a guess
            # that meets this condition whilst also being in the list of remaining possible answers - so that this
            # guess has a chance of being correct.
            if best_total == len(words):
                for remaining_word in words:
                    if check_for_better_total(words=words, guess=remaining_word) == len(words):
                        best_guess = remaining_word
                        break
                break
    return best_guess
