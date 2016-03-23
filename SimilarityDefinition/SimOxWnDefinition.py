import OxParseDefinition
import WordnetParseDefinition
from scipy import spatial
import Util
import WordnetHandler
import ParamsForDefinition as Parameters
import OxfordParser
import heapq
import CompareWithGold
import copy
import DebugHandler
import POSWrapper
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from nltk.corpus import stopwords

__stopwords__ = stopwords.words('english')

from nltk.metrics import jaccard_distance
wordnet_lemmatizer = WordNetLemmatizer()


def sim_for_synset_and_synsetvector(a_synset, vector):
  p_max = 0
  for (synset,weight) in vector:
    p = WordnetHandler.cal_similarity(a_synset, synset)
    if p is not None:
#      p = p*weight
      if p > p_max:
        p_max = p

  return p_max

#def sim_for_synset_and_synsetvector(a_synset, vector):
#  p_average = 0
#  for (synset,weight) in vector:
#    p = WordnetHandler.cal_similarity(a_synset, synset)
#    if p is not None:
#      p = p*weight
#      p_average += p
#
#  return p_average/(len(vector)+1)
#

def vector_for_subvector_with_mixvector(subvector, mixvector):
  result_vector = []
  for (synset,weight) in mixvector:
    result = sim_for_synset_and_synsetvector(synset, subvector)
    result_vector.append(result)

  return result_vector


def sim_2_vector(vector_1, vector_2):
  mix_vector = vector_1 + vector_2
  result_vector_1 = vector_for_subvector_with_mixvector(vector_1, mix_vector)
  result_vector_2 = vector_for_subvector_with_mixvector(vector_2, mix_vector)
  cosine = spatial.distance.cosine(result_vector_1, result_vector_2)
  sim_result = 1 - cosine

  return sim_result


def sim_wn_ox_vector(vectors_ox, vectors_wn):

  m2d_sim = [[0 for x in range(len(vectors_ox))] for x in range(len(vectors_wn))]
  for i in range(len(vectors_wn)):
    vector_wn = vectors_wn[i]
    for j in range(len(vectors_ox)):
      vector_ox = vectors_ox[j]
      m2d_sim[i][j] = sim_2_vector(vector_ox, vector_wn)

  return m2d_sim

def sim_wn_ox_vector_reduce(vectors_ox, vectors_wn, status):
  m2d_sim = [[0 for x in range(len(vectors_ox))] for x in range(len(vectors_wn))]
  for i in range(len(vectors_wn)):
    if status[i] == 1:
      vector_wn = vectors_wn[i]
      for j in range(len(vectors_ox)):
        vector_ox = vectors_ox[j]
        m2d_sim[i][j] = sim_2_vector(vector_ox, vector_wn)

  return m2d_sim


def choose_pair_0_1(matrix_similarity, num_rows, num_cols):
  if num_rows == 1 and num_cols == 1 and matrix_similarity[0][0] > Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN:
    matrix_similarity[0][0] = 1;

  if num_rows > 1 and num_cols == 1:
    col = []
    for iWnWord in range(num_rows):
      col.append(matrix_similarity[iWnWord][0])
    order = heapq.nlargest(2, range(num_rows), col.__getitem__);
    # print "1 col"
    # print order
    if matrix_similarity[order[0]][0] >= Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST*matrix_similarity[order[1]][0] or \
            matrix_similarity[order[0]][0] > Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST:
      matrix_similarity[order[0]][0] = 1;

  if num_rows >= 1 and num_cols > 1:
    for iWnWord in range(num_rows):
      order = heapq.nlargest(2, range(len(matrix_similarity[iWnWord])), matrix_similarity[iWnWord].__getitem__);

      if matrix_similarity[iWnWord][order[0]] >= Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST*matrix_similarity[iWnWord][order[1]] or\
              matrix_similarity[0][order[0]] > Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST:
        matrix_similarity[iWnWord][order[0]] = 1;

  return matrix_similarity


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
  #    if word not in __stopwords__:
      gloss += word + " "

    ngrams_string = ngrams(gloss.split(), num_of_grams)
    for gram in ngrams_string:
      ngrams_result.append(gram)

#  for gram in ngrams_result:
#    print gram

  return ngrams_result


def vector_sim_ngram_for_subngram_mixngram(ngrams_1, mix_ngrams, num_of_grams):
  result_ngram = []

  if num_of_grams == 1:
    for ngram in mix_ngrams:
      w1_1 = ngram
      result_sim = 0.0
      if len(ngrams_1) > 0:
        for ngram_1 in ngrams_1:
          w2_1 = ngram_1
          if w1_1 == w2_1:
            result_sim += 1

#        result_sim /= len(ngrams_1)
      result_ngram.append(result_sim)

  if num_of_grams == 2:
    for ngram in mix_ngrams:
      (w1_1, w1_2) = ngram
      result_sim = 0.0
      if len(ngrams_1) > 0:
        for ngram_1 in ngrams_1:
          (w2_1, w2_2) = ngram_1
          if w1_1 == w2_1 and w1_2 == w2_2:
            result_sim += 1

#        result_sim /= len(ngrams_1)
      result_ngram.append(result_sim)

  if num_of_grams == 3:
    for ngram in mix_ngrams:
      (w1_1, w1_2, w1_3) = ngram
      result_sim = 0.0
      if len(ngrams_1) > 0:
        for ngram_1 in ngrams_1:
          (w2_1, w2_2, w2_3) = ngram_1
          if (w1_1 == w2_1 and w1_2 == w2_2 and w1_3 == w2_3):
            result_sim += 1

      result_ngram.append(result_sim)

  if num_of_grams == 4:
    for ngram in mix_ngrams:
      (w1_1, w1_2, w1_3, w1_4) = ngram
      result_sim = 0.0
      if len(ngrams_1) > 0:
        for ngram_1 in ngrams_1:
          (w2_1, w2_2, w2_3, w2_4) = ngram_1
          if (w1_1 == w2_1 and w1_2 == w2_2 and w1_3 == w2_3 and w1_4 == w2_4):
            result_sim += 1

#        result_sim /= len(ngrams_1)
      result_ngram.append(result_sim)

  return result_ngram


def cal_sim_for_ngrams(ngrams_1, ngrams_2, num_of_grams):
  mix_ngrams = ngrams_1 + ngrams_2
  result_ngram_1 = vector_sim_ngram_for_subngram_mixngram(ngrams_1, mix_ngrams, num_of_grams)
  result_ngram_2 = vector_sim_ngram_for_subngram_mixngram(ngrams_2, mix_ngrams, num_of_grams)
  cosine = spatial.distance.cosine(result_ngram_1, result_ngram_2)
  sim_result = 1 - cosine
  return sim_result


def cal_sim_for_n_grams_feature(wn_ngrams_list, ox_ngrams_list, num_of_grams):
  m2d_simard = [[0 for x in range(len(ox_ngrams_list))] for x in range(len(wn_ngrams_list))]
  for i_wn in range(len(wn_ngrams_list)):
    wn_ngrams = wn_ngrams_list[i_wn]
    for i_ox in range(len(ox_ngrams_list)):
      ox_ngrams = ox_ngrams_list[i_ox]
      m2d_simard[i_wn][i_ox] = cal_sim_for_ngrams(wn_ngrams, ox_ngrams, num_of_grams)
  return m2d_simard


def cal_ngrams_by_jacc(wn_grams, ox_grams):

  matrix_similarity_jaccard = [[0 for x in range(len(ox_grams))] for x in range(len(wn_grams))];

  for iWnWord in range(len(wn_grams)):

    wn_set = set(wn_grams[iWnWord]);

    for iDictWord in range(len(ox_grams)):

      dict_set = set(ox_grams[iDictWord])
      matrix_similarity_jaccard[iWnWord][iDictWord] = 1 - jaccard_distance(wn_set,dict_set);

  return matrix_similarity_jaccard


def cal_n_grams_sim(word, wn_gloss, ox_gloss, num_of_grams):
  wn_ngrams = []
  for gloss in wn_gloss:
    ngrams_string = get_ngrams_for_sen(gloss, num_of_grams)
    wn_ngrams.append(list(ngrams_string))

  ox_ngrams = []
  for gloss in ox_gloss:
    ngrams_string = get_ngrams_for_sen(gloss, num_of_grams)
    ox_ngrams.append(list(ngrams_string))

#  m2d_ngrams = cal_sim_for_n_grams_feature(wn_ngrams, ox_ngrams, num_of_grams)
  m2d_ngrams = cal_ngrams_by_jacc(wn_ngrams, ox_ngrams)
  if num_of_grams == 2:
    __m2d_sim_2grams__[word] = m2d_ngrams
  if num_of_grams == 3:
    __m2d_sim_3grams__[word] = m2d_ngrams
  if num_of_grams == 4:
    __m2d_sim_4grams__[word] = m2d_ngrams



def cal_jacc_sim(word, wn_gloss, ox_gloss):
  matrix_similarity_jaccard = similarity_by_jaccard(ox_gloss, wn_gloss)
  __m2d_sim_jacc__[word] = matrix_similarity_jaccard


def cal_sim_ngrams(word):
  dict_gloss_wn = WordnetParseDefinition.get_gloss_for_jacc(word)
  (key_wn, wn_gloss) = Util.get_keys_values_of_dict(dict_gloss_wn)
  ox_gloss = OxfordParser.get_definitions_of_word_for_jacc(word)
  cal_n_grams_sim(word, wn_gloss, ox_gloss, 2)
  cal_n_grams_sim(word, wn_gloss, ox_gloss, 3)
  cal_n_grams_sim(word, wn_gloss, ox_gloss, 4)

  for i in range(len(wn_gloss)):
    wn_gloss[i] = wn_gloss[i].replace(word, "")
  for i in range(len(ox_gloss)):
    ox_gloss[i] = ox_gloss[i].replace(word, "")
  cal_jacc_sim(word, wn_gloss, ox_gloss)



def sim_ox_wn_defi_WDS_via_main_syns(word):
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectors_synsets_for_word(word)
  synsets_wn = WordnetHandler.get_synsets_for_word(word,'n')
  dict_vectors_ox = OxParseDefinition.get_dict_vectors_synsets_for_word(word, synsets_wn)
#
  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)
#
  m2d_sim = sim_wn_ox_vector(vectors_ox, vectors_wn)
#
  cal_sim_ngrams(word)

# write to file
#  # - - - - - - - - - - - - - - - - - - - - - - - - -
#  for i in range(len(keys_wn)):
#    m2d_sim[i].insert(0,keys_wn[i]);
#  # - - - - - - - - - - - - - - - - - - - - - - - - -
#  # row
#  row_dict = [];
#  row_dict.append(word);
#  for i in range(len(keys_ox)):
#    row_dict.append(keys_ox[i].encode('utf8'));
#  # - - - - - - - - - - - - - - - - - - - - - - - - -
#  filename = 'Results/vector_definition/' + word + '.csv'
#  FileProcess.append_to_excel_file(filename, row_dict, m2d_sim)
#  # - - - - - - - - - - - - - - - - - - - - - - - - -

  return m2d_sim


def sim_ox_wn_defi_WDS_via_defi_of_curr_main_syn(word):
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectors_synsets_for_word(word)
  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)

  dict_vectors_wn_defi = WordnetParseDefinition.get_vectors_defi_for_word(word)
  (keys_wn_defi, vectors_wn_defi) = Util.get_keys_values_of_dict(dict_vectors_wn_defi)


  definitions = OxfordParser.get_definitions_of_word(word)

  m2d_sim = [[0 for x in range(len(definitions))] for x in range(len(vectors_wn))]

  for i in range(len(vectors_wn)):
    vector_wn = vectors_wn[i]
    vector_wn_defi = vectors_wn_defi[i]

    dict_vectors_ox = OxParseDefinition.get_dict_vectors_synsets_for_word(word, vector_wn_defi)
    (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)

    for j in range(len(vectors_ox)):
      vector_ox = vectors_ox[j]
      m2d_sim[i][j] = sim_2_vector(vector_ox, vector_wn)

  cal_sim_ngrams(word)

  return m2d_sim


def sim_ox_wn_defi_WDS_via_curr_main_syn(word):
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectors_synsets_for_word(word)
  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)
  synsets_wn = WordnetHandler.get_synsets_for_word(word, 'n')

  definitions = OxfordParser.get_definitions_of_word(word)

  m2d_sim = [[0 for x in range(len(definitions))] for x in range(len(vectors_wn))]

  for i in range(len(vectors_wn)):
    vector_wn = vectors_wn[i]

    dict_vectors_ox = OxParseDefinition.get_dict_vectors_synsets_for_word(word, [synsets_wn[i]])
    (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)

    for j in range(len(vectors_ox)):
      vector_ox = vectors_ox[j]
      m2d_sim[i][j] = sim_2_vector(vector_ox, vector_wn)

  cal_sim_ngrams(word)

  return m2d_sim


def sim_ox_wn_defi_WDS_via_align(word):
  words_wn = WordnetParseDefinition.get_dict_vectors_words_for_word(word)
  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(words_wn)
  words_ox = OxParseDefinition.get_dict_vectors_word_for_word(word)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(words_ox)

  synsets_wn = WordnetHandler.get_synsets_for_word(word, 'n')

  m2d_sim = [[0 for x in range(len(keys_ox))] for x in range(len(keys_wn))]

  for i in range(len(keys_wn)):
    vector_wn = vectors_wn[i]
    synset_wn = synsets_wn[i]
    for j in range(len(keys_ox)):
      vector_ox = vectors_ox[j]
      m2d_sim[i][j] = WordnetHandler.sim_for_words_words_no_order(vector_ox, vector_wn, synset_wn)
#      (vector_1, vector_2) = WordnetHandler.get_nearest_synsets_words_words_noorder(vector_ox, vector_wn)
#      m2d_sim[i][j] = sim_2_vector(vector_1, vector_2)

  cal_sim_ngrams(word)

  return m2d_sim



def sim_ox_wn_defi_WDS_via_align_all(word):
  words_wn = WordnetParseDefinition.get_dict_vectors_words_for_word(word)
  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(words_wn)
  words_ox = OxParseDefinition.get_dict_vectors_word_for_word(word)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(words_ox)

  m2d_sim = [[0 for x in range(len(keys_ox))] for x in range(len(keys_wn))]

  for i in range(len(keys_wn)):
    vector_wn = vectors_wn[i]
    words_ox = []
    for j in range(len(keys_ox)):
      words_ox += vectors_ox[j]
    synsets_wn = WordnetHandler.get_nearest_synsets_words_words_order(vector_wn, words_ox)

    for j in range(len(keys_ox)):
      synsets_ox = WordnetHandler.get_nearest_synsets_words_synsets_order(vectors_ox[j], synsets_wn)
      m2d_sim[i][j] = sim_2_vector(synsets_wn, synsets_ox)

  cal_sim_ngrams(word)

  return m2d_sim

__m2d_sim__ = {}

__m2d_sim_jacc__ = {}
__m2d_sim_2grams__ = {}
__m2d_sim_3grams__ = {}
__m2d_sim_4grams__ = {}

def sim_ox_wn_defi_WDS_via_1_main_syn(word):
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectors_synsets_for_word(word)
  synsets_wn = WordnetHandler.get_synsets_for_word(word,'n')
  dict_vectors_ox = OxParseDefinition.get_dict_vectors_synsets_for_word(word, synsets_wn)

  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)

  m2d_sim = sim_wn_ox_vector(vectors_ox, vectors_wn)

  return m2d_sim


def sim_ox_wn_mix(word):
  result_1 = sim_ox_wn_defi_WDS_via_curr_main_syn(word)
  result_2 = sim_ox_wn_defi_WDS_via_main_syns(word)
  result_3 = sim_ox_wn_defi_WDS_via_defi_of_curr_main_syn(word)
  if result_1 == None or len(result_1) == 0 or len(result_1[0]) == 0:
      return result_1

  result = [[0 for x in range(len(result_1[0]))] for x in range(len(result_1))]
  for i in range(len(result_1)):
    for j in range(len(result_1[i])):
       result[i][j] = result_1[i][j] + result_2[i][j] + result_3[i][j]
       result[i][j] = result[i][j]/3.0

  return result


def sim_ox_wn_value_main_synsets(word):
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectors_value_for(word)
  synsets_wn = WordnetHandler.get_synsets_for_word(word,'n')
  dict_vectors_ox = OxParseDefinition.get_vectors_value_for_word(word, synsets_wn)

  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)

  m2d_sim_defi_temp =  sim_ox_wn_defi_WDS_via_main_syns(word)
  DebugHandler.print_2d_matrix(m2d_sim_defi_temp)

  m2d_sim_defi = [[0 for x in range(len(vectors_wn))] for x in range(len(vectors_ox))]
  for i in range(len(vectors_wn)):
    for j in range(len(vectors_ox)):
      m2d_sim_defi[j][i] = m2d_sim_defi_temp[i][j]

  m2d_sim = [[0 for x in range(len(vectors_ox))] for x in range(len(vectors_wn))]
  for i in range(len(vectors_wn)):
    vector_wn = vectors_wn[i]
    print vector_wn
    for j in range(len(vectors_ox)):
      vector_ox = vectors_ox[j]
      cosine = spatial.distance.cosine(m2d_sim_defi[j], vector_wn)
      m2d_sim[i][j] = cosine

  print "\n"
  for j in range(len(vectors_ox)):
    vector_ox = vectors_ox[j]
    print vector_ox
  return m2d_sim


def sim_ox_wn_definition(word):
#  result = sim_ox_wn_defi_WDS_via_curr_main_syn(word)
#  result = sim_ox_wn_defi_WDS_via_main_syns(word)
#  result = sim_ox_wn_defi_WDS_via_defi_of_curr_main_syn(word)
#  result = sim_ox_wn_mix(word)
#  result = sim_ox_wn_defi_WDS_via_1_main_syn(word)
#  result = sim_ox_wn_value_main_synsets(word)
#  result = sim_ox_wn_defi_WDS_via_align(word)
  result = sim_ox_wn_defi_WDS_via_align_all(word)

  return result


def sim_ox_wn_via_definition_cal_word():

  total_precision = 0;
  total_recall = 0;
  total_accuracy = 0;
  total_word = 0

  dict_ox = OxfordParser.get_dict_nouns()
  for word in dict_ox:

    if word not in __m2d_sim__:
      m2d_sim = sim_ox_wn_definition(word)
      __m2d_sim__[word] = m2d_sim

    m2d_sim = copy.deepcopy(__m2d_sim__[word])

    if m2d_sim == None or len(m2d_sim) == 0 or len(m2d_sim[0]) == 0:
      continue

    print word
#
#    if len(m2d_sim) == 1 and len(m2d_sim[0]) == 1:
#      continue
#
    m2d_sim = choose_pair_0_1(m2d_sim, len(m2d_sim), len(m2d_sim[0]))

    (precision, recall, accuracy) = CompareWithGold.compareGoldWithResult(m2d_sim,word)
    if precision != -1:
      total_precision += precision
      total_recall += recall
      total_accuracy += accuracy
      total_word += 1

  precision = total_precision/total_word
  recall = total_recall/total_word
  f_score = 0
  if precision != 0 or recall != 0:
    f_score = 2*(precision*recall)/(precision + recall)
  accuracy = total_accuracy/total_word
  print "total:"
  print total_word
  print precision
  print recall
  print f_score
  print accuracy

  Parameters.append_result_to_file( precision, recall, f_score, accuracy)


def count_pair(m2d):
  pair = 0
  for i in range(len(m2d)):
    for j in range(len(m2d[i])):
      if m2d[i][j] == 1:
        pair += 1

  return pair


def reducing_m2d_sim(m2d_sim, status_synsets):
  updated = 0
  num_rows = len(m2d_sim)
  num_cols = len(m2d_sim[0])
  if num_rows >= 1 and num_cols > 1:
    for iWnWord in range(num_rows):
      if status_synsets[iWnWord] == 1:
        order = heapq.nlargest(2, range(len(m2d_sim[iWnWord])), m2d_sim[iWnWord].__getitem__);

        if m2d_sim[iWnWord][order[0]] >= Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST*m2d_sim[iWnWord][order[1]] or\
                m2d_sim[0][order[0]] > Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST:
          m2d_sim[iWnWord][order[0]] = 1;
          status_synsets[iWnWord] = 0
          updated = 1
  return updated

def create_status_array(synsets_wn):
  status = []
  for i in range(len(synsets_wn)):
    status.append(1)
  return status


def match_matrix_sim_with_temp_matrix(m2d_sim, temp_m2d):
  for i in range(len(m2d_sim)):
    for j in range(len(m2d_sim[0])):
      if temp_m2d[i][j] == 1:
        m2d_sim[i][j] = 1


def pair_0_1_reducing_m2d_sim(matrix_similarity, num_rows, num_cols, word):

  if num_rows == 1 and num_cols == 1 and matrix_similarity[0][0] > Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN:
      matrix_similarity[0][0] = 1;

  if num_rows > 1 and num_cols == 1:
    col = []
    for iWnWord in range(num_rows):
      col.append(matrix_similarity[iWnWord][0])
    order = heapq.nlargest(2, range(num_rows), col.__getitem__);
    if matrix_similarity[order[0]][0] >= Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST*matrix_similarity[order[1]][0] or \
            matrix_similarity[order[0]][0] > Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST:
      matrix_similarity[order[0]][0] = 1;

  if num_rows >= 1 and num_cols > 1:
    synsets_wn = WordnetHandler.get_synsets_for_word(word,'n')
    status_synsets = create_status_array(synsets_wn)
    updated = reducing_m2d_sim(matrix_similarity, status_synsets)
    while updated == 1:
      m2d = sim_ox_wn_defi_WDS_via_main_syns_for_reduce(synsets_wn, status_synsets, word)
      updated = reducing_m2d_sim(m2d, status_synsets)
      match_matrix_sim_with_temp_matrix(matrix_similarity, m2d)

  return matrix_similarity


def sim_ox_wn_defi_WDS_via_main_syns_for_reduce(synsets_wn, status_synsets_wn, word):
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectores_synsets_for_synsets(synsets_wn)
  synsets_reduce_wn = list(synsets_wn)
  for i in reversed(range(len(synsets_reduce_wn))):
    if status_synsets_wn[i] == 0:
      del synsets_reduce_wn[i]

  dict_vectors_ox = OxParseDefinition.get_dict_vectors_synsets_for_word(word, synsets_reduce_wn)

  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)

  m2d_sim = sim_wn_ox_vector_reduce(vectors_ox, vectors_wn, status_synsets_wn)

  return m2d_sim


def similarity_by_jaccard(ox_defis, wn_defis):

  matrix_similarity_jaccard = [[0 for x in range(len(ox_defis))] for x in range(len(wn_defis))];

  for iWnWord in range(len(wn_defis)):

    tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wn_defis[iWnWord]));
    words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

    # words = nltk.wordpunct_tokenize(wn.synset(wn_defis[iWnWord].name()).definition());
    # print words
    for i in range(len(words)):
      words[i] = wordnet_lemmatizer.lemmatize(words[i]);
    wn_set = set(words);
#    print "\n"
#    print wn_set
    # wn_set = set(wn.synset(wn_defis[iWnWord].name()).definition().split())
    # print wn_set

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(ox_defis)):

#      if not ox_defis[str(iDictWord)].has_key("d") or dict_words[str(iDictWord)]["d"] == None:
#        matrix_similarity_jaccard[iWnWord][iDictWord] = 1;
#        continue

      tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(ox_defis[iDictWord]));
      words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

      # words = nltk.wordpunct_tokenize(ox_defis[str(iDictWord)]["d"]);
      # print words
      for i in range(len(words)):
        words[i] = wordnet_lemmatizer.lemmatize(words[i]);
      dict_set = set(words);
#      print dict_set
      # print
      # dict_set = set(ox_defis[str(iDictWord)]["d"].encode('utf8').split());
      matrix_similarity_jaccard[iWnWord][iDictWord] = 1 - jaccard_distance(wn_set,dict_set);
#      matrix_similarity_jaccard[iWnWord][iDictWord] = cal_jacc_for_ngrams(wn_set, dict_set, 1)

  ########################################
  return matrix_similarity_jaccard


def sim_ox_wn_via_definition_cal_syns():
  total_tp = 0.;
  total_tn = 0.;
  total_fn = 0.0;
  total_fp = 0.0;
  total_pair = 0

  dict_ox = OxfordParser.get_dict_nouns()
  for word in dict_ox:
#    if word != 'bank':
#      continue
#
    if word not in __m2d_sim__:
      m2d_sim = sim_ox_wn_definition(word)
      __m2d_sim__[word] = m2d_sim

    m2d_sim = copy.deepcopy(__m2d_sim__[word])

    if m2d_sim == None or len(m2d_sim) == 0 or len(m2d_sim[0]) == 0:
      continue

#    if len(m2d_sim) == 1 and len(m2d_sim[0]) == 1:
#      continue
#
    m2d_sim = choose_pair_0_1(m2d_sim, len(m2d_sim), len(m2d_sim[0]))
#    m2d_sim = pair_0_1_reducing_m2d_sim(m2d_sim, len(m2d_sim), len(m2d_sim[0]), word)
#    print word

    pair = count_pair(m2d_sim)
    total_pair += pair

    (tp, tn, fn, fp) = CompareWithGold.compareGoldWithResult_without_cal_result(m2d_sim,word)
    if tp != -1:
      total_tp += tp
      total_tn += tn
      total_fn += fn
      total_fp += fp

  precision = total_tp / (total_tp + total_fp)
  recall = total_tp / (total_tp + total_fn)
  accuracy = (total_tp + total_tn) / (total_tp + total_tn + total_fp + total_fn)

  f_score = 0
  if precision != 0 or recall != 0:
    f_score = 2*(precision*recall)/(precision + recall)
  print "total:"
  print total_pair
  print total_tp
  print total_tn
  print total_fn
  print total_fp

  print precision
  print recall
  print f_score
  print accuracy

  Parameters.append_result_to_file( precision, recall, f_score, accuracy)
  current_params = Parameters.get_current_params()
  current_params = copy.deepcopy(current_params)
  return f_score, current_params


__dict_ngrams__ = {}


def sim_ox_wn_via_definition_morpho_cal_syns():
  total_tp = 0.00001
  total_tn = 0.00001;
  total_fn = 0.00001;
  total_fp = 0.00001;
  total_pair = 0

  dict_ox = OxfordParser.get_dict_nouns()
  for word in dict_ox:
#    if word != 'blaze':
#      continue
#
    if word not in __m2d_sim__:
      m2d_sim = sim_ox_wn_definition(word)
      __m2d_sim__[word] = m2d_sim

    m2d_sim = copy.deepcopy(__m2d_sim__[word])
    if m2d_sim == None or len(m2d_sim) == 0 or len(m2d_sim[0]) == 0:
      continue

#    if len(m2d_sim) == 1 or len(m2d_sim[0]) == 1:
#      continue

    if word not in __dict_ngrams__:
      m2d_jacc = __m2d_sim_jacc__[word]
      m2d_2grams = __m2d_sim_2grams__[word]
      m2d_3grams = __m2d_sim_3grams__[word]
      m2d_4grams = __m2d_sim_4grams__[word]
#      DebugHandler.print_2d_matrix(m2d_jacc)
#      DebugHandler.print_2d_matrix(m2d_2grams)
#      DebugHandler.print_2d_matrix(m2d_3grams)
#      DebugHandler.print_2d_matrix(m2d_4grams)
  #
      m2d_ngrams = [[0 for x in range(len(m2d_sim[0]))] for x in range(len(m2d_sim))]

      monogram_weight = 0.25
      bigram_weight = 0.25
      trigram_weight = 0.25
      for i in range(len(m2d_sim)):
        for j in range(len(m2d_sim[0])):
          m2d_ngrams[i][j] = m2d_jacc[i][j]*monogram_weight \
                              + m2d_2grams[i][j]*bigram_weight \
                              + m2d_3grams[i][j]*(trigram_weight) \
                              + m2d_4grams[i][j]*(1- monogram_weight - bigram_weight - trigram_weight)
      __dict_ngrams__[word] = m2d_ngrams

#    print word

    m2d_ngrams = __dict_ngrams__[word]

#    DebugHandler.print_2d_matrix(m2d_ngrams)
#    DebugHandler.print_2d_matrix(m2d_sim)

#    ngram_weight = 0.075
#    for iWnWord in range(len(m2d_sim)):
#      for iDictWord in range(len(m2d_sim[0])):
#        jacc = m2d_jacc[iWnWord][iDictWord]
#        ngrams = m2d_ngrams[iWnWord][iDictWord]
#        m2d_jacc[iWnWord][iDictWord] = jacc*(1-ngram_weight) + ngrams*ngram_weight
#
    JACCARD_WEIGHT = Parameters.MORPHO.JACCARD
    for i in range(len(m2d_sim)):
      for j in range(len(m2d_sim[0])):
        m2d_sim[i][j] = m2d_sim[i][j]*(1-JACCARD_WEIGHT) + JACCARD_WEIGHT*(m2d_ngrams[i][j]);

#    DebugHandler.print_2d_matrix(m2d_sim)
#    if len(m2d_sim) == 1 and len(m2d_sim[0]) == 1:
#      continue
#
    m2d_sim = choose_pair_0_1(m2d_sim, len(m2d_sim), len(m2d_sim[0]))
#    m2d_sim = pair_0_1_reducing_m2d_sim(m2d_sim, len(m2d_sim), len(m2d_sim[0]), word)
#    print word
#    DebugHandler.print_2d_matrix(m2d_sim)

    pair = count_pair(m2d_sim)
    total_pair += pair

    (tp, tn, fn, fp) = CompareWithGold.compareGoldWithResult_without_cal_result(m2d_sim,word)

#    precision = tp / (tp + fp + 0.0001)
#    recall = tp / (tp + fn + 0.0001)
#    accuracy = (tp + tn) / (tp + tn + fp + fn + 0.0001)
#
#    f_score = 0
#    if precision != 0 or recall != 0:
#      f_score = 2*(precision*recall)/(precision + recall)
#    if f_score < 0.5:
#      print word
#      print f_score
#      print tp
#      print tn
#      print fn
#      print fp
#
    if tp != -1:
      total_tp += tp
      total_tn += tn
      total_fn += fn
      total_fp += fp

  precision = total_tp / (total_tp + total_fp)
  recall = total_tp / (total_tp + total_fn)
  accuracy = (total_tp + total_tn) / (total_tp + total_tn + total_fp + total_fn)

  f_score = 0
  if precision != 0 or recall != 0:
    f_score = 2*(precision*recall)/(precision + recall)
  print "total:"
  print total_pair
  print total_tp
  print total_tn
  print total_fn
  print total_fp

  print precision
  print recall
  print f_score
  print accuracy

  Parameters.append_result_to_file( precision, recall, f_score, accuracy)
  current_params = Parameters.get_current_params()
  current_params = copy.deepcopy(current_params)
  return f_score, current_params



def sim_ox_wn_via_definition():
#  result = sim_ox_wn_via_definition_cal_syns()
  result = sim_ox_wn_via_definition_morpho_cal_syns()

  return result


def choice_1_1_MIN():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 20
  _current_step = 0

  f_score = 0
  current_params = []

  while _current_step <= _max_step:
    (cur_f_score, cur_params) = sim_ox_wn_via_definition()
    if cur_f_score > f_score:
      f_score = cur_f_score
      current_params = cur_params

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

  return f_score, current_params

def choice_1_COL_MIN_FIRST():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = 0.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 20
  _current_step = 0

  f_score = 0
  current_params = []

#  global __continue
#  if __continue == 1:
#    return
#    _current_step = 1
#    _change_params_for_step(_current_step, _alpha)
#
  while _current_step <= _max_step:
    (cur_f_score, cur_params) = choice_1_COL_RANGE_FIRST()
    if cur_f_score > f_score:
      f_score = cur_f_score
      current_params = cur_params


    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

  return f_score, current_params

def choice_1_COL_RANGE_FIRST():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 20
  _current_step = 0

  f_score = 0
  current_params = []

#  global __continue
#  if __continue == 1:
#    return
#    _current_step = 8
#    _change_params_for_step(_current_step, _alpha)
#    __continue = 1

  while _current_step <= _max_step:

    (cur_f_score, cur_params) = sim_ox_wn_via_definition()
    if cur_f_score > f_score:
      f_score = cur_f_score
      current_params = cur_params

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

  return f_score, current_params

def choice_N_N_MIN_FIRST():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = 0.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 20
  _current_step = 0

  f_score = 0
  current_params = []

#  global __continue
#  if __continue == 1:
#    # return
#    _current_step = 4
#    _change_params_for_step(_current_step, _alpha)
#
  while _current_step <= _max_step:
    (cur_f_score, cur_params) = choice_N_N_RANGE_FIRST()
    if cur_f_score > f_score:
      f_score = cur_f_score
      current_params = cur_params

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

  return f_score, current_params

def choice_N_N_RANGE_FIRST():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1.00
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 20
  _current_step = 0

  f_score = 0
  current_params = []

#  global __continue
#  if __continue == 1:
#    _current_step = 3
#    _change_params_for_step(_current_step, _alpha)
#    __continue = 0
#
  while _current_step <= _max_step:
    (cur_f_score, cur_params) = sim_ox_wn_via_definition()
    if cur_f_score > f_score:
      f_score = cur_f_score
      current_params = cur_params

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

  return f_score, current_params


def jaccard_train():
  def _reset_params():
    Parameters.MORPHO.JACCARD = 0.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.MORPHO.JACCARD += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 20
  _current_step = 10

  f_score = 0
  current_params = []

#  global __continue
#  if __continue == 1:
#    return
#    _current_step = 1
#    _change_params_for_step(_current_step, _alpha)
#
  while _current_step <= _max_step:
#    (ch_1_1_f_score, ch_1_1_paramas) = choice_1_1_MIN()
    (ch_1_n_f_score, ch_1_n_paramas) = choice_1_COL_MIN_FIRST()
    (ch_n_n_f_score, ch_n_n_paramas) = choice_N_N_MIN_FIRST()

    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = ch_1_n_paramas[1]
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = ch_1_n_paramas[2]
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = ch_n_n_paramas[3]
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = ch_n_n_paramas[4]

    (cur_f_score, cur_params) = sim_ox_wn_via_definition()

    if cur_f_score > f_score:
      f_score = cur_f_score
      current_params = cur_params

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

  return f_score, current_params


def train_sim_definition():
  Parameters.reset_params_zero()
  (f_score, curr_params) = jaccard_train()

  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = curr_params[0]
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = curr_params[1]
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = curr_params[2]
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = curr_params[3]
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = curr_params[4]
  Parameters.MORPHO.JACCARD = curr_params[5]
#
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = 0.0
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1.0
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = 1
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1.25
#  Parameters.MORPHO.JACCARD = 0.9
#

  sim_ox_wn_via_definition()


def print_gold_pair():
  gold_data = CompareWithGold.goldData
  total_count = 0
  for (key, m2d) in gold_data.items():
    for i in range(len(m2d)):
      for j in range(len(m2d[i])):
        if m2d[i][j] == "1":
          total_count += 1

  print len(gold_data)
  print total_count
