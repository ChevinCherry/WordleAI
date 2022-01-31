def checkForIncorrect(word, letter, states):
        if letter not in word:
            return True
        for index, wLetter in enumerate(word):
            if wLetter == letter and states[index] != "correct":
                return False
        return True

def filterByLetter(word, state, letter, index, states):
    if state == "correct":
        return word[index] == letter
    if state == "wrongPlace":
        return letter in word and word[index] != letter
    if state == "incorrect":
        return checkForIncorrect(word, letter, states)

def filterValidWords(validWordList, guess, states):
    validWords = validWordList
    for index, state in enumerate(states):
        validWords = [word for word in validWords if filterByLetter(word, state, guess[index], index, states)]
    return validWords