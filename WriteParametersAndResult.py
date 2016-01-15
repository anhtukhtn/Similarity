__author__ = 'tu'

import FileProcess
from Parameters import PARAMETERS,PARAMETERS_CHOICE_0_1


def get_current_params():
  return [PARAMETERS.DICT_WN_FEATURE_RELATION_definition,
          PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms,
          PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms,
          PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms,
          PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms,
          PARAMETERS.POS_FEATURE_n,
          PARAMETERS.POS_FEATURE_v,
          PARAMETERS.DICT_OX_FEATURE_RELATION_sd,
          PARAMETERS.DICT_OX_FEATURE_RELATION_d,
          PARAMETERS.DICT_OX_FEATURE_RELATION_xh,
          PARAMETERS.DICT_OX_FEATURE_RELATION_x,
          PARAMETERS.SIMILARITY_METHOD_USING,
          PARAMETERS.N_BEST_CALCULATE_SIMILARITY,
          PARAMETERS.JACCARD_WEIGHT,
          PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN,
          PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST]

params_value = ["wn use definition",
                "wn use hypernyms",
                "wn use hyponyms",
                "wn use meronyms",
                "wn use holonyms",
                "use n",
                "use v",
                "ox use sd",
                "ox use d",
                "ox use xh",
                "ox use x",
                "similarity method",
                "n-best for calculating similarity",
                "jaccard weight",
                "weight for min 1-1",
                "weight for min 1-n",
                "weight for diff 1-n",
                "weight for min n-n",
                "weight for diff n-n",
                "precision",
                "recall",
                "accuracy"]

result_file_name = "Results/parameters/params_result/params_result"
def append_params_and_result_to_file(values):
  FileProcess.append_result_to_excel_file(result_file_name,values)
# append_params_and_result_to_file(params_value)

def append_result_to_file(precision,recall,accuracy):
  params_value = get_current_params()
  params_value.append(precision)
  params_value.append(recall)
  params_value.append(accuracy)
  append_params_and_result_to_file(params_value)
