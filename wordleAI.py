from copy import deepcopy
from policies import scoreWordsByExpectedValue, scoreWordsByLetterFrequency, scoreWordsByLetterPlacementFrequency, singleWordPolicy
from simWordle import Wordle
from utils import filterValidWords, normalizeWordProbs

class WordleAI:

    def __init__(self, wordle: Wordle, policy):
        self.wordle = wordle
        self.policy = policy
        words = open("validWordAndFreq.txt")
        wordsAndFreqStrings = words.read().splitlines()
        wordAndFreqs = []
        for wf in wordsAndFreqStrings:
            strings = wf.split(" ")
            word = strings[0]
            freq = float(strings[1])
            wordAndFreqs.append((word, freq))
        words.close()
        self.validWords = wordAndFreqs
        self.allWords = deepcopy(wordAndFreqs)

    def makeGuess(self):
        return self.policy(self.allWords, normalizeWordProbs(self.validWords), self.wordle.guessNum)
        
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
    word = "grass"
    AI = WordleAI(Wordle(word, 6), scoreWordsByExpectedValue)
    AI.play(True)
    print("Win:", AI.wordle.checkForWin(), "Guesses:", AI.wordle.guessNum)