import FileProcess
from nltk.corpus import wordnet as wn
import svm.semanticpy.vector_space as VS
from os import walk
import os
from svm.semanticpy.transform.tfidf import TFIDF


__filename_folder__ = "svm/dataWn/"


def get_synset_gloss(synset, filename):
  result = ""
  for lemma in synset.lemmas():
    gloss = lemma.name().replace("_", " ")
    result += gloss + ". "

  result += synset.definition() + ". "
  for example in synset.examples():
    result += example + "."

  FileProcess.append_value_to_file(result, filename)

  for hypo in synset.hyponyms():
    get_synset_gloss(hypo, filename)


def write_full_hyponyms_synset_to_file(synset, filename):
  get_synset_gloss(synset, filename)


def write_wn_to_docs(folder):
  entity_synset = wn.synsets('entity')[0]
  for lvl_2_syn in entity_synset.hyponyms():
    for lvl_3_syn in lvl_2_syn.hyponyms():
      for lvl_4_syn in lvl_3_syn.hyponyms():
        for lvl_5_syn in lvl_4_syn.hyponyms():
          filename = folder + lvl_5_syn.name().replace("/",'_')
          write_full_hyponyms_synset_to_file(lvl_5_syn, filename)


def remove_smalle_file(folder):
  files = []
  for (dirpath, dirnames, filenames) in walk(__filename_folder__):
    for filename in filenames:
      files.append(__filename_folder__ + filename)

  for filename in files:
    lines = [line.rstrip('\n') for line in open(filename)]
    if len(lines) < 50:
      os.remove(filename)


def get_wn_data():
  write_wn_to_docs(__filename_folder__)
  remove_smalle_file(__filename_folder__)


def test_lsa_wn():
  files = []
  for (dirpath, dirnames, filenames) in walk(__filename_folder__):
    for filename in filenames:
      files.append(__filename_folder__ + filename)

  files_string = []
  for filename in files:
    lines = [line.rstrip('\n') for line in open(filename)]
    string = " ".join(lines)
    files_string.append(string)

  vector_space = VS.VectorSpace(files_string, [TFIDF])

  sen_1 = "a financial institution that accepts deposits and channels the money into lending activities"
  sen_2 = "an organization that provides various financial services, for example keeping or lending money"
  sen_3 = "a supply of money or things that are used as money in some games, especially those in which gambling is involved"
  sen_4 = "a raised area of ground that slopes at the sides, often at the edge of sth or dividing sth"

  print vector_space.sim([sen_1],[sen_2])
  print vector_space.sim([sen_1],[sen_3])
  print vector_space.sim([sen_1],[sen_4])


def get_vector_space():
  files = []
  for (dirpath, dirnames, filenames) in walk(__filename_folder__):
    for filename in filenames:
      files.append(__filename_folder__ + filename)

  files_string = []
  for filename in files:
    lines = [line.rstrip('\n') for line in open(filename)]
    string = " ".join(lines)
    files_string.append(string)

  print "LSA creating ..."
  vector_space = VS.VectorSpace(files_string, [TFIDF])
  print "LSA done ..."
  return vector_space


__vector_space__ = get_vector_space()


def sim_tfidf(sen_1, sen_2):
  return __vector_space__.sim([sen_1],[sen_2])
