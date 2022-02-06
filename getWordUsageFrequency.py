import json
import requests

def getWordDataFromGoogle(words):
    wordsString = ",".join(words)
    requestURL = "https://books.google.com/ngrams/json?content=" + wordsString + "&year_start=2018&year_end=2019&corpus=26&smoothing=0"
    res = requests.get(requestURL)
    wordData = json.loads(res.text)
    print(len(wordData))
    return wordData

wordFile = open("validWords.txt")
validWords = wordFile.read().splitlines()
wordFile.close()
batchSize = 1000
maxEntries = 1000000

curIndex = 0
nextIndex = batchSize
allWordsData = []
while (nextIndex < len(validWords) and nextIndex < maxEntries):
    words = validWords[curIndex:nextIndex]
    print(curIndex, "to", nextIndex)
    allWordsData += getWordDataFromGoogle(words)
    curIndex = nextIndex
    nextIndex += batchSize
if (curIndex < len(validWords) or curIndex < maxEntries):
    nextIndex = min(len(validWords), maxEntries)
    print(curIndex, "to", nextIndex)
    words = validWords[curIndex:nextIndex]
    allWordsData += getWordDataFromGoogle(words)

newFile = open("validWordAndFreq.txt", "w")
indexOffset = 0
for index, word in enumerate(validWords):
    if (index >= maxEntries):
        break
    wordData = allWordsData[index - indexOffset]
    dataWord = wordData["ngram"]
    writeString = ""
    if (dataWord != word):
        print(word)
        writeString = word + " 0.0"
        indexOffset += 1
    else:
        writeString = " ".join([wordData["ngram"], str(wordData["timeseries"][1])])
    newFile.write(writeString + "\n")