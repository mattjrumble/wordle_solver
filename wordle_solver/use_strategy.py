from argparse import ArgumentParser
from re import match

from wordle_solver import ImpossibleResult
from wordle_solver.strategy_1 import Strategy as Strategy1
from wordle_solver.strategy_2 import Strategy as Strategy2
from wordle_solver.strategy_3 import Strategy as Strategy3


STRATEGIES = {
    1: Strategy1,
    2: Strategy2,
    3: Strategy3
}


def use_strategy(strategy):
    while True:
        guess = strategy.get_guess()
        if len(strategy.possible_words) == 1:
            print(f'The answer is {guess}.')
            break
        else:
            result = input(f'The best guess is {guess}. Enter the result of this guess: ')
            while not match(r'^[0-2]{5}$', result):
                result = input(f'Invalid result. Must be in the form XXXXX, where X is 0, 1 or 2. Try again: ')
            strategy.receive_result_of_last_guess(tuple(int(x) for x in result))


def main():
    parser = ArgumentParser()
    parser.add_argument('strategy', type=int)
    strategy_number = parser.parse_args().strategy
    try:
        strategy = STRATEGIES[strategy_number]()
    except KeyError:
        raise Exception(f'Invalid strategy: {strategy_number}')
    else:
        print(
            "------------------------------------\n"
            "This script provides the strategy's best guess. After each guess, "
            "enter the result in the form XXXXX, where:\n"
            "    0 = incorrect letter\n"
            "    1 = incorrect spot\n"
            "    2 = correct spot\n"
            "------------------------------------"
        )
        try:
            use_strategy(strategy)
        except ImpossibleResult:
            print('Impossible result. Check that all the results provided were correct.')


if __name__ == '__main__':
    main()
