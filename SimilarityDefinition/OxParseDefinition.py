import WordnetHandler
import PreprocessDefinition
import OxfordParser
from collections import OrderedDict


def get_greatest_synset_similarity_between(synsets_wn, noun_2):
  synset_max = None

  synsets_of_noun = WordnetHandler.get_synsets_for_word(noun_2, 'n')

  if len(synsets_of_noun) > 0:
    synset_max = synsets_of_noun[0]
    p_max = 0

    for synset_of_noun in synsets_of_noun:
      for synset_wn in synsets_wn:
        p = synset_wn.path_similarity(synset_of_noun)
        if p > p_max:
          p_max = p
          synset_max = synset_of_noun

  return synset_max


#def get_definition_synset_with_synsetwn(definition, synsets_wn):
#  definition_synsets = []
#  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
#  nouns = list(set(nouns))
#  for noun in nouns:
#    synset_max = get_greatest_synset_similarity_between(synsets_wn, noun)
#    if synset_max is not None:
#      definition_synsets.append(synset_max)
#
#  return definition_synsets
#

def get_definition_synset_with_synsetwn(definition, synsets_wn):
  definition_synsets = []
  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
  nouns = list(set(nouns))
  for noun in nouns:
    synsets_of_noun = WordnetHandler.get_synsets_for_word(noun, 'n')
    for synset_of_noun in synsets_of_noun:
      definition_synsets.append(synset_of_noun)

  return definition_synsets


def get_dict_vectors_synsets_for_word(word, synsets_wn):
  vectors = OrderedDict()
  definitions = OxfordParser.get_definitions_of_word(word)
  for definition in definitions:
    vector = get_definition_synset_with_synsetwn(definition, synsets_wn)
    key = definition
    vectors[key] = vector

  return vectors
