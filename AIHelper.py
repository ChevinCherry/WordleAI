from policies import scoreWordsByExpectedValue
from simWordle import Wordle
from utils import filterValidWords
from wordleAI import WordleAI

def parseStates(stateStr):
    states = []
    for char in stateStr:
        if char == "b":
            states.append("incorrect")
        elif char == "y":
            states.append("wrongPlace")
        elif char == "g":
            states.append("correct")
    return states

maxGuesses = 6

helper = WordleAI(Wordle("fills", maxGuesses), scoreWordsByExpectedValue)
guessNum = 0
while guessNum < maxGuesses:
    validGuess = False
    while not validGuess:
        print("Enter guess:")
        guess = input().strip("\n")
        validGuess = guess in helper.allWords
        if not validGuess:
            print("Invalid.")
    print("Enter states:")
    states = parseStates(input().strip("\n"))
    print(helper.wordle.getColoredGuess(states, guess))
    helper.validWords = filterValidWords(helper.validWords, guess, states)
    helper.wordle.guessNum += 1
    print("Suggested next guess:", helper.makeGuess())
    guessNum += 1
