import WordnetHandler
import FileProcess
import Literal
import WordnetBased
import CompareWithGold
import OxfordParser
import heapq

__filename_input_sen_train__ = "svm/train/input_sen"
__filename_input_gs_train__ = "svm/train/gs_sen"
__filename_input_train_feature_values__ = "svm/train/input_feature_values"

__filename_input_sen_test__ = "svm/test/input_sen"
__filename_input_test_feature_values__ = "svm/test/input_feature_values"


def cal_feature_values_for(syn_wn, syn_ox):
  defi_wn = syn_wn.definition()
  defi_ox = syn_ox["d"]
  feature_values = []

#  literal_leven_value = 1-Literal.levenshtein(defi_wn, defi_ox)
#  feature_values.append(literal_leven_value)

  literal_jacc_value = 1.00001-Literal.jaccard(defi_wn, defi_ox)
  feature_values.append(literal_jacc_value)

  wn_value = WordnetBased.wordnet_based(defi_wn, defi_ox)
  feature_values.append(wn_value)

  return feature_values


def write_sens_for_reading(syns_wn, syns_ox, filename_output):
  for i_wn in range(len(syns_wn)):
    for i_ox in range(len(syns_ox)):
      defi_wn = syns_wn[i_wn].definition()
      defi_ox = syns_ox[str(i_ox)]["d"]
      value = defi_wn + "\t" + defi_ox
      FileProcess.append_value_to_file(value, filename_output)


def write_label_for_svm(syns_wn, syns_ox, dict_gold):
  for i_wn in range(len(syns_wn)):
    for i_ox in range(len(syns_ox)):
      FileProcess.append_value_to_file(dict_gold[i_wn][i_ox], __filename_input_gs_train__)


def get_row_values(syns_values_in_row, index):
  values_of_a_feature_in_row = []
  for values in syns_values_in_row:
    value = values[index]
    values_of_a_feature_in_row.append(value)

  return values_of_a_feature_in_row


def max_values_of_a_feature_in_row(syns_values_in_row, i_feature):
  values_of_a_feature_in_row = get_row_values(syns_values_in_row, i_feature)

  arr_result = values_of_a_feature_in_row
  if len(arr_result) < 1:
    return (0, 0)
  if len(arr_result) < 2:
    return (arr_result[0], arr_result[0])

  order = heapq.nlargest(2, range(len(arr_result)), arr_result.__getitem__);
  return (arr_result[order[0]],arr_result[order[1]])


def cal_features_and_write_to_file_for(syns_wn, syns_ox, filename_output):
  if len(syns_ox) == 1 and len(syns_wn) > 1:

    # cal all features between syns in ox with syn in wn
    syns_values_in_row = []
    for i_wn in range(len(syns_wn)):
      syn_wn = syns_wn[i_wn]
      syn_ox = syns_ox[str(0)]
      feature_values = cal_feature_values_for(syn_wn, syn_ox)
      syns_values_in_row.append(feature_values)

    # cal max values of each feature
    arr_second_values_of_feature = []
    for i_feature in range(len(syns_values_in_row[0])):
      (first, second) = max_values_of_a_feature_in_row(syns_values_in_row, i_feature)
      arr_second_values_of_feature.append(second)

    for i_wn in range(len(syns_wn)):

      # cal value for svm
      for i_ox in range(len(syns_ox)):
        feature_values_for_svm = ""
        feature_values_1_syn = syns_values_in_row[i_wn]
        for i_feature in range(len(feature_values_1_syn)):
          second_value = arr_second_values_of_feature[i_feature]
          feature_value = feature_values_1_syn[i_feature]
          feature_value_for_svm = feature_value/second_value
          feature_values_for_svm += str(feature_value_for_svm) + "\t"

        if feature_values_for_svm != "":
          feature_values_for_svm = feature_values_for_svm[:-1]

        FileProcess.append_value_to_file(feature_values_for_svm, filename_output)
  else:
    for i_wn in range(len(syns_wn)):

      # cal all features between syns in ox with syn in wn
      syns_values_in_row = []
      for i_ox in range(len(syns_ox)):
        syn_wn = syns_wn[i_wn]
        syn_ox = syns_ox[str(i_ox)]
        feature_values = cal_feature_values_for(syn_wn, syn_ox)
        syns_values_in_row.append(feature_values)

      # cal max values of each feature
      arr_second_values_of_feature = []
      for i_feature in range(len(syns_values_in_row[0])):
        (first, second) = max_values_of_a_feature_in_row(syns_values_in_row, i_feature)
        arr_second_values_of_feature.append(second)

      # cal value for svm
      for i_ox in range(len(syns_ox)):
        feature_values_for_svm = ""
        feature_values_1_syn = syns_values_in_row[i_ox]
        for i_feature in range(len(feature_values_1_syn)):
          second_value = arr_second_values_of_feature[i_feature]
          feature_value = feature_values_1_syn[i_feature]
          feature_value_for_svm = feature_value/second_value
          feature_values_for_svm += str(feature_value_for_svm) + "\t"

        if feature_values_for_svm != "":
          feature_values_for_svm = feature_values_for_svm[:-1]

        FileProcess.append_value_to_file(feature_values_for_svm, filename_output)


def create_input_for_train_svm():
  dict_ox =  OxfordParser.get_dict_nouns()
  dict_gold = CompareWithGold.goldData

  for word in dict_ox:

    if len(dict_ox[word]) == 0 or word not in dict_gold:
      continue

    if word == "blockage":
      return

    syns_wn = WordnetHandler.get_synsets_for_word(word, 'n')
    syns_ox = dict_ox[word]

    if len(syns_ox) == 1 and len(syns_wn) == 1:
      continue

    write_label_for_svm(syns_wn, syns_ox, dict_gold[word])
    write_sens_for_reading(syns_wn, syns_ox, __filename_input_sen_train__)
    cal_features_and_write_to_file_for(syns_wn, syns_ox, __filename_input_train_feature_values__)


def create_input_for_test_svm():
  dict_ox =  OxfordParser.get_dict_nouns()
  flag_can_go = False
  for word in dict_ox:

    if word == "blockage":
      flag_can_go = True

    if flag_can_go == False:
      continue

    if len(dict_ox[word]) == 0:
      continue

    syns_wn = WordnetHandler.get_synsets_for_word(word, 'n')
    syns_ox = dict_ox[word]

    if len(syns_ox) == 1 and len(syns_wn) == 1:
      continue

    write_sens_for_reading(syns_wn, syns_ox, __filename_input_sen_test__)
    cal_features_and_write_to_file_for(syns_wn, syns_ox, __filename_input_test_feature_values__)
