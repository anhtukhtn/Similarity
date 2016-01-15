__author__ = 'tu'
import SimilarityWordnetOxford
import OxfordParser
import Parameters

dict_ox_nouns = OxfordParser.readOxfordNouns();


def jaccard_weight(dict_nouns):

  step = 0.01
  Parameters.PARAMETERS.JACCARD_WEIGHT = 0.0

  while (Parameters.PARAMETERS.JACCARD_WEIGHT < 0.05):
    SimilarityWordnetOxford.similarityWords(dict_nouns)
    Parameters.PARAMETERS.JACCARD_WEIGHT += step


def feature_wn(dict_nouns):

  def reset_params():
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_definition = 1
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = 0
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = 0
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = 0
    Parameters.PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = 0
  def change_params_for_step(cur_step):
    reset_params()
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


  reset_params()
  step = 1
  max_step = 10
  current_step = 0

  while current_step <= max_step:
    SimilarityWordnetOxford.similarityWords(dict_nouns)
    current_step += step

    change_params_for_step(current_step)

  reset_params()

def feature_dict(dict_nouns):
  def reset_params():
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_sd = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_d = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 1
    Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 1
  def change_params_for_step(cur_step):
    reset_params()
    if cur_step == 1:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 0
    elif cur_step == 2:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 0
    elif cur_step == 3:
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_xh = 0
      Parameters.PARAMETERS.DICT_OX_FEATURE_RELATION_x = 0

  reset_params()
  step = 1
  max_step = 3
  current_step = 0

  while current_step <= max_step:
    SimilarityWordnetOxford.similarityWords(dict_nouns)
    current_step += step

    change_params_for_step(current_step)

  reset_params()

def feature_POS(dict_nouns):
  def reset_params():
    Parameters.PARAMETERS.POS_FEATURE_n = 1
    Parameters.PARAMETERS.POS_FEATURE_v = 0
  def change_params_for_step(cur_step):
    reset_params()
    if cur_step == 1:
      Parameters.PARAMETERS.POS_FEATURE_v = 1

  reset_params()
  step = 1
  max_step = 1
  current_step = 0

  while current_step <= max_step:
    SimilarityWordnetOxford.similarityWords(dict_nouns)
    current_step += step

    change_params_for_step(current_step)

  reset_params()

def nbest_similarity(dict_nouns):
  def reset_params():
    Parameters.PARAMETERS.N_BEST_CALCULATE_SIMILARITY = 1
  def change_params_for_step(cur_step):
    reset_params()
    Parameters.PARAMETERS.N_BEST_CALCULATE_SIMILARITY += cur_step*1

  reset_params()
  step = 1
  max_step = 9
  current_step = 0

  while current_step <= max_step:
    SimilarityWordnetOxford.similarityWords(dict_nouns)
    current_step += step

    change_params_for_step(current_step)

  reset_params()

# feature_wn(dict_ox_nouns)
# feature_dict(dict_ox_nouns)
# feature_POS(dict_ox_nouns)
nbest_similarity(dict_ox_nouns)