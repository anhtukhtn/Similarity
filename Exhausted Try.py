__author__ = 'tu'

import SimilarityWordnetOxford
import OxfordParser
import Parameters

dict_ox_nouns = OxfordParser.readOxfordNouns();

__continue = 1

def feature_wn(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_definition = 1
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 0
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = 0
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = 0
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = 0
  def _change_params_for_step(cur_step):
    _reset_params()
    if cur_step == 1:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 1
    elif cur_step == 2:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = 1
    elif cur_step == 3:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = 1
    elif cur_step == 4:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = 1
    elif cur_step == 5:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = 1
    elif cur_step == 6:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = 1
    elif cur_step == 7:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = 1
    elif cur_step == 8:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = 1
    elif cur_step == 9:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = 1
    elif cur_step == 10:
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = 1
      Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = 1


  _reset_params()
  _max_step = 10
  _current_step = 0

  while _current_step <= _max_step:
    # SimilarityWordnetOxford.similarityWords(dict_nouns)

    feature_dict(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step)

  _reset_params()

def feature_dict(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_sd = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_d = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 0
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 0
  def _change_params_for_step(cur_step):
    _reset_params()
    if cur_step == 1:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 1
    elif cur_step == 2:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 1
    elif cur_step == 3:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 1
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 1

  _reset_params()
  _max_step = 3
  _current_step = 0

  while _current_step <= _max_step:
    # SimilarityWordnetOxford.similarityWords(dict_nouns)

    feature_POS(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step)

  _reset_params()

def feature_POS(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.POS_FEATURE_n = 1
    Parameters.PARAMETERS.POS_FEATURE_v = 0
  def _change_params_for_step(cur_step):
    _reset_params()
    if cur_step == 1:
      Parameters.PARAMETERS.POS_FEATURE_v = 1

  _reset_params()
  _max_step = 1
  _current_step = 0

  while _current_step <= _max_step:
    # SimilarityWordnetOxford.similarityWords(dict_nouns)

    nbest_similarity(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step)

  _reset_params()

def nbest_similarity(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.N_BEST_CALCULATE_SIMILARITY = 1
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS.N_BEST_CALCULATE_SIMILARITY += cur_step*alpha

  _reset_params()
  _alpha = 1
  _max_step = 8
  _current_step = 0

  while _current_step <= _max_step:
    # SimilarityWordnetOxford.similarityWords(dict_nouns)

    jaccard_weight(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step,_alpha)

  _reset_params()


def jaccard_weight(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.JACCARD_WEIGHT = 0.00
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS.JACCARD_WEIGHT += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 8
  _current_step = 0

  while _current_step <= _max_step:
    # SimilarityWordnetOxford.similarityWords(dict_nouns)

    choice_1_1_MIN(dict_nouns)
    choice_1_COL_MIN_FIRST(dict_nouns)
    choice_N_N_MIN_FIRST(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step,_alpha)

  _reset_params()

def choice_1_1_MIN(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 8
  _current_step = 0

  if __continue == 1:
    return

  while _current_step <= _max_step:
    SimilarityWordnetOxford.similarityWords(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

def choice_1_COL_MIN_FIRST(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = 0.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 8
  _current_step = 0

  global __continue
  if __continue == 1:
    __continue = 0
    return

  while _current_step <= _max_step:
    # SimilarityWordnetOxford.similarityWords(dict_nouns)

    choice_1_COL_RANGE_FIRST(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()

def choice_1_COL_RANGE_FIRST(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 8
  _current_step = 0

  while _current_step <= _max_step:
    SimilarityWordnetOxford.similarityWords(dict_nouns)
    _current_step += 1

    _change_params_for_step(_current_step, _alpha)

  _reset_params()


def choice_N_N_MIN_FIRST(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = 0.00
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.05
  _max_step = 8
  _current_step = 0

  while _current_step <= _max_step:
    # SimilarityWordnetOxford.similarityWords(dict_nouns)

    choice_N_N_RANGE_FIRST(dict_nouns)

    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()


def choice_N_N_RANGE_FIRST(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1.00
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.5
  _max_step = 8
  _current_step = 0

  while _current_step <= _max_step:
    SimilarityWordnetOxford.similarityWords(dict_nouns)
    _current_step += 1
    _change_params_for_step(_current_step, _alpha)

  _reset_params()


feature_wn(dict_ox_nouns)
