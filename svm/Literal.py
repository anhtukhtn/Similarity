import Util
from nltk.stem import WordNetLemmatizer
import heapq


__wordnet_lemmatizer__ = WordNetLemmatizer()
__dict_len__ = {}


def key_len(sen_1, sen_2):
  return sen_1 + sen_2


def split_and_stem(sen):
  words = Util.split_words(sen)
  words_stem = []
  for word in words:
    word_stem = __wordnet_lemmatizer__.lemmatize(word)
    words_stem.append(word_stem)

  return words_stem


def levenshtein(sen_1, sen_2):
  key = key_len(sen_1, sen_2)
  if key not in __dict_len__:
    words_1 = split_and_stem(sen_1)
    words_2 = split_and_stem(sen_2)
    levensh = Util.levenshtein(words_1, words_2)*1.0/(len(words_1) + len( words_2))
    __dict_len__[key] = levensh

  return  __dict_len__[key]


def max_levenshtein(sens):
  sen_0 =  ""
  arr_result = []
  for i_sen in range(len(sens)):
    if i_sen == 0:
      sen_0 = sens[0]
    if i_sen < 2:
      continue
    sen_i = sens[i_sen]
    sim_len = 1.00001 -levenshtein(sen_0, sen_i)
    arr_result.append(sim_len)

  if len(arr_result) < 1:
    return (0, 0)
  if len(arr_result) < 2:
    return (arr_result[0], arr_result[0])

  order = heapq.nlargest(2, range(len(arr_result)), arr_result.__getitem__);
  return (arr_result[order[0]],arr_result[order[1]])


def levenshtein_in_context(sen_1, sen_2, sens):
  sim_len = 1-levenshtein(sen_1, sen_2)
  (first, second) = max_levenshtein(sens)
  return sim_len/second
