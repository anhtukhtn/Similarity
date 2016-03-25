from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

__dict_synsets__ = {}
__dict_similarity__ = {}
__dict_freq_count__ = {}
__dict_lemma__ = {}
__dict_word_word__ = {}


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
#  if synset_1.pos() == synset_2.pos() and synset_1.pos() != "a" and synset_1.pos() != "s":
#    sim = synset_1.lin_similarity(synset_2, brown_ic)
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


def get_lemma_synset(synset):
  key = synset.name()
  if key not in __dict_lemma__:
    lemma_gloss = ""
    for lemma in synset.lemmas():
      gloss = lemma.name().replace("_", " ")
      lemma_gloss += " " + gloss
    __dict_lemma__[key] = lemma_gloss

  return __dict_lemma__[key]


def sim_2_word(word_1, word_2, synset):
  synsets_1_n = get_synsets_for_word(word_1, 'n')
  synsets_1_v = get_synsets_for_word(word_1, 'v')
  synsets_1_a = get_synsets_for_word(word_1, 'a')
  synsets_1 = synsets_1_a + synsets_1_n + synsets_1_v
  synsets_2_n = get_synsets_for_word(word_2, 'n')
  synsets_2_v = get_synsets_for_word(word_2, 'v')
  synsets_2_a = get_synsets_for_word(word_2, 'a')
  synsets_2 = synsets_2_a + synsets_2_n + synsets_2_v
  p_max = 0

  total_count = 0.1
  for synset_of_noun in synsets_1:
    total_count += get_freq_count_of_synset(synset_of_noun)
  for synset_of_noun in synsets_2:
    total_count += get_freq_count_of_synset(synset_of_noun)
#  total_count += get_freq_count_of_synset(synset)

  for synset_1 in synsets_1:
    for synset_2 in synsets_2:
      p = cal_similarity(synset_1, synset_2)

#      p_2 = cal_similarity(synset_1, synset_2)
#      if p_2 != None:
#        synset_freq_count = 0.0
#        synset_freq_count += get_freq_count_of_synset(synset_1)
#        synset_freq_count += get_freq_count_of_synset(synset_2)
#        p += p_2*synset_freq_count
#
#      p_2 = cal_similarity(synset, synset_2)
#      if p_2 != None:
#        synset_freq_count = 0.0
#        synset_freq_count += get_freq_count_of_synset(synset)
#        synset_freq_count += get_freq_count_of_synset(synset_2)
#        p += p_2*synset_freq_count
#
#      p_2 = cal_similarity(synset, synset_1)
#      if p_2 != None:
#        synset_freq_count = 0.0
#        synset_freq_count += get_freq_count_of_synset(synset_1)
#        synset_freq_count += get_freq_count_of_synset(synset)
#        p += p_2*synset_freq_count
#
#      p = p/3.0
#      p = p/total_count
      if p > p_max:
        p_max = p

  return p_max


def sim_for_words_words_with_order(words_1, words_2, synset):
  sim = 0
  for (word_1,pos_1) in words_1:
    p_max = 0
    for (word_2,pos_2) in words_2:
      p = sim_2_word(word_1, word_2, synset)
      if p > p_max:
        p_max = p
    sim += p_max
  sim /= (len(words_1) + 0.001)
  return sim

def sim_for_words_words_no_order(words_1, words_2, synset = None):
  sim_1 = sim_for_words_words_with_order(words_1, words_2, synset)
  sim_2 = sim_for_words_words_with_order(words_2, words_1, synset)
  return (sim_1 + sim_2)/2


def get_nearest_synsets_words_words_order(words_1, words_2):
  synsets_result = []
  for (word_1,pos_1) in words_1:
    synsets_1_n = get_synsets_for_word(word_1, 'n')
    synsets_1_v = get_synsets_for_word(word_1, 'v')
    synsets_1_a = get_synsets_for_word(word_1, 'a')
    synsets_1 = synsets_1_a + synsets_1_n + synsets_1_v
    if len(synsets_1) == 0:
      return synsets_result
    p_max = 0
    synset_max = synsets_1[0]

    for synset_1 in synsets_1:

      for (word_2,pos_2) in words_2:
        synsets_2_n = get_synsets_for_word(word_2, 'n')
        synsets_2_v = get_synsets_for_word(word_2, 'v')
        synsets_2_a = get_synsets_for_word(word_2, 'a')
        synsets_2 = synsets_2_a + synsets_2_n + synsets_2_v

        total_count = 0.1
        for synset_of_noun in synsets_1:
          total_count += get_freq_count_of_synset(synset_of_noun)
        for synset_of_noun in synsets_2:
          total_count += get_freq_count_of_synset(synset_of_noun)

        for synset_2 in synsets_2:
          p = cal_similarity(synset_1, synset_2)

          if p != None:
            synset_freq_count = 0.0
            synset_freq_count += get_freq_count_of_synset(synset_1)
            synset_freq_count += get_freq_count_of_synset(synset_2)
            p += p*synset_freq_count/total_count

          if p > p_max:
            p_max = p
            synset_max = synset_1

    synsets_result.append((synset_max,1))

  return synsets_result

def get_nearest_synsets_words_words_noorder(words_1, words_2):
  vector_1 = get_nearest_synsets_words_words_order(words_1, words_2)
  vector_2 = get_nearest_synsets_words_words_order(words_2, words_1)
  return (vector_1, vector_2)


def get_nearest_synsets_words_synsets_order(words, synsets):
  synsets_result = []
  for (word,pos) in words:
    synsets_n = get_synsets_for_word(word, 'n')
    synsets_v = get_synsets_for_word(word, 'v')
    synsets_a = get_synsets_for_word(word, 'a')
    synsets_word = synsets_a + synsets_n + synsets_v

    if len(synsets_word) == 0:
      return synsets_result
    p_max = 0
    synset_max = synsets_word[0]

    for synset_word in synsets_word:
      for (synset_2, weight) in synsets:
        p = cal_similarity(synset_word, synset_2)
        if p > p_max:
          p_max = p
          synset_max = synset_word

    synsets_result.append((synset_max,1))

  return synsets_result


def get_definitions_for_word(word):
  defis = []
  synsets = get_synsets_for_word(word, 'n')
  for synset in synsets:
    defis.append(synset.definition())

  return defis
