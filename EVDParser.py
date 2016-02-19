import nltk


def readEVDFile():
  dictEVD = {}
  f = open("EVD/EVD99k.txt")
  line = f.readline()
  while (line):
    word_meaning = line.split("#")
    word = word_meaning[0]
    word_meaning[1] = word_meaning[1][:-3]
    meaning = word_meaning[1].split(",")
    dictEVD[word] = meaning
    line = f.readline()

  return dictEVD


#dictEVD = readEVDFile()
#print dictEVD["a b c-book"]
