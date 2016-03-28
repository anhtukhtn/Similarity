# -*- coding: utf-8 -*-

import OxfordParser
import CompareWithGold
import ParamsSVM as Parameters
import heapq
import WordnetHandler
import ReadSVMResult
import copy
import DebugHandler


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


def get_m2d_sim_for_word_from_svm_result(word):
  defis_wn = WordnetHandler.get_definitions_for_word(word)
  defis_ox = OxfordParser.get_definitions_of_word_for_svm(word)

  if len(defis_wn) == 0 or len(defis_ox) == 0:
    return None

  m2d_sim = [[0 for x in range(len(defis_ox))] for x in range(len(defis_wn))]

  for i_wn in range(len(defis_wn)):
    defi_wn = str(defis_wn[i_wn])
    for i_ox in range(len(defis_ox)):
      defi_ox = str(defis_ox[i_ox])
      m2d_sim[i_wn][i_ox] = ReadSVMResult.get_sim_for_sens(defi_wn, defi_ox)

  return m2d_sim


def count_pair(m2d):
  pair = 0
  for i in range(len(m2d)):
    for j in range(len(m2d[i])):
      if m2d[i][j] == 1:
        pair += 1

  return pair


def sim_ox_wn_via_svm():
  total_tp = 0.00001
  total_tn = 0.00001
  total_fn = 0.00001
  total_fp = 0.00001
  total_pair = 0

  dict_ox = OxfordParser.get_dict_nouns()
  flag_can_go = False
  for word in dict_ox:

    if word == "blockage":
      flag_can_go = True

    if flag_can_go == False:
      continue

    word_syns_ox = dict_ox[word]
    wn_synsets = WordnetHandler.get_synsets_for_word(word, "n")

    m2d_sim = [[0 for x in range(len(word_syns_ox))] for x in range(len(wn_synsets))]

    if len(word_syns_ox) == 1 and len(wn_synsets) == 1:
      m2d_sim[0][0] = 1
    else:
      m2d_sim = get_m2d_sim_for_word_from_svm_result(word)

    if m2d_sim == None:
      continue

#    DebugHandler.print_2d_matrix(m2d_sim)

    m2d_sim = choose_pair_0_1(m2d_sim, len(m2d_sim), len(m2d_sim[0]))
#    DebugHandler.print_2d_matrix(m2d_sim)

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

def choice_1_1_MIN():
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 1
  _current_step = 0

  f_score = 0
  current_params = []

  while _current_step <= _max_step:
    (cur_f_score, cur_params) = sim_ox_wn_via_svm()
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
  _max_step = 40
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

    (cur_f_score, cur_params) = sim_ox_wn_via_svm()
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
  _max_step = 40
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
    (cur_f_score, cur_params) = sim_ox_wn_via_svm()
    if cur_f_score > f_score:
      f_score = cur_f_score
      current_params = cur_params

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

  return f_score, current_params


def train_sim_definition():
  Parameters.reset_params_zero()
  (ch_1_n_f_score, ch_1_n_paramas) = choice_1_COL_MIN_FIRST()
  (ch_n_n_f_score, ch_n_n_paramas) = choice_N_N_MIN_FIRST()

  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = ch_1_n_paramas[1]
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = ch_1_n_paramas[2]
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = ch_n_n_paramas[3]
  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = ch_n_n_paramas[4]
#
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = 0.0
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1.0
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = 1
#  Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1.25
#
  sim_ox_wn_via_svm()
