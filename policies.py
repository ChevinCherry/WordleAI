import sys
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
        for index, letter in enumerate(word):
            if letter in letterCounts[index]:
                score += letterCounts[index][letter]
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

def wordsEqualUntilIndex(word1, word2, index):
    for i in range(index+1):
        if word1[i] != word2[i]:
            return False
    return True

def getExpectedValues(expectedValues, numValidWords, remainingWords, allWords, wordIndex, charIndex):
    if (charIndex > 4):
        numRemaining = len(remainingWords)
        if numRemaining == 1 and allWords[wordIndex][0] == remainingWords[0]:
            return wordIndex + 1
        raritySum = sum([1-wordFreq[1] for wordFreq in remainingWords])
        expectedValues[wordIndex] += raritySum*numRemaining / numValidWords
        return wordIndex + 1

    curWord = allWords[wordIndex][0]
    

    if len(remainingWords) == 0:
        newWordIndex = wordIndex
        while wordsEqualUntilIndex(curWord, allWords[newWordIndex][0], charIndex): 
            newWordIndex += 1
            if newWordIndex >= len(allWords):
                break
        return newWordIndex
    
    curChar = curWord[charIndex]
    # Correct case
    correctWords = [word for word in remainingWords if word[0][charIndex] == curChar]

    # Incorrect case
    incorrectWords = [word for word in remainingWords if curChar not in word[0]]

    # Wrong place case
    wrongPlaceWords = [word for word in remainingWords if word not in correctWords and word not in incorrectWords]

    newWordIndex = wordIndex
    while wordsEqualUntilIndex(curWord, allWords[newWordIndex][0], charIndex):
        wi1 = getExpectedValues(expectedValues, numValidWords, correctWords, allWords, newWordIndex, charIndex+1)
        wi2 = getExpectedValues(expectedValues, numValidWords, incorrectWords, allWords, newWordIndex, charIndex+1)
        newWordIndex = getExpectedValues(expectedValues, numValidWords, wrongPlaceWords, allWords, newWordIndex, charIndex+1)
        if newWordIndex >= len(allWords):
                break
    
    return newWordIndex

def scoreWordsByExpectedValue(allWords, validWords, guessNum):
    if len(validWords) == 1:
        return validWords[0][0]
    if guessNum == 0:
        # First guess probabilities are always the same, so to save time I use a precalculated "best" word
        return "lares"
    if guessNum >= 2:
        print(validWords)
        maxWord = validWords[0][0]
        maxFreq = validWords[0][1]
        for wordFreq in validWords:
            if wordFreq[1] > maxFreq:
                maxWord = wordFreq[0]
                maxFreq = wordFreq[1]
        return maxWord
    expectedValues = [0.0] * len(allWords)
    wordIndex = 0
    start = "\rLet me think... - ["
    letterString = ""
    while wordIndex < len(allWords):
        letterString += allWords[wordIndex][0][0]
        spaces = " " * (26 - len(letterString))
        print(start, letterString, spaces, end='] - ', sep='')
        wordIndex = getExpectedValues(expectedValues, len(validWords), validWords, allWords, wordIndex, 0)
    # We round here to account for computer precision error
    for i in range(len(expectedValues)):
        expectedValues[i] = round(expectedValues[i], 10)
    minExpected = min(expectedValues)
    minWords = [word for index, word in enumerate(allWords) if expectedValues[index] == minExpected]
    print(minWords)
    print(minExpected)
    return minWords[0][0]