from nltk.stem import WordNetLemmatizer
import nltk
import POSWrapper


__wordnet_lemmatizer__ = WordNetLemmatizer()


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
  nouns_stemmed = []
  for noun in nouns:
    noun_stemmed = __wordnet_lemmatizer__.lemmatize(noun, pos='n')
    nouns_stemmed.append(noun_stemmed)

  return nouns_stemmed
