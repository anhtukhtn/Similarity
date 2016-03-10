import WordnetHandler
import PreprocessDefinition
from collections import OrderedDict


__dict_defi_for_synset__ = {}
__dict_feature_for_synset = {}


def pos_is_noun(pos):
  return (pos == 'NN' or pos == 'NNS' or pos == 'JJ')


def pos_is_verb(pos):
  return (pos == 'VB' or pos == 'VBD' or pos == 'VBN')


def get_greatest_synset_similarity_between(synset_1, noun_2):
  synset_max = None

  (word, pos) = noun_2
  synsets_of_noun = []
#  if pos_is_noun(pos):
#    synsets_of_noun = WordnetHandler.get_synsets_for_word(word, 'n')
#  if pos_is_verb(pos):
#    synsets_of_noun = WordnetHandler.get_synsets_for_word(word, 'v')

  synsets_of_noun_1 = WordnetHandler.get_synsets_for_word(word, 'n')
  synsets_of_noun_2 = WordnetHandler.get_synsets_for_word(word, 'v')
  synsets_of_noun = synsets_of_noun_1 + synsets_of_noun_2

  total_count = 11.0
  for synset_of_noun in synsets_of_noun:
    total_count += WordnetHandler.get_freq_count_of_synset(synset_of_noun)
#
  if len(synsets_of_noun) > 0:
    synset_max = synsets_of_noun[0]
    p_max = 0.0

    for synset_of_noun in synsets_of_noun:
#      p = synset_1.path_similarity(synset_of_noun)
      p = WordnetHandler.cal_similarity(synset_1, synset_of_noun)

      if p is not None:
        synset_freq_count = 11.0
        synset_freq_count += WordnetHandler.get_freq_count_of_synset(synset_of_noun)

        p = p*(synset_freq_count/total_count)
#
      if p > p_max:
        p_max = p
        synset_max = synset_of_noun

  return synset_max


def get_feature_synset_for(synset):
  key = synset.name()
  if key not in __dict_feature_for_synset:
    synsets_definition = []
    definition = synset.definition()
    nouns = PreprocessDefinition.preprocess_sentence(definition)
#    nouns = list(set(nouns))
    for noun in nouns:
      synset_max = get_greatest_synset_similarity_between(synset, noun)
      if synset_max is not None:
        synsets_definition.append(synset_max)

      # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      # # get hypernyms
      # print "\nhypernyms ------";
#    for hypernym in synset.hypernyms():
#      synsets_definition.append(hypernym)
#
#      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
#      # get hyponyms
#    for hyponym in synset.hyponyms():
#      synsets_definition.append(hyponym)
#
#    for meronym in synset.part_meronyms():
#      synsets_definition.append(meronym)
#
#    for holonym in synset.member_holonyms():
#      synsets_definition.append(holonym)

#    for example in synset.examples():
#      for lemma in synset.lemmas():
#        example = example.replace(lemma.name(), "")
#      nouns = PreprocessDefinition.preprocess_sentence(example)
#      nouns = list(set(nouns))
#      for noun in nouns:
#        synset_max = get_greatest_synset_similarity_between(synset, noun)
#        if synset_max is not None:
#          synsets_definition.append(synset_max)

    synsets_definition.append(synset)
    __dict_feature_for_synset[key] = synsets_definition

  return __dict_feature_for_synset[key]


def get_value_synset_for(cur_synset, synsets):
  synsets_value = []
  definition = cur_synset.definition()
  nouns = PreprocessDefinition.preprocess_sentence(definition)
#  nouns = list(set(nouns))
  for synset in synsets:
    count = 0
    p = 0
    for noun in nouns:
      synset_max = get_greatest_synset_similarity_between(synset, noun)
      if synset_max is not None:
        count += 1
        sim = WordnetHandler.cal_similarity(synset, synset_max)
        if sim != None:
          p += sim

    if count != 0:
      p = p/count

    synsets_value.append(p)

  return synsets_value


def get_definition_synset(synset):
  key = synset.name()
  if key not in __dict_defi_for_synset__:
    synsets_definition = []
    definition = synset.definition()
  #  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
    nouns = PreprocessDefinition.preprocess_sentence(definition)
#    nouns = list(set(nouns))
    for noun in nouns:
      synset_max = get_greatest_synset_similarity_between(synset, noun)
      if synset_max is not None:
        synsets_definition.append(synset_max)
    __dict_defi_for_synset__[key] = synsets_definition

  return __dict_defi_for_synset__[key]


def get_dict_vectors_synsets_for_word(word):
  vectors = OrderedDict()
  synsets = WordnetHandler.get_synsets_for_word(word, 'n')
  for synset in synsets:
    vector = get_feature_synset_for(synset)
    key = synset.definition()
    vectors[key] = vector

  return vectors


def get_vectors_defi_for_word(word):
  vectors = OrderedDict()
  synsets = WordnetHandler.get_synsets_for_word(word, 'n')
  for synset in synsets:
    vector = get_definition_synset(synset)
    key = synset.definition()
    vectors[key] = vector

  return vectors


def get_dict_vectores_synsets_for_synsets(synsets):
  vectors = OrderedDict()
  for synset in synsets:
    vector = get_feature_synset_for(synset)
    key = synset.definition()
    vectors[key] = vector

  return vectors


def get_dict_vectors_value_for(word):
  vectors = OrderedDict()
  synsets = WordnetHandler.get_synsets_for_word(word, 'n')
  for synset in synsets:
    vector = get_value_synset_for(synset, synsets)
    key = synset.definition()
    vectors[key] = vector

  return vectors
