import nltk
import POSWrapper
from nltk.stem import WordNetLemmatizer


__wordnet_lemmatizer__ = WordNetLemmatizer()


def pos_is_noun(pos):
  return (pos == 'NN' or pos == 'NNS' or pos == 'JJ')


def pos_is_verb(pos):
  return (pos == 'VB' or pos == 'VBD' or pos == 'VBN')


def check_pos(pos):
  return (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == 'VB' or pos == 'VBD' or pos == 'VBN')

def check_pos_noun(pos):
  return (pos == 'NN' or pos == 'NNS' or pos == 'JJ')


def preprocess_sentence_to_nouns(sentence):
  # tokenize
  tokens = nltk.wordpunct_tokenize(sentence)
  # pos tag
  tagged_words = POSWrapper.pos_tag(tokens)
  # get n
  nouns = [word for word, pos in tagged_words if check_pos_noun(pos)]
  # stemming
#  nouns_stemmed = []
#  for noun in nouns:
#    noun_stemmed = __wordnet_lemmatizer__.lemmatize(noun, pos='n')
#    nouns_stemmed.append(noun_stemmed)
#
  return nouns

def preprocess_sentence(sentence):
  # tokenize
  tokens = nltk.wordpunct_tokenize(sentence)
  # pos tag
  tagged_words = POSWrapper.pos_tag(tokens)
  # get n
  nouns = [(word, pos) for word, pos in tagged_words if check_pos(pos)]
  # stemming
#  nouns_stemmed = []
#  for noun in nouns:
#    (word, pos) = noun
#    if pos_is_noun(pos):
#      noun_stemmed = __wordnet_lemmatizer__.lemmatize(word, pos='n')
#      nouns_stemmed.append(noun_stemmed)
#    if pos_is_verb(pos):
#      noun_stemmed = __wordnet_lemmatizer__.lemmatize(word, pos='v')
#      nouns_stemmed.append(noun_stemmed)
#
  return nouns
