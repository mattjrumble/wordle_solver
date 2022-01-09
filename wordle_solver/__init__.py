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
