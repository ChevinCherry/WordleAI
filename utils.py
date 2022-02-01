from turtle import st


def checkWrongPlace(answer, guess, letter, upToChar):
    if letter not in answer:
        return False
    numBothMatch = 0
    numGuessMatch = 0
    numAnswerMatch = 0
    numCurGuessMatch = 0
    for index, gLetter in enumerate(guess):
        guessMatch = gLetter == letter
        answerMatch = answer[index] == letter
        if guessMatch and answerMatch:
            numBothMatch += 1
        if answerMatch:
            numAnswerMatch += 1
        if guessMatch:
            numGuessMatch += 1
            if index <= upToChar:
                numCurGuessMatch += 1

    return numGuessMatch > numBothMatch and not numCurGuessMatch > numAnswerMatch

def getStatesForGuess(answer, guess):     
    states: list[str] = [None] * 5
    for index, letter in enumerate(guess):
        if letter == answer[index]:
            states[index] = "correct"
        elif checkWrongPlace(answer, guess, letter, index):
            states[index] = "wrongPlace"
        else:
            states[index] = "incorrect"
    return states

def statesAreEqual(stateList1, stateList2):
    if len(stateList1) != len(stateList2):
        return False
    for index, state in enumerate(stateList1):
        if state != stateList2[index]:
            return False
    return True


def filterValidWords(validWordList, guess, states):
    validWords = [word for word in validWordList if statesAreEqual(getStatesForGuess(word, guess), states)]
    return validWords
    