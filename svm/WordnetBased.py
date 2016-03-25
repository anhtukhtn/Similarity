import nltk
import POSWrapper
import WordnetHandler


def pos_is_noun(pos):
  return (pos == 'NN' or pos == 'NNS' or pos == 'JJ')


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
#  p_max = 0
#
#  for synset_1 in synsets_1:
#    for synset_2 in synsets_2:
#      p = WordnetHandler.cal_similarity(synset_1, synset_2)
#
#      if p > p_max:
#        p_max = p
#
  if len(synsets_1) == 0 or len(synsets_2) == 0:
    return 0
  p_max = WordnetHandler.cal_similarity(synsets_1[0], synsets_2[0])
  return p_max


def sim_for_words_words_with_order(words_1, words_2):
  sim = 0
  for word_1 in words_1:
    p_max = 0
    for word_2 in words_2:
      p = sim_2_word(word_1, word_2)
      if p > p_max:
        p_max = p
    sim += p_max
  sim /= (len(words_1) + 0.001)
  return sim


def sim_for_words_words_no_order(words_1, words_2):
  sim_1 = sim_for_words_words_with_order(words_1, words_2)
  sim_2 = sim_for_words_words_with_order(words_2, words_1)
  return (sim_1 + sim_2)/2


def split_words(sen):
  tokens = nltk.wordpunct_tokenize(sen)
  tagged_words = POSWrapper.pos_tag(tokens)
  return tagged_words


def wordnet_based(sen_1, sen_2):
  words_1 = split_words(sen_1)
  words_2 = split_words(sen_2)
  result = sim_for_words_words_no_order(words_1, words_2)
  return result
