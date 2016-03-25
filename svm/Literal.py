import Util
from nltk.stem import WordNetLemmatizer


__wordnet_lemmatizer__ = WordNetLemmatizer()


def split_and_stem(sen):
  words = Util.split_words(sen)
  words_stem = []
  for word in words:
    word_stem = __wordnet_lemmatizer__.lemmatize(word)
    words_stem.append(word_stem)

  return words_stem

def levenshtein(sen_1, sen_2):
  words_1 = split_and_stem(sen_1)
  words_2 = split_and_stem(sen_2)

  return Util.levenshtein(words_1, words_2)
