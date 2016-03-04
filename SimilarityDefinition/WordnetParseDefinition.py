import WordnetHandler
import PreprocessDefinition
from collections import OrderedDict


__dict_defi_for_synset__ = {}
__dict_feature_for_synset = {}


def get_greatest_synset_similarity_between(synset_1, noun_2):
  synset_max = None

  synsets_of_noun = WordnetHandler.get_synsets_for_word(noun_2, 'n')
  synsets_of_verb = WordnetHandler.get_synsets_for_word(noun_2, 'v')
  synsets_of_noun = synsets_of_noun + synsets_of_verb

  if len(synsets_of_noun) > 0:
    synset_max = synsets_of_noun[0]
    p_max = 0

    for synset_of_noun in synsets_of_noun:
#      p = synset_1.path_similarity(synset_of_noun)
      p = WordnetHandler.cal_similarity(synset_1, synset_of_noun)
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
    nouns = list(set(nouns))
    for noun in nouns:
      synset_max = get_greatest_synset_similarity_between(synset, noun)
      if synset_max is not None:
        synsets_definition.append(synset_max)

      # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      # # get hypernyms
      # print "\nhypernyms ------";
  #  for hypernym in synset.hypernyms():
  #    synsets_definition.append(hypernym)
  #
  #    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #    # get hyponyms
  #  for hyponym in synset.hyponyms():
  #    synsets_definition.append(hyponym)
  #
  #  for meronym in synset.part_meronyms():
  #    synsets_definition.append(meronym)
  #
  #  for holonym in synset.member_holonyms():
  #    synsets_definition.append(holonym)
  #
    synsets_definition.append(synset)
    __dict_feature_for_synset[key] = synsets_definition

  return __dict_feature_for_synset[key]


def get_definition_synset(synset):
  key = synset.name()
  if key not in __dict_defi_for_synset__:
    synsets_definition = []
    definition = synset.definition()
  #  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
    nouns = PreprocessDefinition.preprocess_sentence(definition)
    nouns = list(set(nouns))
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
    vector = get_definition_synset(synset)
    key = synset.definition()
    vectors[key] = vector

  return vectors
