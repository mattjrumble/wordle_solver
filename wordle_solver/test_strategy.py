from wordle_solver import WORDS, result_of_guess
from wordle_solver.strategy_1 import Strategy


def test_strategy(strategy_cls, answer):
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


def expected_guess_count(strategy_cls):
    """
    Return the expected (average) number of guesses it takes the strategy to get the correct answer, across
    all possible answers.
    """
    total = 0
    worst_words, worst_guess_count = [], 0

    for word in WORDS:
        guess_count = test_strategy(strategy_cls, word)
        total += guess_count
        print(f'{word} - {guess_count}')

        if guess_count > worst_guess_count:
            worst_guess_count = guess_count
            worst_words = [word]
        elif guess_count == worst_guess_count:
            worst_words.append(word)

    print(f'Expected number of guesses: {total / len(WORDS)}')
    print(f'These are the worst words which took {worst_guess_count} guesses: {worst_words}')


if __name__ == '__main__':
    expected_guess_count(Strategy)
