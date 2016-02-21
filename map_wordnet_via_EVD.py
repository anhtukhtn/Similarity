import EVDParser
import WordnetProcessForEVD
import collections
import FileProcess
from nltk.corpus import wordnet as wn

from operator import itemgetter

def map_wordnet_EVD():
  dict_EVD = EVDParser.readEVDFile()
  dict_wn = WordnetProcessForEVD.read_nouns()

  for key, values in dict_wn.items():
    vi_means = []

    noun = key.split(".")[0]
    synset_noun = wn.synsets(noun, pos = 'n')
    # if just has 1 synset and has in evd
    if len(synset_noun) == 1 and dict_EVD.has_key(noun):
      values = [noun]

    values = list(set(values))
    for value in values:
      value = value.replace("_"," ")
      if not dict_EVD.has_key(value):
        continue
      vi_mean = dict_EVD[value]
      for element in vi_mean:
        vi_means.append(element)

#    if len(values) > 1:
#      means = [item for item, count in collections.Counter(vi_means).items() if count > 1]
#    else:
#      means = [item for item, count in collections.Counter(vi_means).items() if count >= 1]

    means = []
    if len(values) == 1:
      means = vi_means
      item_count = [(item,count) for item, count in collections.Counter(vi_means).items() if count > 1]
      if len(item_count) > 0:
        means = [max(item_count,key = itemgetter(1))[0]]

        items_2 = [item for item, count in collections.Counter(vi_means).items() if count > 2]
        for item in items_2:
          means.append(item)
        means = list(set(means))

    else:
      item_count = [(item,count) for item, count in collections.Counter(vi_means).items() if count > 1]
      if len(item_count) == 0:
        continue
      means = [max(item_count,key = itemgetter(1))[0]]

      items_2 = [item for item, count in collections.Counter(vi_means).items() if count > 2]
      for item in items_2:
        means.append(item)
      means = list(set(means))

    if len(means) > 0:
      means.insert(0,key)
      FileProcess.append_result_to_excel_file("Results/EVD/wn_evd.csv",means)


map_wordnet_EVD()
