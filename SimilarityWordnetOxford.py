__author__ = 'tu'

# get num of b best when extracting oxford and wn
N_BEST_EXTRACT_OXFORD = 1
N_BEST_EXTRACT_WN = 1

# features in wn for a word
DICT_WN_FEATURE_RELATION = {}
DICT_WN_FEATURE_RELATION['definition'] = 1
DICT_WN_FEATURE_RELATION['hypernyms'] = 1
DICT_WN_FEATURE_RELATION['hyponyms'] = 1
DICT_WN_FEATURE_RELATION['part_meronyms'] = 1

# using POS (extracting)
POS_FEATURE = {}
POS_FEATURE['n'] = 1
POS_FEATURE['v'] = 1

# features in Oxford for a word
DICT_WN_FEATURE_RELATION = {}
DICT_WN_FEATURE_RELATION['sd'] = 1
DICT_WN_FEATURE_RELATION['d'] = 1
DICT_WN_FEATURE_RELATION['xh'] = 1
DICT_WN_FEATURE_RELATION['x'] = 1

# similarity method
class SIMILARITY_METHOD:
  PATH = 1
  JCN  = 2
  LCH  = 3
  LIN  = 4
  RESNIK = 5
  WUP  = 6

# weight for jaccard and similarity
JACCARD_WEIGHT = 0.3


