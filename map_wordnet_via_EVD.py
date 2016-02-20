import EVDParser
import WordnetProcessForEVD
import collections
import FileProcess


def map_wordnet_EVD():
  dict_EVD = EVDParser.readEVDFile()
  dict_wn = WordnetProcessForEVD.read_nouns()

  for key, values in dict_wn.items():
    vi_means = []
    values = list(set(values))
    for value in values:
      if not dict_EVD.has_key(value):
        continue
      vi_mean = dict_EVD[value]
      for element in vi_mean:
        vi_means.append(element)

#    if len(values) > 1:
#      means = [item for item, count in collections.Counter(vi_means).items() if count > 1]
#    else:
#      means = [item for item, count in collections.Counter(vi_means).items() if count >= 1]

    means = [item for item, count in collections.Counter(vi_means).items() if count > 1]
    if len(means) > 0:
      means.insert(0,key)
      FileProcess.append_result_to_excel_file("Results/EVD/wn_evd.csv",means)

map_wordnet_EVD()
