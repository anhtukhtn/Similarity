#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import FileProcess
import ReadVietNet
import OxfordParser
import Util
import Literal
import ShallowSyntactic
import WordnetBased

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__filename_input_sen__ = "svm/train/input_sen"
__filename_input_gs__ = "svm/train/gs_sen"
__filename_input_feature_values__ = "svm/train/input_feature_values"


def split_tv(tv):
  result = filter(None, re.split("[,.(;\-!/?:]+", tv))
  return result


def reprocessing_tv(tv):
  tv = Util.remove_unicode_characters(tv)
  tv = tv.rstrip().lstrip().lower().replace("\n","")
  return tv


def check_tv_similar(sen_tv_1, sen_tv_2):
  arr_tv_1 = split_tv(sen_tv_1)
  arr_tv_2 = split_tv(sen_tv_2)
  for tv_1 in arr_tv_1:
    tv_1 = reprocessing_tv(tv_1)
    for tv_2 in arr_tv_2:
      tv_2 = reprocessing_tv(tv_2)
      if tv_1 == tv_2:
        return 1

  return 0


def check_tv_not_similar(sen_tv_1, sen_tv_2):
  can_similarity = 0
  arr_tv_1 = split_tv(sen_tv_1)
  arr_tv_2 = split_tv(sen_tv_2)
  for tv_1 in arr_tv_1:
    tv_1 = reprocessing_tv(tv_1)
    for tv_2 in arr_tv_2:
      tv_2 = reprocessing_tv(tv_2)

      levenshtein = Util.levenshtein(tv_1,tv_2)
      if levenshtein <  len(tv_1)/2:
        can_similarity = 1

  if can_similarity == 1:
    return 0

  return 1


def create_input_sen_via_ox_vn(dict_vn, dict_ox):

  for word in dict_ox:
    if len(dict_ox[word]) == 0:
      continue

    if word in dict_vn:

      word_syns_vn = dict_vn[word]
      word_syns_ox = dict_ox[word]
      for i_vn in word_syns_vn:
        syn_vn = word_syns_vn[i_vn]
        for i_ox in word_syns_ox:
          syn_ox = word_syns_ox[i_ox]
          if "tv" not in syn_ox:
            continue
          if check_tv_similar(syn_vn['tv'], syn_ox['tv']) == 1:
            defi_vn = syn_vn['d']
            defi_ox = syn_ox['d']
            value = defi_vn + "\t" + defi_ox
            FileProcess.append_value_to_file(value, __filename_input_sen__)
            FileProcess.append_value_to_file("1", __filename_input_gs__)


def create_input_sen_via_ox_wn_negative(dict_vn, dict_ox):
  words = list(dict_ox.keys())

  for diff in range(2):
    diff = diff + 1
    for i_word in range(len(words)-diff):
      word_ox = words[i_word]
      word_vn = words[i_word+diff]

      if word_vn in dict_vn:
        if len(dict_ox[word_ox]) == 0:
          continue

        if len(dict_vn[word_vn]) == 0:
          continue

        word_syns_vn = dict_vn[word_vn]
        word_syns_ox = dict_ox[word_ox]
        for i_vn in word_syns_vn:
          syn_vn = word_syns_vn[i_vn]
          for i_ox in word_syns_ox:
            syn_ox = word_syns_ox[i_ox]
            if "tv" not in syn_ox:
              continue
            if check_tv_not_similar(syn_vn['tv'], syn_ox['tv']) == 1:
              defi_vn = syn_vn['d']
              defi_ox = syn_ox['d']
              value = defi_vn + "\t" + defi_ox
              print value
              FileProcess.append_value_to_file(value, __filename_input_sen__)
              FileProcess.append_value_to_file("0", __filename_input_gs__)


def create_input_for_train():
  dict_vn = ReadVietNet.readVietNetFile()
  dict_ox = OxfordParser.get_dict_nouns()
  create_input_sen_via_ox_vn(dict_vn, dict_ox)
  create_input_sen_via_ox_wn_negative(dict_vn, dict_ox)


def cal_features_from_sens_write_to_file(filename_sens, filename_output):
  f = open(filename_sens,'r');
  line = f.readline();
  while (line):
    if len(line) > 0:

      feature_values = ""

      sens = line.split("\t")

      sen_1 = sens[0]
      sen_2 = sens[1]

      feature_values += str(Literal.levenshtein(sen_1, sen_2)) + "\t"
      feature_values += str(ShallowSyntactic.jaccard_POS(sen_1, sen_2)) + "\t"
      feature_values += str(WordnetBased.wordnet_based(sen_1, sen_2))

      FileProcess.append_value_to_file(feature_values, filename_output)

      line = f.readline();

  f.close()


def cal_features_for_train():
  cal_features_from_sens_write_to_file(__filename_input_sen__, __filename_input_feature_values__)

__filename_test_sen__ = "svm/test/input_sen"
__filename_test_feature_values__ = "svm/test/input_feature_values"

def cal_features_for_test():
  cal_features_from_sens_write_to_file(__filename_test_sen__, __filename_test_feature_values__)

