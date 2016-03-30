from nltk.util import ngrams
from nltk.metrics import jaccard_distance
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

def get_ngrams_for_sen(gloss, num_of_grams):
  gloss = gloss.replace("\\"," ")
  gloss = gloss.replace("-"," ")
  gloss = gloss.replace("/"," ")
  sen_gloss = gloss.split(".")
  ngrams_result = []
  for sen in sen_gloss:
    gloss_temp = ''.join([i for i in sen if (i.isalpha() or i == " ")])
    gloss_words = gloss_temp.split()
    gloss = ""
    for word in gloss_words:
      word = wordnet_lemmatizer.lemmatize(word)
      gloss += word + " "

    ngrams_string = ngrams(gloss.split(), num_of_grams)
    for gram in ngrams_string:
      ngrams_result.append(gram)

  return ngrams_result


def ngrams_word_for(sen_1, sen_2, n_grams):
  ngrams_1 = get_ngrams_for_sen(sen_1, n_grams)
  ngrams_2 = get_ngrams_for_sen(sen_2, n_grams)
  set_1 = set(ngrams_1)
  set_2 = set(ngrams_2)
  if len(set_1) == 0 or len(set_2) == 0:
    return 0.00001
  value = 1.00001 -  jaccard_distance(set_1, set_2)

  return value
