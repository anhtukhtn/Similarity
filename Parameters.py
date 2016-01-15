__author__ = 'tu'

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

  # features in wn for a word
  DICT_WN_FEATURE_RELATION_definition = 1
  DICT_WN_FEATURE_RELATION_hypernyms = 0
  DICT_WN_FEATURE_RELATION_hyponyms = 0
  DICT_WN_FEATURE_RELATION_part_meronyms = 0
  DICT_WN_FEATURE_RELATION_member_holonyms = 0

  # using POS (extracting)
  POS_FEATURE_n = 1
  POS_FEATURE_v = 0

  # features in Oxford for a word
  DICT_OX_FEATURE_RELATION_sd = 1
  DICT_OX_FEATURE_RELATION_d = 1
  DICT_OX_FEATURE_RELATION_xh = 1
  DICT_OX_FEATURE_RELATION_x = 1

  # similarity method
  SIMILARITY_METHOD_USING = SIMILARITY_METHOD.PATH

  # n best when calculating similarity for each synset
  N_BEST_CALCULATE_SIMILARITY = 4

  # weight for jaccard and similarity
  JACCARD_WEIGHT = 0.05

class PARAMETERS_CHOICE_0_1:
  CHOICE_1_1_MIN = 0.1
  CHOICE_1_COL_MIN_FIRST = 0.5
  CHOICE_1_COL_RANGE_FIRST = 1.01
  CHOICE_N_N_MIN_FIRST = 0.5
  CHOICE_N_N_RANGE_FIRST = 1.26
####################################################################################################

