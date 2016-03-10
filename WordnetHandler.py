from nltk.corpus import wordnet as wn

__dict_synsets__ = {}
__dict_similarity__ = {}
__dict_freq_count__ = {}


def create_key_for_get_synsets(word, pos):
  return word + "-" + pos


def get_synsets_for_word(word, pos_tag):
  key = create_key_for_get_synsets(word, pos_tag)
  if key not in __dict_synsets__:
    __dict_synsets__[key] = wn.synsets(word, pos=pos_tag)

  return __dict_synsets__[key]


def create_key_for_similarity(synset_1, synset_2):
  return synset_1.name() + '--' + synset_2.name()


def similarity(synset_1, synset_2):
  sim = 0
  sim = synset_1.path_similarity(synset_2)
#  if synset_1.pos() == synset_2.pos():
#    sim = synset_1.lch_similarity(synset_2)
#  sim = synset_1.wup_similarity(synset_2)

  return sim


def cal_similarity(synset_1, synset_2):
  key = create_key_for_similarity(synset_1, synset_2)
  if key not in __dict_similarity__:
    __dict_similarity__[key] = similarity(synset_1, synset_2)

  return __dict_similarity__[key]


def get_freq_count_of_synset(synset):
  key = synset.name()
  if key not in __dict_freq_count__:
    count = 0
    for lemma in synset.lemmas():
      count += lemma.count()
    __dict_freq_count__[key] = count
  return __dict_freq_count__[key]
