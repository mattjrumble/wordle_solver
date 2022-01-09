from argparse import ArgumentParser
from time import time

from wordle_solver import WORDS, result_of_guess
from wordle_solver.strategy_1 import Strategy as Strategy1
from wordle_solver.strategy_2 import Strategy as Strategy2


STRATEGIES = {
    1: Strategy1,
    2: Strategy2
}


def test_strategy_for_given_answer(strategy_cls, answer):
    """
    Return the number of guesses it takes the strategy to get the correct answer, for a given answer.
    """
    guess, guess_count = None, 0
    strategy = strategy_cls()
    while guess != answer:
        guess = strategy.get_guess()
        guess_count += 1
        strategy.receive_result_of_last_guess(result_of_guess(guess=guess, answer=answer))
    return guess_count


def test_strategy(strategy_cls):
    """
    Print the expected number of guesses it takes the strategy to get the correct answer, across all possible answers.
    Also print the worst possible word(s) for the given strategy.
    """
    start = time()
    total = 0
    worst_words, worst_guess_count = [], 0

    for word in WORDS:
        guess_count = test_strategy_for_given_answer(strategy_cls, word)
        total += guess_count
        print(f'{word} - {guess_count}')

        if guess_count > worst_guess_count:
            worst_guess_count = guess_count
            worst_words = [word]
        elif guess_count == worst_guess_count:
            worst_words.append(word)

    print(
        f"This strategy takes {round(total / len(WORDS), 3)} guesses on average.\n"
        f"The worst word(s) for this strategy are '{worst_words}', which take {worst_guess_count} guesses to get."
    )
    end = time()
    print(f'Time taken: {end-start}')


def main():
    parser = ArgumentParser()
    parser.add_argument('strategy', type=int)
    strategy_number = parser.parse_args().strategy
    try:
        strategy_cls = STRATEGIES[strategy_number]
    except KeyError:
        raise Exception(f'Invalid strategy: {strategy_number}')
    else:
        test_strategy(strategy_cls)


if __name__ == '__main__':
    main()
