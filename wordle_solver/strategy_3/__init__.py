from collections import defaultdict
from itertools import combinations
from string import ascii_uppercase

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


def words_remaining_for_given_result(guess, result):
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

    return set(word for word in possible_words if result_of_guess(guess, word) == result)
