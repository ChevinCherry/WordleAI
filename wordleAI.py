from copy import deepcopy
from policies import scoreWordsByExpectedValue, scoreWordsByLetterFrequency, scoreWordsByLetterPlacementFrequency, singleWordPolicy
from simWordle import Wordle
from utils import filterValidWords

class WordleAI:

    def __init__(self, wordle: Wordle, policy):
        self.wordle = wordle
        self.policy = policy
        words = open("validWords.txt")
        self.validWords = words.read().splitlines()
        self.allWords = deepcopy(self.validWords)
        words.close()

    def makeGuess(self):
        return self.policy(self.allWords, self.validWords, self.wordle.guessNum)
        
    def play(self, output=True):
        guessNum = 0
        while guessNum < self.wordle.maxGuesses and not self.wordle.checkForWin():
            AIguess = self.makeGuess()
            states = self.wordle.makeGuess(AIguess)
            self.validWords = filterValidWords(self.validWords, AIguess, states)
            if output == True:
                print(AIguess)
                print(self.wordle.getColoredGuess(states, AIguess))
            guessNum += 1

if __name__ == "__main__":
    word = "flush"
    AI = WordleAI(Wordle(word, 6), scoreWordsByExpectedValue)
    AI.play(True)
    print("Win:", AI.wordle.checkForWin(), "Guesses:", AI.wordle.guessNum)