import OxfordParser
import WordnetHandler
import FileProcess


__filename_input_sen__ = "svm/test/input_sen"


def parse_ox_wn_defi_to_input(word):
  defis_wn = WordnetHandler.get_definitions_for_word(word)
  defis_ox = OxfordParser.get_definitions_of_word_for_svm(word)

  for defi_wn in defis_wn:
    for defi_ox in defis_ox:
      value = defi_wn + "\t" + defi_ox
      FileProcess.append_value_to_file(value, __filename_input_sen__)


def create_input_sens_for_test_svm():
  dict_ox = OxfordParser.get_dict_nouns()
  for word in dict_ox:
    parse_ox_wn_defi_to_input(word)
