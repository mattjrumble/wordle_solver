from os.path import join

from wordle_solver import WORDS, result_of_guess
from wordle_solver.strategy_3.compute_best_first_guess import words_remaining_for_given_result


#  We know that 'LARES' is the best first guess, thanks to `compute_best_first_guess.py`.
FIRST_GUESS = 'LARES'
OUTPUT_FILENAME = join('wordle_solver', 'strategy_3', 'best_second_guesses.txt')


class WorseTotal(Exception):
    pass


def check_for_better_total(words_after_first_guess, second_guess, current_best_total):
    """
    Calculate the total number of remaining words after the given second guess, summed across all possible answers.
    Raise a `WorseAverage` exception if this number is larger than the current best total.
    Return the new total if it's lower.
    """
    # Maintain a mapping of results to the remaining words. There's no point recalculating all the words
    # that are ruled out by a result we've already calculated it for.
    result_to_remaining_words_cache = {}
    total = 0
    for answer in words_after_first_guess:
        result = result_of_guess(guess=second_guess, answer=answer)
        new_remaining_words = result_to_remaining_words_cache.get(result)
        if new_remaining_words is None:
            new_remaining_words = words_remaining_for_given_result(guess=second_guess, result=result)
            result_to_remaining_words_cache[result] = new_remaining_words
        total += len(words_after_first_guess.intersection(new_remaining_words))
        if total > current_best_total:
            raise WorseTotal()
    return total


def main():
    """
    For each possible result following the first guess, determine which second guess results in the lowest average
    number of remaining possible words. Store this mapping of {result -> best second guess} in a file.
    """
    possible_results = sorted(set(result_of_guess(guess=FIRST_GUESS, answer=word) for word in WORDS))
    for result in possible_results[9:]:
        print(f'Calculating for result: {result}')
        words_after_first_guess = words_remaining_for_given_result(guess=FIRST_GUESS, result=result)
        best_second_guess, best_total = None, 99999999999999999
        for i, word in enumerate(WORDS):
            if i % 1000 == 0:
                print(f'{i} / {len(WORDS)}')
            try:
                total = check_for_better_total(
                    words_after_first_guess=words_after_first_guess,
                    second_guess=word,
                    current_best_total=best_total
                )
            except WorseTotal:
                pass
            else:
                best_second_guess = word
                best_total = total
                # If the total is equal to the length of possible answers, then this second guess guarantees the word
                # can be found next round (if it hasn't been found already). We can't do any better than this, so take
                # this word as the best second guess for this particular result.
                if best_total == len(words_after_first_guess):
                    break
        print(
            f'{result} - Best second guess is {best_second_guess} '
            f'with {best_total / len(words_after_first_guess)} average remaining words '
            f'(down from {len(words_after_first_guess)}).'
        )
        with open(OUTPUT_FILENAME, 'a') as fd:
            fd.write(f'{result} - {best_second_guess}\n')


if __name__ == '__main__':
    main()
