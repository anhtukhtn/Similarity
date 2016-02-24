import nltk
from nltk.stem import WordNetLemmatizer
import POSWrapper
import WordnetHandler


__wordnet_lemmatizer__ = WordNetLemmatizer()


def check_pos_noun(pos):
  return (pos == 'NN' or pos == 'NNS' or pos == 'JJ')


def preprocess_sentence_to_nouns(sentence):
  tokens = nltk.wordpunct_tokenize(sentence)
  tagged_words = POSWrapper.pos_tag(tokens)
  nouns = [word for word, pos in tagged_words if check_pos_noun(pos)]
  return nouns


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


def get_definition_synsets(synset):
  definition_synsets = []
  definition = synset.definition()
  nouns = preprocess_sentence_to_nouns(definition)
  for noun in nouns:
    synset_max = get_greatest_synset_similarity_between(synset, noun)
    if synset_max is not None:
      definition_synsets.append(synset_max)

  return definition_synsets
