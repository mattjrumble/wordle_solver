from sys import maxsize

from wordle_solver import WORDS, result_of_guess
from wordle_solver.strategy_3 import BEST_SECOND_GUESSES_FILENAME, BEST_FIRST_GUESS
from wordle_solver.strategy_3.compute_best_first_guess import words_remaining_for_given_result


class WorseTotal(Exception):
    pass


def check_for_better_total(words_after_first_guess, second_guess, current_best_total=None):
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
        if current_best_total and total > current_best_total:
            raise WorseTotal()
    return total


def main():
    """
    For each possible result following the first guess, determine which second guess results in the lowest average
    number of remaining possible words. Store this mapping of {result -> best second guess} in a file.
    """
    possible_results = sorted(set(result_of_guess(guess=BEST_FIRST_GUESS, answer=word) for word in WORDS))
    possible_results.remove((2, 2, 2, 2, 2))  # If the first guess was correct, there is no second guess.
    for result in possible_results:
        print(f'Calculating for result: {result}')
        words_after_first_guess = words_remaining_for_given_result(guess=BEST_FIRST_GUESS, result=result)
        best_second_guess, best_total = None, maxsize
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
                # can be found next round (if it hasn't been found already). The only way we can improve on this is
                # by finding a second guess meets this condition whilst also being in the list of remaining possible
                # words - so that this second guess has a chance of being correct.
                if best_total == len(words_after_first_guess):
                    for remaining_word in words_after_first_guess:
                        if check_for_better_total(
                            words_after_first_guess=words_after_first_guess, second_guess=remaining_word
                        ) == len(words_after_first_guess):
                            best_second_guess = remaining_word
                            break
                    break

        print(
            f'{result} - Best second guess is {best_second_guess} '
            f'with {best_total / len(words_after_first_guess)} average remaining words '
            f'(down from {len(words_after_first_guess)}).'
        )
        with open(BEST_SECOND_GUESSES_FILENAME, 'a') as fd:
            fd.write(f'{"".join(str(x) for x in result)} {best_second_guess}\n')


if __name__ == '__main__':
    main()
