import nltk
import POSWrapper
import WordnetHandler
import heapq

__dict_sim__ = {}
__WSD_type__ = 0  # 0: first, 1: max syn word-word

def create_key(sen_1, sen_2):
  return sen_1 + sen_2 + str(__WSD_type__)

def pos_is_noun(pos):
  return (pos == 'NN' or pos == 'NNS')


def pos_is_verb(pos):
  return (pos == 'VB' or pos == 'VBD' or pos == 'VBN')


def synsets_for_word(word):
  (word, pos) = word
  synsets_of_noun = []
  if pos_is_noun(pos):
    synsets_of_noun = WordnetHandler.get_synsets_for_word(word, 'n')
  if pos_is_verb(pos):
    synsets_of_noun = WordnetHandler.get_synsets_for_word(word, 'v')
  return synsets_of_noun


def sim_2_word(word_1, word_2):
  synsets_1 = synsets_for_word(word_1)
  synsets_2 = synsets_for_word(word_2)
  p_max = 0
  if __WSD_type__ == 1:
    for synset_1 in synsets_1:
      for synset_2 in synsets_2:
        p = WordnetHandler.cal_similarity(synset_1, synset_2)

        if p > p_max:
          p_max = p

  if __WSD_type__ == 0:
    if len(synsets_1) == 0 or len(synsets_2) == 0:
      return 0
    p_max = WordnetHandler.cal_similarity(synsets_1[0], synsets_2[0])

  return p_max


def sim_for_words_words_with_order(words_1, words_2):
  sim = 0.0001
  count = 0
  for word_1 in words_1:
    p_max = 0
    for word_2 in words_2:
      p = sim_2_word(word_1, word_2)
      if p > p_max:
        p_max = p

    if p > 0:
      count += 1
      sim += p_max

  sim /= (count + 0.001)
  return sim


def sim_for_words_words_no_order(sen_1, sen_2):
  key = create_key(sen_1, sen_2)
  if key not in __dict_sim__:
    words_1 = split_words(sen_1)
    words_2 = split_words(sen_2)
    sim_1 = sim_for_words_words_with_order(words_1, words_2)
    sim_2 = sim_for_words_words_with_order(words_2, words_1)
    __dict_sim__[key] = (sim_1 + sim_2)/2

  return __dict_sim__[key]


def split_words(sen):
  tokens = nltk.wordpunct_tokenize(sen)
  tagged_words = POSWrapper.pos_tag(tokens)
  return tagged_words


def wordnet_based(sen_1, sen_2, WSD_type):
  global __WSD_type__
  __WSD_type__ = WSD_type

  result = sim_for_words_words_no_order(sen_1, sen_2)
  return result


def max_wordnet_based(sens):
  sen_0 =  ""
  arr_result = []
  for i_sen in range(len(sens)):
    if i_sen == 0:
      sen_0 = sens[0]
    if i_sen < 2:
      continue
    sen_i = sens[i_sen]
    sim_len = wordnet_based(sen_0, sen_i)
    arr_result.append(sim_len)

  if len(arr_result) < 1:
    return (0, 0)
  if len(arr_result) < 2:
    return (arr_result[0], arr_result[0])

  order = heapq.nlargest(2, range(len(arr_result)), arr_result.__getitem__);
  return (arr_result[order[0]],arr_result[order[1]])


def wordnet_based_in_context(sen_1, sen_2, sens, WSD_type):
  global __WSD_type__
  __WSD_type__ = WSD_type

  result = sim_for_words_words_no_order(sen_1, sen_2)
  (first, second) = max_wordnet_based(sens)
  return result/second
