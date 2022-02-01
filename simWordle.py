
import random
from termcolor import colored
from utils import checkWrongPlace

LetterStates = ["correct", "wrongPlace", "incorrect"]
StateToColor = {"correct": "green", "wrongPlace": "yellow", "incorrect": "white"}

class Wordle:

    def __init__(self, wordle, maxGuesses):
        
        self.validWords = open('validWords.txt').read().splitlines()
        if wordle not in self.validWords:
            raise "Invalid Wordle choice!"
        self.wordle = wordle
        self.guessNum = 0
        self.maxGuesses = maxGuesses
        self.win = False
    
    def validWord(self, word: str):
        return word in self.validWords
        
    
    def getColoredGuess(self, states, guess):
        string = ""
        for index, state in enumerate(states):
            string += colored(guess[index], StateToColor[state])
        return string
    
    def makeGuess(self, guess):
        if (self.guessNum >= self.maxGuesses):
            raise "Cannot make guess! Game is over."
        if not self.validWord(guess):
            raise "Invalid guess!"
        validity: list[str] = [None] * 5
        for index, letter in enumerate(guess):
            if letter == self.wordle[index]:
                validity[index] = "correct"
            elif checkWrongPlace(self.wordle, guess, letter, index):
                validity[index] = "wrongPlace"
            else:
                validity[index] = "incorrect"
        self.guessNum += 1
        self.win = all([valid=="correct" for valid in validity])
        return validity
    
    def checkForWin(self):
        return self.win

if (__name__ == "__main__"):
    maxGuesses = 6
    allWords = open("validWords.txt").readlines()
    wordle = random.choice(allWords).strip("\n")
    game = Wordle("sloth", maxGuesses)
    guessNum = 0
    win = False
    while guessNum < maxGuesses and not game.checkForWin():
        validGuess = False
        while not validGuess:
            print("Enter guess:")
            guess = input()
            validGuess = game.validWord(guess)
            if not validGuess:
                print("Invalid.")
        states = game.makeGuess(guess)
        print(game.getColoredGuess(states, guess))
        guessNum += 1
    print(game.checkForWin())
    print(game.wordle)



