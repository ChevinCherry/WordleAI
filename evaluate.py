import random
from simWordle import Wordle
from wordleAI import WordleAI
from policies import scoreWordsByExpectedValue, scoreWordsByLetterFrequency, scoreWordsByLetterPlacementFrequency, singleWordPolicy

class evaluateModel:

    def __init__(self, policies: list):
        words = open('answers.txt')
        self.testWords = words.read().splitlines()
        self.testPolicies = policies

    def __score(self, win, guessNum):
        if win:
            return guessNum
        return 10
    
    def __scoreGames(self, word):
        games = [WordleAI(Wordle(word, 6), policy) for policy in self.testPolicies]
        for game in games:
            game.play(False)
        return [self.__score(game.wordle.checkForWin(), game.wordle.guessNum) for game in games]
    
    def __printStats(self, scores):
        scoreTotals = [ sum(x) for x in zip(*scores)]
        numTrials = len(scores)
        averages = [total / numTrials for total in scoreTotals]
        print(averages)

    def run(self, maxTests=None):
        if maxTests:
            useWords = random.sample(self.testWords, maxTests)
        else:
            useWords = self.testWords
        print("Running tests...")
        scores = [self.__scoreGames(word) for word in useWords]
        print("Done! Showing stats...")
        print(useWords)
        self.__printStats(scores)

if __name__ == "__main__":
    policies = [scoreWordsByExpectedValue]
    eval = evaluateModel(policies)
    eval.run(100)
            




