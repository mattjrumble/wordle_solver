with open('words.txt') as fd:
    WORDS = [line.strip() for line in fd.readlines()]


LETTER_FREQUENCIES = {
    'A': 5738, 'B': 1547, 'C': 1947, 'D': 2364, 'E': 6441, 'F': 1071, 'G': 1576, 'H': 1682, 'I': 3595, 'J': 270,
    'K': 1426, 'L': 3269, 'M': 1908, 'N': 2854, 'O': 4248, 'P': 1945, 'Q': 104, 'R': 4027, 'S': 6427, 'T': 3206,
    'U': 2399, 'V': 661, 'W': 1013, 'X': 268, 'Y': 1992, 'Z': 412
}


def result_of_guess(guess, answer):
    """
    Return a tuple of five integers representing the result of a guess.
    2 = Correct letter, correct spot.
    1 = Correct letter, wrong spot.
    0 = Wrong letter.
    """
    result = [None, None, None, None, None]
    remaining_letters = list(answer)

    # Mark the letters which are in the correct spot.
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            result[i] = 2
            remaining_letters.remove(letter)

    # Go through the remaining letters in the guess and check if that letter is still in the answer, after the letters
    # in the correct spot have been taken out.
    for i, letter in enumerate(guess):
        if result[i] is None:
            if letter in remaining_letters:
                result[i] = 1
                remaining_letters.remove(letter)
            else:
                result[i] = 0

    return tuple(result)


def filter_words(words, guess, result):
    """
    Filter the list of words based on a guess result.
    """
    # The naive approach is to loop through every word, get the result of the guess assuming that word is correct, and
    # checking if that result matches the given result. This can be made a little quicker by working out which letters
    # from the guess are correct and which are incorrect, checking for those letters in the list of words first, and
    # only then comparing the full results.
    correct_letters = set(guess[i] for i, spot in enumerate(result) if spot in (1, 2))
    incorrect_letters = set(guess) - correct_letters

    filtered_words = []
    for word in words:
        unique_letters = set(word)
        if any(letter in unique_letters for letter in incorrect_letters):
            continue
        if all(letter in unique_letters for letter in correct_letters):
            if result_of_guess(guess, word) == result:
                filtered_words.append(word)

    return filtered_words
