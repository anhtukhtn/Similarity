import OxParseDefinition
import WordnetParseDefinition
from scipy import spatial
import Util
import FileProcess
import WordnetHandler


def sim_for_synset_and_synsetvector(a_synset, vector):
  p_max = 0
  for synset in vector:
    p = a_synset.path_similarity(synset)
    if p > p_max:
      p_max = p

  return p_max


def vector_for_subvector_with_mixvector(subvector, mixvector):
  result_vector = []
  for synset in mixvector:
    result = sim_for_synset_and_synsetvector(synset, subvector)
    result_vector.append(result)

  return result_vector


def sim_2_vector(vector_1, vector_2):
  mix_vector = vector_1 + vector_2
  result_vector_1 = vector_for_subvector_with_mixvector(vector_1, mix_vector)
  result_vector_2 = vector_for_subvector_with_mixvector(vector_2, mix_vector)
  cosine = spatial.distance.cosine(result_vector_1, result_vector_2)
  sim_result = 1 - cosine

  return sim_result


def sim_wn_ox_vector(vectors_ox, vectors_wn):

  m2d_sim = [[0 for x in range(len(vectors_ox))] for x in range(len(vectors_wn))]
  for i in range(len(vectors_wn)):
    vector_wn = vectors_wn[i]
    for j in range(len(vectors_ox)):
      vector_ox = vectors_ox[j]
      m2d_sim[i][j] = sim_2_vector(vector_ox, vector_wn)

  return m2d_sim


def sim_ox_wn_definition():
  word = 'bench'
  dict_vectors_wn = WordnetParseDefinition.get_dict_vectors_synsets_for_word(word)
  synsets_wn = WordnetHandler.get_synsets_for_word(word,'n')
  dict_vectors_ox = OxParseDefinition.get_dict_vectors_synsets_for_word(word, synsets_wn)

  (keys_wn, vectors_wn) = Util.get_keys_values_of_dict(dict_vectors_wn)
  (keys_ox, vectors_ox) = Util.get_keys_values_of_dict(dict_vectors_ox)

  m2d_sim = sim_wn_ox_vector(vectors_ox, vectors_wn)

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  for i in range(len(keys_wn)):
    m2d_sim[i].insert(0,keys_wn[i]);
  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  row_dict = [];
  row_dict.append(word);
  for i in range(len(keys_ox)):
    row_dict.append(keys_ox[i].encode('utf8'));
  # - - - - - - - - - - - - - - - - - - - - - - - - -
  filename = 'Results/vector_definition/' + word + '.csv'
  FileProcess.append_to_excel_file(filename, row_dict, m2d_sim)
  # - - - - - - - - - - - - - - - - - - - - - - - - -
