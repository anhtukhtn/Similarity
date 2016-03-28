import nltk
import POSWrapper
from nltk.metrics import jaccard_distance
import heapq

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


def max_jaccard_POS(sens):
  sen_0 =  ""
  arr_result = []
  for i_sen in range(len(sens)):
    if i_sen == 0:
      sen_0 = sens[0]
    if i_sen < 2:
      continue
    sen_i = sens[i_sen]
    sim_len = 1.00001 -jaccard_POS(sen_0, sen_i)
    arr_result.append(sim_len)

  if len(arr_result) < 1:
    return (0, 0)
  if len(arr_result) < 2:
    return (arr_result[0], arr_result[0])

  order = heapq.nlargest(2, range(len(arr_result)), arr_result.__getitem__);
  return (arr_result[order[0]],arr_result[order[1]])


def jaccard_POS_in_context(sen_1, sen_2, sens):
  sim_len = 1-jaccard_POS(sen_1, sen_2)
  (first, second) = max_jaccard_POS(sens)
  return sim_len/second
