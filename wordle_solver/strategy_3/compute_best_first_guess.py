from sys import maxsize

from wordle_solver import WORDS, result_of_guess
from wordle_solver.strategy_3 import words_remaining_for_given_result


class WorseTotal(Exception):
    pass


def check_for_better_total(first_guess, current_best_total):
    """
    Calculate the total number of remaining words after the given first guess, summed across all possible answers.
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
            count = len(words_remaining_for_given_result(guess=first_guess, result=result))
            result_to_count_cache[result] = count
        total += count
        if total > current_best_total:
            raise WorseTotal()
    return total


def main():
    """
    Determine which first guess results in the lowest average number of remaining possible words.
    """
    best_first_guess, best_total = None, maxsize
    for word in WORDS:
        try:
            total = check_for_better_total(first_guess=word, current_best_total=best_total)
        except WorseTotal:
            pass
        else:
            best_first_guess = word
            best_total = total
        print(f'{word} - Current best is {best_first_guess} with {best_total / len(WORDS)} average remaining words.')


if __name__ == '__main__':
    main()
