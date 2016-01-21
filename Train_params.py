__author__ = 'tu'
import SimilarityWordnetOxford
import OxfordParser
import Parameters
import random
import WriteParametersAndResult

dict_ox_nouns = OxfordParser.readOxfordNouns();

def jaccard_weight(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.JACCARD_WEIGHT = 0.01
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS.JACCARD_WEIGHT += cur_step*alpha

  _reset_params()
  _alpha = 0.02
  _max_step = 10
  _current_step = 0

  _best_result = 0
  _best_params = Parameters.get_current_params()

  while _current_step <= _max_step:
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()
    _current_step += 1

    _change_params_for_step(_current_step,_alpha)

  _reset_params()
  return (_best_result,_best_params)

def choice_1_COL_RANGE_FIRST(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1.01
  def _change_params_for_step(cur_step,alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.02
  _max_step = 10
  _current_step = 0

  _best_result = 0
  _best_params = Parameters.get_current_params()

  while _current_step <= _max_step:
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()
    _current_step += 1

    _change_params_for_step(_current_step, _alpha)

  _reset_params()
  return (_best_result,_best_params)

def choice_N_N_RANGE_FIRST(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1.01
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST += cur_step*alpha

  _reset_params()
  _alpha = 0.02
  _max_step = 10
  _current_step = 0

  _best_result = 0
  _best_params = Parameters.get_current_params()

  while _current_step <= _max_step:
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()
    _current_step += 1

    _change_params_for_step(_current_step, _alpha)

  _reset_params()
  return (_best_result,_best_params)

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

  _best_result = 0
  _best_params = Parameters.get_current_params()

  while _current_step <= _max_step:
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()
    _current_step += 1

    _change_params_for_step(_current_step)

  _reset_params()
  return (_best_result,_best_params)

def feature_dict(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_sd = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_d = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 1
  def _change_params_for_step(cur_step):
    _reset_params()
    if cur_step == 1:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 0
    elif cur_step == 2:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 0
    elif cur_step == 3:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 0
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 0

  _reset_params()
  _max_step = 3
  _current_step = 0

  _best_result = 0
  _best_params = Parameters.get_current_params()

  while _current_step <= _max_step:
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()
    _current_step += 1

    _change_params_for_step(_current_step)

  _reset_params()
  return (_best_result,_best_params)

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

  _best_result = 0
  _best_params = Parameters.get_current_params()

  while _current_step <= _max_step:
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()
    _current_step += 1

    _change_params_for_step(_current_step)

  _reset_params()
  return (_best_result,_best_params)

def nbest_similarity(dict_nouns):
  def _reset_params():
    Parameters.PARAMETERS.N_BEST_CALCULATE_SIMILARITY = 1
  def _change_params_for_step(cur_step, alpha):
    _reset_params()
    Parameters.PARAMETERS.N_BEST_CALCULATE_SIMILARITY += cur_step*alpha

  _reset_params()
  _alpha = 1
  _max_step = 9
  _current_step = 0

  _best_result = 0
  _best_params = Parameters.get_current_params()

  while _current_step <= _max_step:
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()

    _current_step += 1

    _change_params_for_step(_current_step,_alpha)

  _reset_params()

  return (_best_result,_best_params)

def train():
  _best_result = 0;
  _best_params = Parameters.get_current_params()

  for i in range(0,1000):
    # random_all_feature
    Parameters.random_params_values()
    # calculate_result -> current best
    (precision, recall, accuracy) = SimilarityWordnetOxford.similarityWords(dict_ox_nouns)
    if accuracy > _best_result:
      _best_result = accuracy
      _best_params = Parameters.get_current_params()

    # run this feature in range -> choice best result
    lower = -1
    previous_random = -1;
    best_result_loop = 0
    best_params_loop = Parameters.get_current_params()
    while lower < 7:
      chosen_feature = random.randint(0,6)
      while chosen_feature == previous_random:
        chosen_feature = random.randint(0,6)
      previous_random = chosen_feature
      best_result = 0
      best_params = []
      if lower >= 0:
        chosen_feature = lower

      if chosen_feature == 0:
        (best_result, best_params) = jaccard_weight(dict_ox_nouns)
      elif chosen_feature == 1:
        (best_result, best_params) = choice_1_COL_RANGE_FIRST(dict_ox_nouns)
      elif chosen_feature == 2:
        (best_result, best_params) = choice_N_N_RANGE_FIRST(dict_ox_nouns)
      elif chosen_feature == 3:
        (best_result, best_params) = feature_wn(dict_ox_nouns)
      elif chosen_feature == 4:
        (best_result, best_params) = feature_dict(dict_ox_nouns)
      elif chosen_feature == 5:
        (best_result, best_params) = feature_POS(dict_ox_nouns)
      else:
        (best_result, best_params) = nbest_similarity(dict_ox_nouns)
      # compare with _best
      if best_result >= best_result_loop:
        best_result_loop = best_result
        best_params_loop = best_params
        lower = -1
      else:
        lower += 1

      Parameters.set_params_from_arr(best_params_loop)

    if best_result >= best_result_loop:
        _best_result = best_result_loop
        _best_params = best_params_loop
        Parameters.set_params_from_arr(_best_params)
        WriteParametersAndResult.append_params_and_result_to_file(_best_params)






# train()
feature_wn(dict_ox_nouns)
# feature_dict(dict_ox_nouns)
# feature_POS(dict_ox_nouns)
# nbest_similarity(dict_ox_nouns)
# jaccard_weight(dict_ox_nouns)
# choice_1_COL_RANGE_FIRST(dict_ox_nouns)
# choice_N_N_RANGE_FIRST(dict_ox_nouns)