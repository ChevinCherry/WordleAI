from simWordle import LetterStates
from utils import filterValidWords

### WORD SCORING POLICIES ###
def singleWordPolicy(allWords, validWords, guessNum):
    return "tests"

def scoreWordsByLetterPlacementFrequency(allWords, validWords, guessNum):
    if len(validWords) == 1:
        return validWords[0]
    letterCounts = [{}, {}, {}, {}, {}]
    for word in validWords:
        for index, letter in enumerate(word):
            if letter in letterCounts[index]:
                letterCounts[index][letter] += 1
            else:
                letterCounts[index][letter] = 1
    def key(word):
        score = 0
        seen = []
        for index, letter in enumerate(word):
            if letter not in seen and letter in letterCounts[index]:
                score += letterCounts[index][letter]
                seen.append(letter)
        return score
    return max(validWords, key=key)
    
def scoreWordsByLetterFrequency(allWords, validWords, guessNum):
    if len(validWords) == 1:
        return validWords[0]
    letterCounts = {}
    for word in validWords:
        for letter in word:
            if letter in letterCounts:
                letterCounts[letter] += 1
            else:
                letterCounts[letter] = 1
    def key(word):
        score = 0
        seen = []
        for letter in word:
            if letter not in seen and letter in letterCounts:
                score += letterCounts[letter]
                seen.append(letter)
        return score
    return max(validWords, key=key)

def generateAllPossibleStates(ofLength):
    if ofLength == 0:
        return [[]]
    statesOfLowerLength = generateAllPossibleStates(ofLength-1)
    stateList = []
    for lowerState in statesOfLowerLength:
        for addState in LetterStates:
            stateList.append(lowerState + [addState])
    return stateList

allStates = generateAllPossibleStates(5)

def wordsEqualUntilIndex(word1, word2, index):
    for i in range(index+1):
        if word1[i] != word2[i]:
            return False
    return True

def getExpectedValues(expectedValues, numValidWords, remainingWords, allWords, wordIndex, charIndex):
    if (charIndex > 4):
        numRemaining = len(remainingWords)
        expectedValues[wordIndex] += numRemaining*numRemaining / numValidWords
        return wordIndex + 1

    curWord = allWords[wordIndex]
    

    if len(remainingWords) == 0:
        newWordIndex = wordIndex
        while wordsEqualUntilIndex(curWord, allWords[newWordIndex], charIndex): 
            newWordIndex += 1
            if newWordIndex >= len(allWords):
                break
        return newWordIndex
    
    curChar = curWord[charIndex]
    # Correct case
    correctWords = [word for word in remainingWords if word[charIndex] == curChar]

    # Incorrect case
    incorrectWords = [word for word in remainingWords if curChar not in word]

    # Wrong place case
    wrongPlaceWords = [word for word in remainingWords if word not in correctWords and word not in incorrectWords]

    newWordIndex = wordIndex
    while wordsEqualUntilIndex(curWord, allWords[newWordIndex], charIndex):
        wi1 = getExpectedValues(expectedValues, numValidWords, correctWords, allWords, newWordIndex, charIndex+1)
        wi2 = getExpectedValues(expectedValues, numValidWords, incorrectWords, allWords, newWordIndex, charIndex+1)
        newWordIndex = getExpectedValues(expectedValues, numValidWords, wrongPlaceWords, allWords, newWordIndex, charIndex+1)
        if newWordIndex >= len(allWords):
                break
    
    return newWordIndex

def scoreWordsByExpectedValue(allWords, validWords, guessNum):
    if len(validWords) == 1:
        return validWords[0]
    if guessNum == 0:
        return "raise"
    expectedValues = [0.0] * len(allWords)
    wordIndex = 0
    while wordIndex < len(allWords):
        print(allWords[wordIndex][0])
        wordIndex = getExpectedValues(expectedValues, len(validWords), validWords, allWords, wordIndex, 0)
    minExpected = min(expectedValues)
    allMinWords = [word for index, word in enumerate(allWords) if expectedValues[index] == minExpected]
    print(allMinWords)
    validMinWords = [word for word in allMinWords if word in validWords]
    print(validMinWords)
    selection = ""
    if len(validMinWords) > 0:
        selection = validMinWords[0]
    else:
        selection = allMinWords[0]
    return selection