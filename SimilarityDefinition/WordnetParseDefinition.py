import WordnetHandler
import PreprocessDefinition


def get_greatest_synset_similarity_between(synset_1, noun_2):
  synset_max = None

  synsets_of_noun = WordnetHandler.get_synsets_for_word(noun_2, 'n')

  if len(synsets_of_noun) > 0:
    synset_max = synsets_of_noun[0]
    p_max = 0

    for synset_of_noun in synsets_of_noun:
      p = synset_1.path_similarity(synset_of_noun)
      if p > p_max:
        p_max = p
        synset_max = synset_of_noun

  return synset_max


def get_definition_synset(synset):
  synsets_definition = []
  definition = synset.definition()
  nouns = PreprocessDefinition.preprocess_sentence_to_nouns(definition)
  nouns = list(set(nouns))
  for noun in nouns:
    synset_max = get_greatest_synset_similarity_between(synset, noun)
    if synset_max is not None:
      synsets_definition.append(synset_max)

  return synsets_definition


def get_dict_vectors_synsets_for_word(word):
  vectors = {}
  synsets = WordnetHandler.get_synsets_for_word(word, 'n')
  for synset in synsets:
    vector = get_definition_synset(synset)
    key = synset.definition()
    vectors[key] = vector

  return vectors
