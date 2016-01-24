__author__ = 'tu'

import FileProcess
import Parameters

result_file_name = "Results/parameters/params_result/params_result_exhausted_2"
def append_params_and_result_to_file(values):
  FileProcess.append_result_to_excel_file(result_file_name,values)

# # #
# create first row
# params_string = Parameters.get_params_string()
# params_string.append("precision")
# params_string.append("recall")
# params_string.append("accuracy")
# append_params_and_result_to_file(params_string)
# # #

def append_result_to_file(precision,recall,accuracy):

  params_value = Parameters.get_current_params()
  params_value.append(precision)
  params_value.append(recall)
  params_value.append(accuracy)

  append_params_and_result_to_file(params_value)
