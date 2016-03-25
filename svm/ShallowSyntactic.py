import nltk
import POSWrapper
from nltk.metrics import jaccard_distance

def split_and_POS(sen):
  # tokenize
  tokens = nltk.wordpunct_tokenize(sen)
  # pos tag
  tagged_words = POSWrapper.pos_tag(tokens)

  arr_pos = []
  for (word, pos) in tagged_words:
    arr_pos.append(pos)

  return arr_pos

def jaccard_POS(sen_1, sen_2):
  pos_1 = split_and_POS(sen_1)
  pos_2 = split_and_POS(sen_2)

  pos_1 = set(pos_1)
  pos_2 = set(pos_2)
  return jaccard_distance(pos_1, pos_2)

