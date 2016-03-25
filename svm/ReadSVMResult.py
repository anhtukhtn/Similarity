import GoldDataSVM
import main_svm
import Util

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__dict_sim__ = {}


def reprocessing(sen):
  sen = Util.remove_unicode_characters(sen)
  sen = sen.rstrip().lstrip().lower().replace("\n","")
  return sen

def create_key_for_sens(sen_1, sen_2):
  sen_1 = reprocessing(sen_1)
  sen_2 = reprocessing(sen_2)
  return sen_1 + "--" + sen_2


def read_svm_result():
  f = open(GoldDataSVM.__filename_test_sen__, 'r');
  line = f.readline();

  f_sim = open(main_svm.file_rs, 'r')
  line_sim = f_sim.readline()
  while (line):
    if len(line) > 0:
      sens = line.split("\t")
      sen_1 = sens[0]
      sen_2 = sens[1]

      sim = float(line_sim)

      key = create_key_for_sens(sen_1, sen_2)
      print key
      __dict_sim__[key] = sim

    line = f.readline();
    line_sim = f_sim.readline()

  f.close()
  f_sim.close()


def get_sim_for_sens(sen_1, sen_2):
  key = create_key_for_sens(sen_1, sen_2)
  return __dict_sim__[key]

