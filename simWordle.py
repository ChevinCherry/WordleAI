
import random
from termcolor import colored
from processWords import validWord

StateToColor = {"correct": "green", "wrongPlace": "yellow", "incorrect": "white"}

class Wordle:

    def __init__(self, wordle, maxGuesses):
        self.wordle = wordle
        self.guessNum = 0
        self.maxGuesses = maxGuesses
        self.win = False
    
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
    
    def getColoredGuess(self, states, guess):
        string = ""
        for index, state in enumerate(states):
            string += colored(guess[index], StateToColor[state])
        return string

    def __checkWrongPlace(self, guess, letter):
        if letter not in self.wordle:
            return False
        appearances = 0
        correctGuesses = 0
        for index, gLetter in enumerate(guess):
            if self.wordle[index] == letter:
                appearances += 1
                if gLetter == letter:
                    correctGuesses += 1
        return appearances > correctGuesses
    
    def makeGuess(self, guess):
        if (self.guessNum >= self.maxGuesses):
            raise "Cannot make guess! Game is over."
        if not validWord(guess):
            raise "Invalid guess!"
        validity: list[str] = [None] * 5
        for index, letter in enumerate(guess):
            if letter == self.wordle[index]:
                validity[index] = "correct"
            elif self.__checkWrongPlace(guess, letter):
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
    wordle = random.choice(allWords)
    game = Wordle(wordle, maxGuesses)
    guessNum = 0
    win = False
    while guessNum < maxGuesses and not game.checkForWin():
        validGuess = False
        while not validGuess:
            print("Enter guess:")
            guess = input()
            validGuess = validWord(guess)
            if not validGuess:
                print("Invalid.")
        states = game.makeGuess(guess)
        print(game.getColoredGuess(states, guess))
        guessNum += 1
    print(game.checkForWin())
    print(game.wordle)


