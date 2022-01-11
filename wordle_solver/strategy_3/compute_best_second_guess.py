from os.path import join

from wordle_solver import WORDS, result_of_guess
from wordle_solver.strategy_3 import words_remaining_for_given_result, find_best_next_guess


BEST_FIRST_GUESS = 'LARES'
BEST_SECOND_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_second_guesses.txt')


def main():
    """
    For each possible result following the first guess, determine which second guess results in the lowest average
    number of remaining possible words. Store this mapping in a file.
    """
    possible_results = sorted(set(result_of_guess(guess=BEST_FIRST_GUESS, answer=word) for word in WORDS))
    possible_results.remove((2, 2, 2, 2, 2))  # If the first guess was correct, there is no second guess.
    for result in possible_results:
        print(f'Calculating for result: {result}')
        words_after_first_guess = words_remaining_for_given_result(words=WORDS, guess=BEST_FIRST_GUESS, result=result)
        best_second_guess = find_best_next_guess(words=words_after_first_guess)
        with open(BEST_SECOND_GUESSES_FILENAME, 'a') as fd:
            fd.write(f'{BEST_FIRST_GUESS} {"".join(str(x) for x in result)} {best_second_guess}\n')


if __name__ == '__main__':
    main()
