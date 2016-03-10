import FileProcess


class PARAMETERS_CHOICE_0_1:
  CHOICE_1_1_MIN = 0.3
  CHOICE_1_COL_MIN_FIRST = 0.6
  CHOICE_1_COL_RANGE_FIRST = 1.1
  CHOICE_N_N_MIN_FIRST = 0.6
  CHOICE_N_N_RANGE_FIRST = 1.1


################################################################################


filename = "main_syns_defi_d_cal_syns_v_test.csv"
__result_file_name__ = "Results/vector_definition/" + filename


def append_params_and_result_to_file(values):
  FileProcess.append_result_to_excel_file(__result_file_name__, values)


def reset_params_zero():
  PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN = 0.0
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST = 0.0
  PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST = 1.0
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST = 0.0
  PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST = 1.0


def get_current_params():
  return [
          PARAMETERS_CHOICE_0_1.CHOICE_1_1_MIN,
          PARAMETERS_CHOICE_0_1.CHOICE_1_COL_MIN_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_1_COL_RANGE_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_N_N_MIN_FIRST,
          PARAMETERS_CHOICE_0_1.CHOICE_N_N_RANGE_FIRST]


def get_params_string():
   return [
          "weight for min 1-1",
          "weight for min 1-n",
          "weight for diff 1-n",
          "weight for min n-n",
          "weight for diff n-n"]


# # #
# create first row
#params_string = get_params_string()
#params_string.append("precision")
#params_string.append("recall")
#params_string.append("f_score")
#params_string.append("accuracy")
#append_params_and_result_to_file(params_string)
# # #


def append_result_to_file(precision, recall, f_score, accuracy):
  params_value = get_current_params()
  params_value.append(precision)
  params_value.append(recall)
  params_value.append(f_score)
  params_value.append(accuracy)

  append_params_and_result_to_file(params_value)
