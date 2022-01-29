from simWordle import Wordle
import random

### WORD SCORING POLICIES ###
def scoreWordsByLetterPlacementFrequency(words):
    letterCounts = [{}, {}, {}, {}, {}]
    for word in words:
        for index, letter in enumerate(word):
            if letter in letterCounts[index]:
                letterCounts[index][letter] += 1
            else:
                letterCounts[index][letter] = 1
    def fun(word):
        score = 0
        seen = []
        for index, letter in enumerate(word):
            if letter not in seen:
                score += letterCounts[index][letter]
                seen.append(letter)
        return score
    return fun
    
def scoreWordsByLetterFrequency(words):
    letterCounts = {}
    for word in words:
        for letter in word:
            if letter in letterCounts:
                letterCounts[letter] += 1
            else:
                letterCounts[letter] = 1
    def fun(word):
        score = 0
        seen = []
        for letter in word:
            if letter not in seen:
                score += letterCounts[letter]
                seen.append(letter)
        return score
    return fun

class WordleAI:

    def __init__(self, wordle: Wordle, policy):
        self.wordle = wordle
        self.policy = policy
        words = open("validWords.txt")
        self.validWords = words.read().splitlines()
        words.close()
    
    def __checkForIncorrect(self, word, letter, states):
        if letter not in word:
            return True
        for index, wLetter in enumerate(word):
            if wLetter == letter and states[index] != "correct":
                return False
        return True


    def filterByLetter(self, word, state, letter, index, states):
        if state == "correct":
            return word[index] == letter
        if state == "wrongPlace":
            return letter in word and word[index] != letter
        if state == "incorrect":
            return self.__checkForIncorrect(word, letter, states)

    def filterValidWords(self, guess, states):
        for index, state in enumerate(states):
            self.validWords = [word for word in self.validWords if self.filterByLetter(word, state, guess[index], index, states)]


    def makeGuess(self):
        bestWord = max(self.validWords, key=self.policy(self.validWords))
        return bestWord
        
    def play(self):
        guessNum = 0
        while guessNum < self.wordle.maxGuesses and not self.wordle.checkForWin():
            AIguess = self.makeGuess()
            print(AIguess)
            states = self.wordle.makeGuess(AIguess)
            self.filterValidWords(AIguess, states)
            print(self.wordle.getColoredGuess(states, AIguess))
            guessNum += 1

word = "stout"
AI1 = WordleAI(Wordle(word, 6), scoreWordsByLetterFrequency)
AI2 = WordleAI(Wordle(word, 6), scoreWordsByLetterPlacementFrequency)
AI1.play()
print("Win:", AI1.wordle.checkForWin(), "Guesses:", AI1.wordle.guessNum)
AI2.play()
print("Win:", AI2.wordle.checkForWin(), "Guesses:", AI2.wordle.guessNum)
        