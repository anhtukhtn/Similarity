import WordnetHandler
import PreprocessDefinition
import OxfordParser
from collections import OrderedDict


def pos_is_noun(pos):
  return (pos == 'NN' or pos == 'NNS' or pos == 'JJ')


def pos_is_verb(pos):
  return (pos == 'VB' or pos == 'VBD' or pos == 'VBN')


def get_greatest_synset_similarity_between(synsets_wn, noun_2):
  synset_max = None

  (word, pos) = noun_2
  synsets_of_noun = []
  if pos_is_noun(pos):
    synsets_of_noun = WordnetHandler.get_synsets_for_word(word, 'n')
  if pos_is_verb(pos):
    synsets_of_noun = WordnetHandler.get_synsets_for_word(word, 'v')

  if len(synsets_of_noun) > 0:
    synset_max = synsets_of_noun[0]
    p_max = 0

    for synset_of_noun in synsets_of_noun:
      for synset_wn in synsets_wn:
#        p = synset_wn.path_similarity(synset_of_noun)
        p = WordnetHandler.cal_similarity(synset_wn, synset_of_noun)
        if p > p_max:
          p_max = p
          synset_max = synset_of_noun

  return synset_max

#
def get_greatest_synsets_similarity_between(synsets_wn, nouns):
  synset_wn_max = None
  p_max = 0

  if len(nouns) != 0:
    for synset_wn in synsets_wn:
      p_noun = 0
      for noun in nouns:
        synsets_of_noun = WordnetHandler.get_synsets_for_word(noun, 'n')

        if len(synsets_of_noun) > 0:
          p_each_noun = 0
          for synset_of_noun in synsets_of_noun:
    #        p = synset_wn.path_similarity(synset_of_noun)
            p = WordnetHandler.cal_similarity(synset_wn, synset_of_noun)
            p_each_noun += p
          p_each_noun = p_each_noun/len(synsets_of_noun)
          p_noun += p_each_noun

      p = p_noun/len(nouns)
      if p > p_max:
        synset_wn_max = synset_wn
  else:
    print "no nouns"

  return synset_wn_max

# get synsets via fix main synset
#def get_definition_synset_with_synsetwn(definition, synsets_wn):
#  definition_synsets = []
#  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
#  nouns = list(set(nouns))
#  max_wn_syn = get_greatest_synsets_similarity_between(synsets_wn, nouns)
#  if max_wn_syn is not None:
#    synsets_wn = [max_wn_syn]
#    for noun in nouns:
#        synset_max = get_greatest_synset_similarity_between(synsets_wn, noun)
#        if synset_max is not None:
#          definition_synsets.append(synset_max)
#
#  return definition_synsets


# synsets via synsets of main synset in wn
def get_definition_synset_with_synsetwn(definition, synsets_wn):
  definition_synsets = []
#  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
  nouns = PreprocessDefinition.preprocess_sentence(definition)
  nouns = list(set(nouns))
  for noun in nouns:
    synset_max = get_greatest_synset_similarity_between(synsets_wn, noun)
    if synset_max is not None:
      definition_synsets.append(synset_max)

  return definition_synsets


# all synsets
#def get_definition_synset_with_synsetwn(definition, synsets_wn):
#  definition_synsets = []
#  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
#  nouns = list(set(nouns))
#  for noun in nouns:
#    synsets_of_noun = WordnetHandler.get_synsets_for_word(noun, 'n')
#    for synset_of_noun in synsets_of_noun:
#      definition_synsets.append(synset_of_noun)
#
#  return definition_synsets


def get_dict_vectors_synsets_for_word(word, synsets_wn):
  vectors = OrderedDict()
  definitions = OxfordParser.get_definitions_of_word(word)
  for definition in definitions:
    vector = get_definition_synset_with_synsetwn(definition, synsets_wn)
    key = definition
    vectors[key] = vector

  return vectors
