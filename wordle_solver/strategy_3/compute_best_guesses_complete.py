from collections.abc import MutableMapping
from copy import copy
from os.path import join

from wordle_solver import result_of_guess, WORDS
from wordle_solver.strategy_3 import words_remaining_for_given_result, find_best_next_guess

BEST_FIRST_GUESS = 'LARES'
BEST_SECOND_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_second_guesses.txt')
BEST_THIRD_GUESSES_FILENAME = join('wordle_solver', 'strategy_3', 'best_third_guesses.txt')
BEST_GUESSES_COMPLETE_FILENAME = join('wordle_solver', 'strategy_3', 'best_guesses_complete.txt')


def load_best_second_guess_mapping():
    mapping = {}
    with open(BEST_SECOND_GUESSES_FILENAME) as fd:
        for line in fd.readlines():
            _, first_result_string, second_guess = line.strip().split(' ')
            first_result = tuple(int(x) for x in first_result_string)
            mapping[first_result] = second_guess
    return mapping


def load_best_third_guess_mapping():
    mapping = {}
    with open(BEST_THIRD_GUESSES_FILENAME) as fd:
        for line in fd.readlines():
            _, first_result_string, _, second_result_string, third_guess = line.strip().split(' ')
            first_result = tuple(int(x) for x in first_result_string)
            second_result = tuple(int(x) for x in second_result_string)
            if first_result in mapping:
                mapping[first_result][second_result] = third_guess
            else:
                mapping[first_result] = {second_result: third_guess}
    return mapping


BEST_SECOND_GUESS_MAPPING = load_best_second_guess_mapping()
BEST_THIRD_GUESS_MAPPING = load_best_third_guess_mapping()


def generate_mapping(previous_guesses_and_results, words_remaining, depth):
    depth += 1

    if len(words_remaining) == 1:
        answer = next(iter(words_remaining))
        return {answer: {(2, 2, 2, 2, 2): answer}}

    if depth == 1:
        guess = BEST_FIRST_GUESS
    elif depth == 2:
        guess = BEST_SECOND_GUESS_MAPPING[previous_guesses_and_results[1]]
    elif depth == 3:
        guess = BEST_THIRD_GUESS_MAPPING[previous_guesses_and_results[1]][previous_guesses_and_results[3]]
    else:
        guess = find_best_next_guess(words_remaining)
    mapping = {guess: {}}
    results = sorted(set(result_of_guess(guess=guess, answer=answer) for answer in words_remaining))

    if depth == 3:
        print(f'Solving for {previous_guesses_and_results + [guess]}...')

    for result in results:
        if result == (2, 2, 2, 2, 2):
            mapping[guess][result] = guess
        else:
            new_words_remaining = words_remaining_for_given_result(words=words_remaining, guess=guess, result=result)
            new_previous_guesses_and_results = copy(previous_guesses_and_results)
            new_previous_guesses_and_results.extend((guess, result))
            mapping[guess][result] = generate_mapping(new_previous_guesses_and_results, new_words_remaining, depth)
    return mapping


def flatten(d, parent_key=''):
    """
    Flatten a nested dictionary into a list of lines, where each line has the form 'key key key ... value'.
    """
    items = []
    for k, v in d.items():
        new_key = f'{parent_key} {k}' if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key))
        else:
            items.append(f'{new_key} {v}')
    return items


def main():
    mapping = generate_mapping(
        previous_guesses_and_results=[],
        words_remaining=WORDS,
        depth=0
    )
    lines = flatten(mapping)
    with open(BEST_GUESSES_COMPLETE_FILENAME, 'w') as fd:
        fd.writelines((f'{line}\n' for line in lines))


if __name__ == '__main__':
    main()
