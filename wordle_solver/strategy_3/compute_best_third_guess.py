from os.path import join, exists

from wordle_solver import result_of_guess, filter_words, WORDS
from wordle_solver.strategy_3 import words_remaining_for_given_result, find_best_next_guess

BEST_SECOND_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_second_guesses.txt')
BEST_THIRD_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_third_guesses.txt')


def load_best_second_guess_mapping():
    mapping = []
    with open(BEST_SECOND_GUESSES_FILENAME) as fd:
        for line in fd.readlines():
            first_guess, first_result_string, second_guess = line.strip().split(' ')
            first_result = tuple(int(x) for x in first_result_string)
            mapping.append((first_guess, first_result, second_guess))
    return mapping


BEST_SECOND_GUESS_MAPPING = load_best_second_guess_mapping()


def output_to_file(first_guess, first_result, second_guess, second_result, third_guess):
    first_result_string = ''.join(str(x) for x in first_result)
    second_result_string = ''.join(str(x) for x in second_result)
    with open(BEST_THIRD_GUESSES_FILENAME, 'a') as fd:
        fd.write(f'{first_guess} {first_result_string} {second_guess} {second_result_string} {third_guess}\n')


def main():
    """
    For each possible result following each best second guess, determine which third guess results in the lowest
    average number of remaining possible words. Store this mapping in a file. This computation takes a while, so this
    method is resumable.
    """
    if exists(BEST_THIRD_GUESSES_FILENAME):
        with open(BEST_THIRD_GUESSES_FILENAME) as fd:
            last_line = fd.readlines()[-1].strip()
            _, resumed_first_result_string, _, resumed_second_result_string, _ = last_line.split(' ')
            resumed_first_result = tuple(int(x) for x in resumed_first_result_string)
            resumed_second_result = tuple(int(x) for x in resumed_second_result_string)
    else:
        resumed_first_result = None
        resumed_second_result = None

    for first_guess, first_result, second_guess in BEST_SECOND_GUESS_MAPPING:

        if resumed_first_result and first_result < resumed_first_result:
            continue
        else:
            resumed_first_result = None

        words_after_first_guess = words_remaining_for_given_result(words=WORDS, guess=first_guess, result=first_result)
        possible_second_results = sorted(set(
            result_of_guess(guess=second_guess, answer=answer) for answer in words_after_first_guess
        ))
        # If the second guess was correct, there is no third guess.
        if (2, 2, 2, 2, 2) in possible_second_results:
            possible_second_results.remove((2, 2, 2, 2, 2))

        for second_result in possible_second_results:

            if resumed_second_result and second_result <= resumed_second_result:
                continue
            else:
                resumed_second_result = None

            print(f'Calculating for results: {first_result} and {second_result}')
            words_after_second_guess = set(filter_words(
                words=words_after_first_guess, guess=second_guess, result=second_result
            ))
            best_third_guess = find_best_next_guess(words=words_after_second_guess)
            output_to_file(first_guess, first_result, second_guess, second_result, best_third_guess)


if __name__ == '__main__':
    main()
