## Wordle Solver  
  
[Wordle](https://www.powerlanguage.co.uk/wordle/) is a game where you have to guess a 5-letter word in a similar manner  
as the guess-the-color game Mastermind. After guessing a five-letter word, the game tells you whether any of your  
letters are in the secret word and whether they are in the correct place.  
  
This is my attempt at coding some different strategies for the game and seeing how well they perform. Each strategy  
is tested against every 5-letter word to calculate the expected number of guesses the strategy needs to correctly  
guess a random 5-letter word. To test a particular strategy,  
run `python wordle_solver/test_strategy.py <STRATEGY_NUMBER>`.  
  
### Strategy 1  
  
* Average guesses needed: 5.530  
* Worst word for this strategy: ZILLS (18 guesses needed)
  
This strategy keeps track of every word that hasn't been ruled out yet, in alphabetical order. It picks the first word  
from this list, then updates the list based on the result of the guess. This repeats until the word is found.  
  
### Strategy 2  
  
* Average guesses needed: 4.951  
* Worst words for this strategy: SALES, SANGS, SILLS (15 guesses needed)
  
This strategy improves on Strategy 1 by picking the "best" word from the list of possible words, rather than the first  
word. The "best" word is based on a heuristic scoring of how common each unique letter in the word is.  
  
### Strategy 3 (WIP)

* Average guesses needed: 4.378  
* Worst word for this strategy: ZILLS (15 guesses needed)  
  
This strategy involves a few pre-calculations. First we pre-calculate the "best" first guess, where the best first guess
is defined as the one that results in the lowest number of remaining possible words, when averaged across all possible
answers. The code for this pre-calculation is in `wordle_solver/strategy_3/compute_best_first_guess.py` and the best
first guess is `LARES`.  
  
Then we pre-calculate the "best" second guess, for every possible result that might come from the first guess (`LARES`).  
The code for this pre-calculation is in `wordle_solver/strategy_3/compute_best_second_guess.py`, and this outputs  
a mapping of `{best first guess -> result from first guess -> best second guess}` into
`wordle_solver/strategy_3/best_second_guesses.txt`.  
  
The strategy uses these pre-calculations for the first two guesses. After the first two guesses, it always picks  
the word from the list of remaining possible answers that gives the lower number of remaining possible words, when  
averaged across all remaining possible answers.
