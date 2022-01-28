from simWordle import Wordle
import random

class WordleAI:

    def __init__(self, wordle: Wordle):
        self.wordle = wordle
        words = open("validWords.txt")
        self.validWords = words.readlines()
        words.close()

    def filterByLetter(self, word, state, letter, index):
        if state == "correct":
            return word[index] == letter
        if state == "wrongPlace":
            return letter in word and word[index] != letter
        if state == "incorrect":
            return letter not in word

    def filterValidWords(self, guess, states):
        for index, state in enumerate(states):
            self.validWords = [word for word in self.validWords if self.filterByLetter(word, state, guess[index], index)]

    def makeGuess(self):
        return random.choice(self.validWords).strip("\n")
        
    def play(self):
        guessNum = 0
        while guessNum < self.wordle.maxGuesses:
            AIguess = self.makeGuess()
            print(AIguess)
            states = self.wordle.makeGuess(AIguess)
            self.filterValidWords(AIguess, states)
            print(self.wordle.getColoredGuess(states, AIguess))
            guessNum += 1

AI = WordleAI(Wordle("tests", 6))
AI.play()
        