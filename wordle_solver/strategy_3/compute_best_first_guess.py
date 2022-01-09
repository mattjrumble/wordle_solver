from collections import defaultdict
from itertools import combinations
from string import ascii_uppercase

from wordle_solver import WORDS, result_of_guess


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


def words_remaining_for_given_result(first_guess, result):
    """
    Return the number of words that would remain after the given first guess and corresponding result.
    """
    correct_letters = set(first_guess[i] for i, spot in enumerate(result) if spot)
    incorrect_letters = list(set(first_guess) - correct_letters)

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

    return sum(result_of_guess(first_guess, word) == result for word in possible_words)


class WorseTotal(Exception):
    pass


def check_for_better_total(first_guess, current_best_total):
    """
    Calculate the total number of remaining words after the given first guess, summed across all possible words.
    Raise a `WorseAverage` exception if this number is larger than the current best total.
    Return the new total if it's lower.
    """
    # Maintain a mapping of results to the number of remaining words. There's no point recalculating all the words
    # that are ruled out by a result we've already calculated it for.
    result_to_count_cache = {}
    total = 0
    for answer in WORDS:
        result = result_of_guess(guess=first_guess, answer=answer)
        count = result_to_count_cache.get(result)
        if count is None:
            count = words_remaining_for_given_result(first_guess=first_guess, result=result)
            result_to_count_cache[result] = count
        total += count
        if total > current_best_total:
            raise WorseTotal()
    return total


def main():
    """
    Determine which first guess results in the lowest average number of remaining possible words.
    """
    best_word, best_total = None, 99999999999999999
    for word in WORDS:
        try:
            total = check_for_better_total(first_guess=word, current_best_total=best_total)
        except WorseTotal:
            pass
        else:
            best_word = word
            best_total = total
        print(
            f'{word} - Best first guess so far is {best_word} with an '
            f'average of {best_total / len(WORDS)} remaining words.'
        )


if __name__ == '__main__':
    main()
