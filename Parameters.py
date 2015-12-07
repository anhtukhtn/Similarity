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

  # get num of b best when extracting oxford and wn
  N_BEST_EXTRACT_OXFORD = 1
  N_BEST_EXTRACT_WN = 1

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
  SIMILARITY_METHOD_USING = SIMILARITY_METHOD.JCN

  # n best when calculating similarity for each synset
  N_BEST_CALCULATE_SIMILARITY = 5

  # weight for jaccard and similarity
  JACCARD_WEIGHT = 0.2

####################################################################################################

