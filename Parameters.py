__author__ = 'tu'

import random

####################################################################################################
class Map(dict):
    def __init__(self, **kwargs):
        super(Map, self).__init__(**kwargs)
        self.__dict__ = self

####################################################################################################

# similarity method
class SIMILARITY_METHOD:
  PATH = 1
  JCN  = 2
  LCH  = 3
  LIN  = 4
  RESNIK = 5
  WUP  = 6

class PARAMETERS:

  # similarity method
  SIMILARITY_METHOD_USING = SIMILARITY_METHOD.PATH

  # features in wn for a word
  DICT_WN_FEATURE_RELATION_definition = 1
  DICT_WN_FEATURE_RELATION_hypernyms = 1
  DICT_WN_FEATURE_RELATION_hyponyms = 1
  DICT_WN_FEATURE_RELATION_part_meronyms = 0
  DICT_WN_FEATURE_RELATION_member_holonyms = 0

  # features in Oxford for a wor`d
  DICT_OX_FEATURE_RELATION_sd = 1
  DICT_OX_FEATURE_RELATION_d = 1
  DICT_OX_FEATURE_RELATION_xh = 0
  DICT_OX_FEATURE_RELATION_x = 0

  # using POS (extracting)
  POS_FEATURE_n = 1
  POS_FEATURE_v = 0

  # n best when calculating similarity for each synset
  N_BEST_CALCULATE_SIMILARITY = 4

  # weight for jaccard and similarity
  JACCARD_WEIGHT = 0.1

class PARAMETERS_CHOICE_0_1:
  CHOICE_1_1_MIN = 0.00
  CHOICE_1_COL_MIN_FIRST = 0.0
  CHOICE_1_COL_RANGE_FIRST = 1.0
  CHOICE_N_N_MIN_FIRST = 0.0
  CHOICE_N_N_RANGE_FIRST = 1.00
####################################################################################################

class params_string:
  definition = "definition"
  hypernyms = "hypernyms"
  hyponyms = "hyponyms"
  meronyms = "meronyms"
  holonyms = "holonyms"
  sd = "sd"
  d = "d"
  xh = "xh"
  x = "x"
  n = "n"
  v = "v"
  nbest = "nbest"
  jaccard_weight = "jaccard_weight"
  _1_1_min = "1_1_min"
  _1_col_min = "1_col_min"
  _1_col_range = "1_col_range"
  _n_n_min = "_n_n_min"
  _n_n_range = "n_n_range"

def get_current_params():
  return [
          PARAMETERS.SIMILARITY_METHOD_USING,
          PARAMETERS.DICT_WN_FEATURE_RELATION_definition,
          PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms,
          PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms,
          PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms,
          PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms,
          PARAMETERS.DICT_OX_FEATURE_RELATION_sd,
          PARAMETERS.DICT_OX_FEATURE_RELATION_d,
          PARAMETERS.DICT_OX_FEATURE_RELATION_xh,
          PARAMETERS.DICT_OX_FEATURE_RELATION_x,
          PARAMETERS.POS_FEATURE_n,
          PARAMETERS.POS_FEATURE_v,
          PARAMETERS.N_BEST_CALCULATE_SIMILARITY,
          PARAMETERS.JACCARD_WEIGHT,
          PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN,
          PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST]

def get_params_string():
   return [
                  "similarity method",
                  "wn use definition",
                  "wn use hypernyms",
                  "wn use hyponyms",
                  "wn use meronyms",
                  "wn use holonyms",
                  "ox use sd",
                  "ox use d",
                  "ox use xh",
                  "ox use x",
                  "use n",
                  "use v",
                  "n-best for calculating similarity",
                  "jaccard weight",
                  "weight for min 1-1",
                  "weight for min 1-n",
                  "weight for diff 1-n",
                  "weight for min n-n",
                  "weight for diff n-n",
                  ]

def set_params_from_dict(params):
  # features in wn for a word
  PARAMETERS.DICT_WN_FEATURE_RELATION_definition = params[params_string.definition]
  PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = params[params_string.hypernyms]
  PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = params[params_string.holonyms]
  PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = params[params_string.meronyms]
  PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = params[params_string.holonyms]

  # using POS (extracting)
  PARAMETERS.POS_FEATURE_n = params[params_string.n]
  PARAMETERS.POS_FEATURE_v = params[params_string.v]

  # features in Oxford for a word
  PARAMETERS.DICT_OX_FEATURE_RELATION_sd = params[params_string.sd]
  PARAMETERS.DICT_OX_FEATURE_RELATION_d = params[params_string.d]
  PARAMETERS.DICT_OX_FEATURE_RELATION_xh = params[params_string.xh]
  PARAMETERS.DICT_OX_FEATURE_RELATION_x = params[params_string.x]

  # similarity method
  PARAMETERS.SIMILARITY_METHOD_USING = SIMILARITY_METHOD.PATH

  # n best when calculating similarity for each synset
  PARAMETERS.N_BEST_CALCULATE_SIMILARITY = params[params_string.nbest]

  # weight for jaccard and similarity
  PARAMETERS.JACCARD_WEIGHT = params[params_string.jaccard_weight]

  PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = params[params_string._1_1_min]
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = params[params_string._1_col_min]
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = params[params_string._1_col_range]
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = params[params_string._n_n_min]
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = params[params_string._n_n_range]

def set_params_from_arr(params):
  # features in wn for a word
  PARAMETERS.DICT_WN_FEATURE_RELATION_definition = params[0]
  PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = params[1]
  PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = params[2]
  PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = params[3]
  PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = params[4]

  # using POS (extracting)
  PARAMETERS.POS_FEATURE_n = params[5]
  PARAMETERS.POS_FEATURE_v = params[6]

  # features in Oxford for a word
  PARAMETERS.DICT_OX_FEATURE_RELATION_sd = params[7]
  PARAMETERS.DICT_OX_FEATURE_RELATION_d = params[8]
  PARAMETERS.DICT_OX_FEATURE_RELATION_xh = params[9]
  PARAMETERS.DICT_OX_FEATURE_RELATION_x = params[10]

  # similarity method
  PARAMETERS.SIMILARITY_METHOD_USING = SIMILARITY_METHOD.PATH

  # n best when calculating similarity for each synset
  PARAMETERS.N_BEST_CALCULATE_SIMILARITY = params[11]

  # weight for jaccard and similarity
  PARAMETERS.JACCARD_WEIGHT = params[12]

  PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = params[13]
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = params[14]
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = params[15]
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = params[16]
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = params[17]

def random_params_values():
  PARAMETERS.DICT_WN_FEATURE_RELATION_definition = 1
  PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms = random.randint(0,1)
  PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms = random.randint(0,1)
  PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms = random.randint(0,1)
  PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms = random.randint(0,1)

  # using POS (extracting)
  PARAMETERS.POS_FEATURE_n = 1
  PARAMETERS.POS_FEATURE_v = random.randint(0,1)

  # features in Oxford for a word
  PARAMETERS.DICT_OX_FEATURE_RELATION_sd = 1
  PARAMETERS.DICT_OX_FEATURE_RELATION_d = 1
  PARAMETERS.DICT_OX_FEATURE_RELATION_xh = random.randint(0,1)
  PARAMETERS.DICT_OX_FEATURE_RELATION_x = random.randint(0,1)
  # similarity method
  PARAMETERS.SIMILARITY_METHOD_USING = SIMILARITY_METHOD.PATH

  # n best when calculating similarity for each synset
  PARAMETERS.N_BEST_CALCULATE_SIMILARITY = random.randint(1,9)

  # weight for jaccard and similarity
  PARAMETERS.JACCARD_WEIGHT = random.randint(1,30)/100.

  PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = random.randint(1,30)/100.
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = random.randint(1,500)/100.
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1 + random.randint(1,40)/100.
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = random.randint(1,500)/100.
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1 + random.randint(1,40)/100.


