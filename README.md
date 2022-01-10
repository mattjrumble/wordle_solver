## Wordle Solver

[Wordle](https://www.powerlanguage.co.uk/wordle/) is a game where you have to guess a 5-letter word in a similar manner
as the guess-the-color game Mastermind. After guessing a five-letter word, the game tells you whether any of your
letters are in the secret word and whether they are in the correct place.

This is my attempt at coding some different strategies for the game and seeing how well they perform. Each strategy
is tested against every 5-letter word to calculate the expected number of guesses the strategy needs to correctly
guess a random 5-letter word. To test a particular strategy,
run `python wordle_solver/test_strategy.py <STRATEGY_NUMBER>`.

### Strategy 1

This strategy keeps track of every word that hasn't been ruled out yet, in alphabetical order. It picks the first word
from this list, then updates the list based on the result of the guess. This repeats until the word is found.

This strategy takes **5.530** guesses on average. The worst word for this strategy is `ZILLS`, which takes 18 guesses to
get.

### Strategy 2

This strategy improves on Strategy 1 by picking the "best" word from the list of possible words, rather than the first
word. The "best" word is based on a heuristic scoring of how common each unique letter in the word is.

This strategy takes **4.951** guesses on average. The worst words for this strategy are `[SALES, SANGS, SILLS]`,
which take 15 guesses to get.

### Strategy 3 (WIP)

This strategy involves a few pre-calculations.

First we pre-calculate the "best" first guess, where the best first guess is defined as the one that results in the
lowest number of remaining possible words, when averaged across all possible answers. The code for this pre-calculation
is in `wordle_solver/strategy_3/compute_best_first_guess.py` and the best first guess is `LARES`.

Then we pre-calculate the "best" second guess, for every possible result that might come from the first guess (`LARES`).
The code for this pre-calculation is in `wordle_solver/strategy_3/compute_best_second_guess.py`, and this outputs
a mapping of `{result from first guess -> best second guess}` into a text file.

The strategy then uses these pre-calculations for the first two guesses. After the first two guesses, it acts like
Strategy 2.

This strategy takes **4.535** guesses on average. The worst word for this strategy is `SILLS`, which takes 16 guesses
to get.
