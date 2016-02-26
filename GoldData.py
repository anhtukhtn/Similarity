import csv
import OxfordParser
import WordnetHandler
import FileProcess


def read_gold_file_to_dict(filename):
  dict_gold = {}

  f = open(filename, 'r')
  reader = csv.reader(f)

  current_row_of_word = 1
  current_word = ""
  cols_keys = []
  rows_keys = []

  for row in reader:

    if len(row) == 0:
      current_row_of_word = 1
      current_word = ""
      cols_keys = []
      rows_keys = []

    else:
      if current_row_of_word == 2:
        row_key = row.pop(0)
        row_key = row_key.split('<>')[1]
        rows_keys.append(row_key)
        for i_row in range(len(cols_keys)):
          dict_gold[current_word][cols_keys[i_row]][row_key] = row[i_row]

      if current_row_of_word == 1:
        current_word = row[0]
        dict_gold[current_word] = {}
        row.pop(0)
        for col_key in row:
          col_key = col_key.split('<>')[1]
          cols_keys.append(col_key)
          dict_gold[current_word][col_key] = {}
        current_row_of_word = 2

  return dict_gold


def get_current_order_of_ox(word):
  definitions = OxfordParser.get_definitions_of_word(word)
  return definitions


def get_current_order_of_wn(word):
  definitions = []
  synsets = WordnetHandler.get_synsets_for_word(word, 'n')
  for synset in synsets:
    definition = synset.definition()
    definitions.append(definition)
  return definitions


def reorder_dict_for_word(dict_gold, word):
  if word not in dict_gold:
    return

  ox_order = get_current_order_of_ox(word)
  wn_order = get_current_order_of_wn(word)
  dict_word = dict_gold[word]

  m2d_sim = [[0 for x in range(len(ox_order))] for x in range(len(wn_order))]

  for i_wn in range(len(wn_order)):
    wn_key = wn_order[i_wn]
    for i_ox in range(len(ox_order)):
      ox_key = ox_order[i_ox]
      sim_value = dict_word[ox_key][wn_key]
      m2d_sim[i_wn][i_ox] = sim_value

  for i_wn in range(len(wn_order)):
    wn_key = wn_order[i_wn]
    m2d_sim[i_wn].insert(0, wn_key)

  first_row = ox_order
  first_row.insert(0, word)

  filename = 'Results/GoldData/'+'compare_VN_Ox_2_1_new_order_3_1.csv'
  FileProcess.append_to_excel_file(filename, first_row, m2d_sim)


dict_filename = 'Results/parameters/VN_Ox/'+'compare_VN_Ox_2.1.csv'
dict_gold = read_gold_file_to_dict(dict_filename)
reorder_dict_for_word(dict_gold, 'bank')
