from nltk.corpus import wordnet as wn


def read_nouns():
  dict_wn = {}
  count = 0
  for synset in list(wn.all_synsets('n')):
    lemmas =  [str(lemma.name()) for lemma in synset.lemmas()]
    dict_wn[synset.name()] = lemmas

  return dict_wn


#dict_wn = read_nouns()
#print dict_wn
