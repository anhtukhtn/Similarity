import OxParseDefinition
import WordnetParseDefinition
from scipy import spatial
import Util
import FileProcess
import WordnetHandler
import ParamsForDefinition as Parameters
import OxfordParser
import heapq
import CompareWithGold
import copy


def sim_for_synset_and_synsetvector(a_synset, vector):
  p_max = 0
  for synset in vector:
    p = a_synset.path_similarity(synset)
    if p > p_max:
      p_max = p

  return p_max


def vector_for_subvector_with_mixvector(subvector, mixvector):
  result_vector = []
  for synset in mixvector:
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


def sim_ox_wn_definition(word):
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectors_synsets_for_word(word)
  synsets_wn = WordnetHandler.get_synsets_for_word(word,'n')
  dict_vectors_ox = OxParseDefinition.get_dict_vectors_synsets_for_word(word, synsets_wn)

  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)

  m2d_sim = sim_wn_ox_vector(vectors_ox, vectors_wn)

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


__m2d_sim__ = {}


def sim_ox_wn_via_definition():

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

  while _current_step <= _max_step:
    sim_ox_wn_via_definition()
    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

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

#  global __continue
#  if __continue == 1:
#    return
#    _current_step = 1
#    _change_params_for_step(_current_step, _alpha)
#
  while _current_step <= _max_step:
    choice_1_COL_RANGE_FIRST()
    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

def choice_1_COL_RANGE_FIRST():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 10
  _current_step = 0

#  global __continue
#  if __continue == 1:
#    return
#    _current_step = 8
#    _change_params_for_step(_current_step, _alpha)
#    __continue = 1

  while _current_step <= _max_step:
    sim_ox_wn_via_definition()
    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()


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
#  global __continue
#  if __continue == 1:
#    # return
#    _current_step = 4
#    _change_params_for_step(_current_step, _alpha)
#
  while _current_step <= _max_step:
    choice_N_N_RANGE_FIRST()
    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()


def choice_N_N_RANGE_FIRST():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1.00
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 10
  _current_step = 0
#  global __continue
#  if __continue == 1:
#    _current_step = 3
#    _change_params_for_step(_current_step, _alpha)
#    __continue = 0
#
  while _current_step <= _max_step:
    sim_ox_wn_via_definition()
    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()


def train_sim_definition():
  Parameters.reset_params_zero()
  choice_1_1_MIN()
  choice_1_COL_MIN_FIRST()
  choice_N_N_MIN_FIRST()
