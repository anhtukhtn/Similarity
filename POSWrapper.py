import nltk
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()

def pos_tag(tokens):
  return nltk.tag._pos_tag(tokens, None, tagger)