import OxfordParser
import Literal
import Ngrams
import ShallowSyntactic
import WordnetBased
import LSA
import jellyfish as Jelly
import unicodedata
import re

import CompareWithGold
import WordnetHandler
import FileProcess
import heapq
from nltk.corpus import wordnet as wn
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__filename_input_sen_train__ = "svm/train/input_sen"
__filename_input_gs_train__ = "svm/train/gs_sen"
__filename_input_train_feature_values__ = "svm/train/input_feature_values"

__filename_input_sen_test__ = "svm/test/input_sen"
__filename_input_test_feature_values__ = "svm/test/input_feature_values"


def cal_feature_values_for(syn_wn, syn_ox):
  feature_values = []

  defi_wn = WordnetHandler.get_defi_for_syn(syn_wn)
  defi_ox = OxfordParser.get_defi_for_syn(syn_ox)

  gloss_wn = WordnetHandler.get_gloss_for_syn(syn_wn)
  gloss_ox = OxfordParser.get_gloss_for_syn(syn_ox)

  lemma_wn = WordnetHandler.get_lemma_for_synset(syn_wn)
  sd_ox = OxfordParser.get_short_defi_for_syn(syn_ox)

  ex_wn = WordnetHandler.get_ex_for_syn(syn_wn)
  ex_ox = OxfordParser.get_ex_for_syn(syn_ox)

  cl_ox =  OxfordParser.get_collocation_for_syn(syn_ox)
  hyper_wn = WordnetHandler.get_hyper_defi_for_synset(syn_wn)
  mero_wn = WordnetHandler.get_mero_defi_for_synset(syn_wn)

  # # # # # # # # # # # # # # # # #
  # Literal
  literal_leven_value = 1-Literal.levenshtein(defi_wn, defi_ox)
  feature_values.append(literal_leven_value)

  literal_jacc_value = 1.00001-Literal.jaccard(defi_wn, defi_ox)
  feature_values.append(literal_jacc_value)
#  feature_values.append(literal_jacc_value+literal_leven_value)

  # # # # # # # # # #

  literal_leven_value = 1-Literal.levenshtein(gloss_wn, gloss_ox)
  feature_values.append(literal_leven_value)

  literal_jacc_value = 1.00001-Literal.jaccard(gloss_wn, gloss_ox)
  feature_values.append(literal_jacc_value)
#  feature_values.append(literal_jacc_value+literal_leven_value)

  # # # # # # # # # #

  literal_leven_ngram = literal_leven_value
  literal_jacc_ngram = literal_jacc_value

  ngrams_value = Ngrams.ngrams_word_for(gloss_wn, gloss_ox, 2)
  literal_jacc_ngram += ngrams_value
  literal_leven_ngram += ngrams_value

  ngrams_value = Ngrams.ngrams_word_for(gloss_wn, gloss_ox, 3)
  literal_jacc_ngram += ngrams_value
  literal_leven_ngram += ngrams_value

  ngrams_value = Ngrams.ngrams_word_for(gloss_wn, gloss_ox, 4)
  literal_jacc_ngram += ngrams_value
  literal_leven_ngram += ngrams_value

  ngrams_value = Ngrams.ngrams_word_for(gloss_wn, gloss_ox, 5)
  literal_jacc_ngram += ngrams_value
  literal_leven_ngram += ngrams_value

  feature_values.append(literal_jacc_ngram)
#  feature_values.append(literal_leven_ngram)

  # # # # # # # # # #

#  gloss_split_wn = Literal.split_and_stem(gloss_wn)
#  gloss_split_ox = Literal.split_and_stem(gloss_ox)
#  literal_jaro_winkler = Jelly.jaro_winkler(gloss_wn, gloss_ox)
#  feature_values.append(literal_jaro_winkler + literal_jacc_value)

  # # # # # # # # # #

#  literal_jacc_value = 1.00001-Literal.jaccard(ex_wn, ex_ox)
#  feature_values.append(literal_jacc_value)

  # # # # # # # # # # # # # # # # #
  # ShallowSyntactic

#  shallow_jaccard_POS = 0
#  shallow_jaccard_POS += 1.0001 - ShallowSyntactic.jaccard_POS(gloss_wn, gloss_ox)
#  shallow_jaccard_POS += 1.0001 - ShallowSyntactic.jaccard_POS_ngrams(gloss_wn, gloss_ox, 2)
#  shallow_jaccard_POS += 1.0001 - ShallowSyntactic.jaccard_POS_ngrams(gloss_wn, gloss_ox, 3)
#  shallow_jaccard_POS += 1.0001 - ShallowSyntactic.jaccard_POS_ngrams(gloss_wn, gloss_ox, 4)
#  feature_values.append(shallow_jaccard_POS)

  # # # # # # # # # # # # # # # # #
  # wordnet-based, WSD

  wn_value = WordnetBased.wordnet_based(defi_wn, defi_ox, 0)
  feature_values.append(wn_value)

#  wn_value = WordnetBased.wordnet_based(hyper_wn, defi_ox, 0)
#  feature_values.append(wn_value)

#  hypo_value = 0
#  if len(syn_wn.hyponyms()) > 0:
#    for hypo in syn_wn.hyponyms():
#      hypo_value += WordnetBased.wordnet_based_synset(hypo, defi_ox)
#    hypo_value /= len(syn_wn.hyponyms())
#  feature_values.append(hypo_value)

#  hyper_value = 0
#  if len(syn_wn.hypernyms()) > 0:
#    for hyper in syn_wn.hypernyms():
#      hyper_value += WordnetBased.wordnet_based_synset(hyper, defi_ox)
#    hyper_value /= len(syn_wn.hypernyms())
#  feature_values.append(hyper_value)
#
#  wn_value = WordnetBased.wordnet_based(ex_wn, ex_ox,0)
#  feature_values.append(wn_value)
#
#  wn_value_1 = WordnetBased.wordnet_based(defi_wn, defi_ox, 1)
#  feature_values.append(wn_value + wn_value_1)
#
#  wn_value = WordnetBased.wordnet_based(gloss_wn, gloss_ox, 0)
#  feature_values.append(wn_value)
#
#  wn_value_1 = WordnetBased.wordnet_based(gloss_wn, gloss_ox, 1)
#  feature_values.append(wn_value + wn_value_1)

  # # # # # # # # # # # # # # # # #
  # lsa
#  lsa_tfidf = LSA.sim_tfidf(defi_wn, defi_ox)
#  feature_values.append(lsa_tfidf)
##
#  lsa_tfidf = LSA.sim_tfidf(hyper_wn, defi_ox)
#  feature_values.append(lsa_tfidf)
#
#  lsa_tfidf = LSA.sim_tfidf(gloss_wn, gloss_ox)
#  feature_values.append(lsa_tfidf)

#  lsa_tfidf = LSA.sim_tfidf(lemma_wn, sd_ox)
#  feature_values.append(lsa_tfidf)
#
#  lsa_tfidf = LSA.sim_tfidf(ex_wn, ex_ox)
#  feature_values.append(lsa_tfidf)

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


def root_values_of_a_feature_in_row(syns_values_in_row, i_feature):
  values_of_a_feature_in_row = get_row_values(syns_values_in_row, i_feature)

  arr_result = values_of_a_feature_in_row
  if len(arr_result) < 1:
    return 0
  if len(arr_result) < 2:
    return arr_result[0]

  order = heapq.nlargest(2, range(len(arr_result)), arr_result.__getitem__);
  return arr_result[order[1]] + 0.000001
#  average_value = 0
#  for value in arr_result:
#    average_value += value
#  average_value /= len(arr_result)
#  return average_value


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
    arr_root_values_of_feature = []
    for i_feature in range(len(syns_values_in_row[0])):
      root = root_values_of_a_feature_in_row(syns_values_in_row, i_feature)
      arr_root_values_of_feature.append(root)

    for i_wn in range(len(syns_wn)):

      # cal value for svm
      for i_ox in range(len(syns_ox)):
        feature_values_for_svm = ""
        feature_values_1_syn = syns_values_in_row[i_wn]
        for i_feature in range(len(feature_values_1_syn)):
          root_value = arr_root_values_of_feature[i_feature]
          feature_value = feature_values_1_syn[i_feature]
          feature_value_for_svm = feature_value/root_value
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
      arr_root_values_of_feature = []
      for i_feature in range(len(syns_values_in_row[0])):
        root = root_values_of_a_feature_in_row(syns_values_in_row, i_feature)
        arr_root_values_of_feature.append(root)

      # cal value for svm
      for i_ox in range(len(syns_ox)):
        feature_values_for_svm = ""
        feature_values_1_syn = syns_values_in_row[i_ox]
        for i_feature in range(len(feature_values_1_syn)):
          root_value = arr_root_values_of_feature[i_feature]
          feature_value = feature_values_1_syn[i_feature]
          feature_value_for_svm = feature_value/root_value
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

    if word == "brook":
      return

#    if word != "bank":
#      continue

    syns_wn = WordnetHandler.get_synsets_for_word(word, 'n')
    syns_ox = dict_ox[word]

    if len(syns_ox) == 1 and len(syns_wn) == 1:
      continue

    write_label_for_svm(syns_wn, syns_ox, dict_gold[word])
    write_sens_for_reading(syns_wn, syns_ox, __filename_input_sen_train__)
    cal_features_and_write_to_file_for(syns_wn, syns_ox, __filename_input_train_feature_values__)


def append_value_to_file(value, filename):
  file = open(filename, 'a')
  file.write(value + "\n")
  file.close()


def reprocessing_tv(tv):
  tv = remove_unicode_characters(tv)
  tv = tv.rstrip().lstrip().lower().replace("\n","")
  return tv


def remove_unicode_characters(phrase):
  return unicodedata.normalize('NFKD', phrase.decode('utf-8')).encode('ascii', 'ignore')


def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n

    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]

def check_tv_similar(sen_tv_1, sen_tv_2):
  tv_1 = reprocessing_tv(sen_tv_1)
  tv_2 = reprocessing_tv(sen_tv_2)
  if tv_1 == tv_2:
    return 1
#
#  if tv_1 in tv_2:
#    return 1
#  if tv_2 in tv_1:
#    return 1
#
#  if levenshtein(tv_1, tv_2) < len(tv_2)/1.4:
#    return 1

  return 0

def create_input_for_train_svm_via_vn():

  dict_ox =  OxfordParser.get_dict_csv_nouns()
  f = open(__filename_input_sen_train__,'r');
  line = f.readline();

  while (line):
    if len(line) > 0:

      sens = line.split("\t")
      syn_wn = wn._synset_from_pos_and_offset('n', long(sens[0]))

      for lemma in syn_wn.lemmas():
        word = lemma.name().lower()
        if word in dict_ox:
          syns_ox = dict_ox[word]
          syns_values_in_row = []

          ox_current = -1
          for i_ox in range(len(syns_ox)):
            syn_ox = syns_ox[str(i_ox)]
            ox_defi = syn_ox['d'].replace("\n","")
            ox_defi = ox_defi.replace("\t","")
            ox_gold_defi = sens[1].replace("\n","")
            ox_gold_defi = ox_gold_defi.replace("\t","")
            ox_gold_defi = ox_gold_defi.replace(","," ")
            if check_tv_similar(ox_defi, ox_gold_defi):
              ox_current = i_ox
          if ox_current == -1:
            continue

          # cal all features between syns in ox with syn in wn
          syns_values_in_row = []
          for i_ox in range(len(syns_ox)):
            syn_ox = syns_ox[str(i_ox)]
            feature_values = cal_feature_values_for(syn_wn, syn_ox)
            syns_values_in_row.append(feature_values)

          # cal max values of each feature
          arr_root_values_of_feature = []
          for i_feature in range(len(syns_values_in_row[0])):
            root = root_values_of_a_feature_in_row(syns_values_in_row, i_feature)
            arr_root_values_of_feature.append(root)

          # cal value for svm
          feature_values_for_svm = ""
          feature_values_1_syn = syns_values_in_row[ox_current]
          for i_feature in range(len(feature_values_1_syn)):
            root_value = arr_root_values_of_feature[i_feature]
            feature_value = feature_values_1_syn[i_feature]
            feature_value_for_svm = feature_value/root_value
            feature_values_for_svm += str(feature_value_for_svm) + "\t"

          if feature_values_for_svm != "":
            feature_values_for_svm = feature_values_for_svm[:-1]

          append_value_to_file(feature_values_for_svm,  __filename_input_train_feature_values__)
          break

      line = f.readline();

  f.close()


def create_input_for_test_svm():
  dict_ox =  OxfordParser.get_dict_nouns()
  flag_can_go = False
  for word in dict_ox:

#    if word == "brook":
#      flag_can_go = True
#
#    if flag_can_go == False:
#      continue

    if len(dict_ox[word]) == 0:
      continue

    syns_wn = WordnetHandler.get_synsets_for_word(word, 'n')
    syns_ox = dict_ox[word]

    if len(syns_ox) == 1 and len(syns_wn) == 1:
      continue

    write_sens_for_reading(syns_wn, syns_ox, __filename_input_sen_test__)
    cal_features_and_write_to_file_for(syns_wn, syns_ox, __filename_input_test_feature_values__)
