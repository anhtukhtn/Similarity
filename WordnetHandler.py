from nltk.corpus import wordnet as wn

__dict_synsets__ = {}


def create_key(word, pos):
  return word + "-" + pos


def get_synsets_for_word(word, pos_tag):
  key = create_key(word, pos_tag)
  if not __dict_synsets__.has_key(key):
    __dict_synsets__[key] = wn.synsets(word, pos=pos_tag)
  return __dict_synsets__[key]
