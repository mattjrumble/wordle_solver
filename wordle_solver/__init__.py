with open('../words.txt') as fd:
    WORDS = [line.strip() for line in fd.readlines()]


def result_of_guess(guess, answer):
    """
    Return a list of five integers representing the result of a guess.
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

    return result


def filter_words(words, guess, result):
    """
    Filter the list of words based on a guess result.
    """
    filtered_words = []
    for word in words:
        if result_of_guess(guess, word) == result:
            filtered_words.append(word)
    return filtered_words
