import EVDParser
import WordnetProcessForEVD
import FileProcess
from nltk.corpus import wordnet as wn
import SimilarityWordnetOxford

from nltk.metrics import jaccard_distance
import Util


def word_word_is_similarity(phrase_word_1, phrase_word_2):
  words_1 = Util.split_unicode_words(phrase_word_1)
  words_2 = Util.split_unicode_words(phrase_word_2)
  if len(words_1) == 0 or len(words_2) == 0:
    return False

  jaccard_similarity = jaccard_distance(words_1, words_2)

  return jaccard_similarity < 0.1


def count_word_in_set(word, words):
  count = 0
  for word_ in words:
    if word_word_is_similarity(word, word_):
      count += 1

  return count


def get_best_mean(means_EVD, means_ox, count_min):
  means = set(means_EVD) | set(means_ox)

  mean_best = []
  count_best = 0
  for mean in means:
    count = count_word_in_set(mean, means)
    if count > count_min and count > count_best:
      count_best = count

  for mean in means:
    count = count_word_in_set(mean, means)
    if count == count_best and count_best >= 0:
      mean_best.append(mean)

  if count_best == 0:
    if len(means_ox) > 0:
      return means_ox
    else:
      return means_EVD

  return mean_best


def get_EVD_means(key, key_lemmas, values, dict_EVD):
  vi_means = []
  noun = key.split(".")[0]
  synset_noun = wn.synsets(noun, pos='n')
  # if just has 1 synset and has in evd
  if len(synset_noun) == 1:
    for lemma in key_lemmas:
      if dict_EVD.has_key(noun):
        values = key_lemmas
        print("just has 1 synset")
        print values
        break

  values = list(set(values))
  for value in values:
    value = value.replace("_", " ")
    if not dict_EVD.has_key(value):
      continue
    vi_mean = dict_EVD[value]
    for element in vi_mean:
      if element not in vi_means:
        vi_means.append(element)

  return vi_means


__dict_Ox__ = {}


def get_Ox_means(key, key_lemmas):
  means = []
  for noun in key_lemmas:
    if not __dict_Ox__.has_key(noun):
      filted_dict = SimilarityWordnetOxford.cal_similarity_for_word(noun)
      __dict_Ox__[noun] = filted_dict

  for noun in key_lemmas:
    if __dict_Ox__[noun].has_key(key):
      means = __dict_Ox__[noun][key]
      break

  return means


def map_wordnet_EVD():
  print "loading EVD"
  dict_EVD = EVDParser.readEVDFile()
  print "loading WN"
  dict_wn = WordnetProcessForEVD.read_nouns()

  for key, values in dict_wn.items():
    key_lemmas = key.split("=")[1]
    key_lemmas = key_lemmas.split("-")
    key = key.split("=")[0]
    key_definition = key.split("-")[1]
    key = key.split("-")[0]

    test_flag = 0
    for lemma in key_lemmas:
      if lemma[:1] == "b" :
        test_flag = 1
    if test_flag == 0:
      continue

    print "map_wordnet_EVD " + key

    vi_means = get_EVD_means(key, key_lemmas, values, dict_EVD)
    ox_means = get_Ox_means(key, key_lemmas)

    means = get_best_mean(vi_means, ox_means, 2)

################################################################################
# get greatest duplicated mean
#    if len(values) == 1:
#      means = vi_means
#      item_count = [(item,count) for item, count in collections.Counter(vi_means).items() if count > 1]
#      if len(item_count) > 0:
#        means = [max(item_count,key = itemgetter(1))[0]]
#
#        items_2 = [item for item, count in collections.Counter(vi_means).items() if count > 2]
#        for item in items_2:
#          means.append(item)
#        means = list(set(means))
#
#    else:
#      item_count = [(item,count) for item, count in collections.Counter(vi_means).items() if count > 1]
#      if len(item_count) == 0:
#        continue
#      means = [max(item_count,key = itemgetter(1))[0]]
#
#      items_2 = [item for item, count in collections.Counter(vi_means).items() if count > 2]
#      for item in items_2:
#        means.append(item)
#      means = list(set(means))
################################################################################

    if len(means) > 0:
      means = [means[0]]
      means.insert(0,key + "-" + key_definition)
      filename = "Results/EVD/wn_evd_b_0_1.csv"
      FileProcess.append_result_to_excel_file(filename, means)


map_wordnet_EVD()
