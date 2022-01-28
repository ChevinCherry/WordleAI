words = open('words.txt')


def validWord(word: str):
    alphabetStart = ord('a')
    alphabetEnd = ord('z')
    if len(word) != 5:
        return False
    for letter in word:
        charCode = ord(letter)
        if charCode < alphabetStart or charCode > alphabetEnd:
            return False
    return True

validWords = open('validWords.txt', 'w')
for word in words:
    lowerWord = word.lower()
    if validWord(lowerWord.strip("\n")):
        validWords.write(lowerWord)