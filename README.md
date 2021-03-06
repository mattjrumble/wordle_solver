## Wordle Solver
  
[Wordle](https://www.powerlanguage.co.uk/wordle/) is a game where you have to guess a 5-letter word in a similar manner
as the guess-the-color game Mastermind. After guessing a five-letter word, the game tells you whether any of your
letters are in the secret word and whether they are in the correct place. This project explores some different
strategies for the game.

To use a particular strategy, run `python wordle_solver/use_strategy.py <STRATEGY_NUMBER>`:

```
python wordle_solver/use_strategy.py 3
...
The best guess is LARES. Enter the result of this guess: 00000
The best guess is TONIC. Enter the result of this guess: 00200
The best guess is DYING. Enter the result of this guess: 01020
Remaining words: ['BUNNY', 'FUNNY', 'NUNNY', 'PUNNY']
The best guess is UPBYE. Enter the result of this guess: 10110
The answer is BUNNY.
```

To test a particular strategy, run `python wordle_solver/test_strategy.py <STRATEGY_NUMBER>`. Each strategy
is tested against every 5-letter word to calculate the expected number of guesses the strategy needs to correctly
guess a random 5-letter word, along with calculating the worst possible word(s) for the strategy.

### Strategy 1 (The Dumb Strategy)
  
* Average guesses needed: 5.530
* Worst word for this strategy: ZILLS (18 guesses needed)

This strategy keeps track of every word that hasn't been ruled out yet, in alphabetical order. It picks the first word
from this list, then updates the list based on the result of the guess. This repeats until the word is found.

### Strategy 2 (The Slightly Less Dumb Strategy)

* Average guesses needed: 4.951
* Worst words for this strategy: SALES, SANGS, SILLS (15 guesses needed)

This strategy improves on Strategy 1 by picking the "best" word from the list of possible words, rather than the first
word. The "best" word is based on a heuristic scoring of how common each unique letter in the word is.

### Strategy 3 (The Good Strategy)

* Average guesses needed: 4.111
* Worst word for this strategy: SILLS (8 guesses needed)

This strategy involves some pre-calculations to work out the "best" next guess from a given point in the game. The
"best" guess is defined as the one that results in the lowest number of remaining possible words, when averaged across
all possible answers.

1. `compute_best_first_guess.py` does this for the first guess. This calculates that the best first guess is `LARES`.
2. `compute_best_second_guess.py` does this for the second guess (assuming `LARES` as the first guess). It outputs
the mapping of `{best first guess -> result from first guess -> best second guess}` into `best_second_guesses.txt`.
3. `compute_best_third_guess.py` does this again for the third guess (using the mapping of best second guesses),
outputting the mapping of `{best first guess -> result from first guess -> best second guess -> result from second guess -> best third guess}`
to `best_third_guesses.txt`.
4. `compute_best_guesses_complete.py` does this for all remaining guesses (using the previous mappings), and combines
all the previous mapping files into one complete mapping of `{best guess -> result -> best guess -> etc}` in
`best_guesses_complete.txt`. 

The strategy then just uses the complete mapping stored in `best_guesses_complete.txt` to pick its next guess.
