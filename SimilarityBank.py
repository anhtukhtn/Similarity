#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tu'

from nltk.corpus import wordnet as wn
# from  .metrics.pairwise import cosine_similarity
import ManualData
import DictProcess
import WordnetProcess
import FileProcess
from math import*


def square_rooted(x):

   return round(sqrt(sum([a*a for a in x])),3)


def cosine_similarity(x,y):

 numerator = sum(a*b for a,b in zip(x,y))
 denominator = square_rooted(x)*square_rooted(y)
 return round(numerator/float(denominator),3)





####################################################################################################
#
# @brief:   calculate similarity by nouns
#
def similarity_by_nouns():

  WORD = 'bank';
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BANK();
  dict_words_nouns = DictProcess.get_nouns(dict_words);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_nouns = WordnetProcess.get_nouns(WORD, wn_words);


  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # for bank in wn_words:
  #   print "\n"
  #   print bank.name()
  #   print wn.synset(bank.name()).hypernyms();
  #   print wn.synset(bank.name()).hyponyms();
  #   print wn.synset(bank.name()).definition();
  #
  # print "\n"
  #
  # for lemma in wn.synset('bank.n.01').lemmas():
  #   print  lemma.name()

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dictNoun in dict_words_nouns[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.0001;

        synsetsDictNoun = wn.synsets(dictNoun, pos = "n");
        if len(synsetsDictNoun) <= 0:
          continue

        # - - - - - - - - - - - - - - - - - - - - - - - -

        synset_of_word = wn.synset(wn_words[iWnWord].name());

        synset_dict_noun = synsetsDictNoun[0];
        # for synset_dict_noun in synsetsDictNoun:
        #   synset_dict_noun = synsetsDictNoun[0];

        p_dictNoun_wnNouns += synset_dict_noun.path_similarity(synset_of_word) * 1;
        countwnNouns += 1;

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wnNoun in wn_words_nouns[iWnWord]:
          #
          # print "------------ wn noun"
          # print wnNoun;

          synsetsWnNoun = wn.synsets(wnNoun);

          if len(synsetsDictNoun) > 0 and len(synsetsWnNoun) > 0:
            p_dictNoun_wnNoun = synset_dict_noun.path_similarity(synsetsWnNoun[0]);
            # print synset_dict_noun
            # print synsetsWnNoun[0]
            # print p_dictNoun_wnNoun
            if isinstance(p_dictNoun_wnNoun, (int, long, float, complex)):
              p_dictNoun_wnNouns += p_dictNoun_wnNoun;
              countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/countwnNouns;
        p_iWnWord_iDictWord += p_dictNoun_wnNouns;

      p_iWnWord_iDictWord = p_iWnWord_iDictWord/len(dict_words_nouns[iDictWord]);
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################

  print "--------------------------------------"
  for iWnWord in range(len(wn_words)):
    p_max = 0;
    i_max = 0;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(dict_words)):
      p = matrix_similarity[iWnWord][iDictWord];
      # if p != 0:
      #   print p;

      if p > p_max:
        p_max = p;
        i_max = iDictWord;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print "\n";
    print wn.synset(wn_words[iWnWord].name()).definition()
    print dict_words[i_max]["tv"]
    print p_max

  print "--------------------------------------"
  for iDictWord in range(len(dict_words)):
    p_max = 0;
    i_max = 0;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iWnWord in range(len(wn_words)):
      p = matrix_similarity[iWnWord][iDictWord];
      # if p != 0:
      #   print p;

      if p > p_max:
        p_max = p;
        i_max = iWnWord;

      # print "..............."
      # print dict_words[iDictWord]["tv"]
      # print wn_words[iWnWord]
      # print p
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print "\n";
    print dict_words[iDictWord]["tv"]
    print  wn.synset(wn_words[i_max].name()).definition()
    print p_max

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);
# - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  for i in range(len(dict_words)):
    matrix_similarity_dict[i].insert(0,dict_words[i]["tv"]);

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);
  for i in range(len(wn_words)):
    arrRowDict.append(wn.synset(wn_words[i].name()).definition());

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_concept_dict.csv",arrRowDict,matrix_similarity_dict)


  FileProcess.write_to_excel_file("Results/"+WORD+"_nouns.csv",arrRowDict,matrix_similarity)
  ####################################################################################################



####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets():

  WORD = 'bank';
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BANK();
  dict_words_nouns = DictProcess.get_nouns(dict_words);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # for bank in wn_words:
  #   print "\n"
  #   print bank.name()
  #   print wn.synset(bank.name()).hypernyms();
  #   print wn.synset(bank.name()).hyponyms();
  #   print wn.synset(bank.name()).definition();
  #
  # print "\n"
  #
  # for lemma in wn.synset('bank.n.01').lemmas():
  #   print  lemma.name()

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dictNoun in dict_words_nouns[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        synsetsDictNoun = wn.synsets(dictNoun, pos = "n");
        if len(synsetsDictNoun) <= 0:
          continue

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          # print "------------ wn noun"
          # print wnNoun;

          if len(synsetsDictNoun) > 0:
            p_max = 0;

            # for synset_dict_noun in synsetsDictNoun:
            #   # print "synset_dict_noun"
            #   # print synset_dict_noun
            #   # for hypernym in synset_dict_noun.hypernyms():
            #   #   print "hypernym"
            #   print "-----------------------------aaaa"
            #   print synset_dict_noun
            #   print wn_synset
            #   p = synset_dict_noun.path_similarity(wn_synset)
            #   if p> p_max:
            #     p_max = p;

            p_max = synsetsDictNoun[0].path_similarity(wn_synset);
            # p_max += synsetsDictNoun[len(synsetsDictNoun)-1].path_similarity(wn_synset);


            p_dictNoun_wnNouns += p_max;
            countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/countwnNouns;
        p_iWnWord_iDictWord += p_dictNoun_wnNouns;

      p_iWnWord_iDictWord = p_iWnWord_iDictWord/len(dict_words_nouns[iDictWord]);
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################

  print "--------------------------------------"
  for iWnWord in range(len(wn_words)):
    p_max = 0;
    i_max = 0;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(dict_words)):
      p = matrix_similarity[iWnWord][iDictWord];
      # if p != 0:
      #   print p;

      if p > p_max:
        p_max = p;
        i_max = iDictWord;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print "\n";
    print wn.synset(wn_words[iWnWord].name()).definition()
    print dict_words[i_max]["tv"]
    print p_max

  print "--------------------------------------"
  for iDictWord in range(len(dict_words)):
    p_max = 0;
    i_max = 0;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iWnWord in range(len(wn_words)):
      p = matrix_similarity[iWnWord][iDictWord];
      # if p != 0:
      #   print p;

      if p > p_max:
        p_max = p;
        i_max = iWnWord;

      # print "..............."
      # print dict_words[iDictWord]["tv"]
      # print wn_words[iWnWord]
      # print p
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print "\n";
    print dict_words[iDictWord]["tv"]
    print  wn.synset(wn_words[i_max].name()).definition()
    print p_max

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets.csv",arrRowDict,matrix_similarity)
  ####################################################################################################


# similarity_by_synsets();
# similarity_by_nouns();

####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets():

  WORD = 'bank';
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BANK();
  dict_words_synsets = DictProcess.get_synsets(dict_words);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # for bank in wn_words:
  #   print "\n"
  #   print bank.name()
  #   print wn.synset(bank.name()).hypernyms();
  #   print wn.synset(bank.name()).hyponyms();
  #   print wn.synset(bank.name()).definition();
  #
  # print "\n"
  #
  # for lemma in wn.synset('bank.n.01').lemmas():
  #   print  lemma.name()

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          # print "------------ wn noun"
          # print wnNoun;

          p_max = dict_synset.path_similarity(wn_synset);

          p_dictNoun_wnNouns += p_max;
          countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/countwnNouns;
        p_iWnWord_iDictWord += p_dictNoun_wnNouns;

      p_iWnWord_iDictWord = p_iWnWord_iDictWord/len(dict_words_synsets[iDictWord]);
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################

  print "--------------------------------------"
  for iWnWord in range(len(wn_words)):
    p_max = 0;
    i_max = 0;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(dict_words)):
      p = matrix_similarity[iWnWord][iDictWord];
      # if p != 0:
      #   print p;

      if p > p_max:
        p_max = p;
        i_max = iDictWord;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print "\n";
    print wn.synset(wn_words[iWnWord].name()).definition()
    print dict_words[i_max]["tv"]
    print p_max

  print "--------------------------------------"
  for iDictWord in range(len(dict_words)):
    p_max = 0;
    i_max = 0;
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iWnWord in range(len(wn_words)):
      p = matrix_similarity[iWnWord][iDictWord];
      # if p != 0:
      #   print p;

      if p > p_max:
        p_max = p;
        i_max = iWnWord;

      # print "..............."
      # print dict_words[iDictWord]["tv"]
      # print wn_words[iWnWord]
      # print p
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print "\n";
    print dict_words[iDictWord]["tv"]
    print  wn.synset(wn_words[i_max].name()).definition()
    print p_max

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets.csv",arrRowDict,matrix_similarity)
  ####################################################################################################

# similarity_by_nouns()
# similarity_by_synsets_synsets();


####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest():

  WORD = 'bank'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BANK();
  dict_words_synsets = DictProcess.get_nbest_synsets(dict_words);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # for bank in wn_words:
  #   print "\n"
  #   print bank.name()
  #   print wn.synset(bank.name()).hypernyms();
  #   print wn.synset(bank.name()).hyponyms();
  #   print wn.synset(bank.name()).definition();
  #
  # print "\n"
  #
  # for lemma in wn.synset('bank.n.01').lemmas():
  #   print  lemma.name()

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # print "---------------------- iwnword - iDict"
      # print wn_words[iWnWord]
      # print dict_words[iDictWord]
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          # print "------------ wn- dict"
          # print wn_synset;
          # print dict_synset


          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);

          # print p_max

          # p_dictNoun_wnNouns += p_max;
          # countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          p_iWnWord_iDictWord += arr_p_word[i];
          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # print "--------------------------------------"
  # for iWnWord in range(len(wn_words)):
  #   p_max = 0;
  #   i_max = 0;
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   for iDictWord in range(len(dict_words)):
  #     p = matrix_similarity[iWnWord][iDictWord];
  #     # if p != 0:
  #     #   print p;
  #
  #     if p > p_max:
  #       p_max = p;
  #       i_max = iDictWord;
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   print "\n";
  #   print wn.synset(wn_words[iWnWord].name()).definition()
  #   print dict_words[i_max]["tv"]
  #   print p_max
  #
  # print "--------------------------------------"
  # for iDictWord in range(len(dict_words)):
  #   p_max = 0;
  #   i_max = 0;
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   for iWnWord in range(len(wn_words)):
  #     p = matrix_similarity[iWnWord][iDictWord];
  #     # if p != 0:
  #     #   print p;
  #
  #     if p > p_max:
  #       p_max = p;
  #       i_max = iWnWord;
  #
  #     # print "..............."
  #     # print dict_words[iDictWord]["tv"]
  #     # print wn_words[iWnWord]
  #     # print p
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   print "\n";
  #   print dict_words[iDictWord]["tv"]
  #   print  wn.synset(wn_words[i_max].name()).definition()
  #   print p_max

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest.csv",arrRowDict,matrix_similarity)
  ####################################################################################################

# similarity_by_synsets_synsets_nbest();

####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword():

  WORD = 'bank'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BANK();
  dict_words_synsets = DictProcess.get_nbest_synsets_n_v_with_word(dict_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # for bank in wn_words:
  #   print "\n"
  #   print bank.name()
  #   print wn.synset(bank.name()).hypernyms();
  #   print wn.synset(bank.name()).hyponyms();
  #   print wn.synset(bank.name()).definition();
  #
  # print "\n"
  #
  # for lemma in wn.synset('bank.n.01').lemmas():
  #   print  lemma.name()

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # print "---------------------- iwnword - iDict"
      # print wn_words[iWnWord]
      # print dict_words[iDictWord]
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          # print "------------ wn- dict"
          # print wn_synset;
          # print dict_synset


          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);

          # print p_max

          # p_dictNoun_wnNouns += p_max;
          # countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        count = 0;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # print "--------------------------------------"
  # for iWnWord in range(len(wn_words)):
  #   p_max = 0;
  #   i_max = 0;
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   for iDictWord in range(len(dict_words)):
  #     p = matrix_similarity[iWnWord][iDictWord];
  #     # if p != 0:
  #     #   print p;
  #
  #     if p > p_max:
  #       p_max = p;
  #       i_max = iDictWord;
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   print "\n";
  #   print wn.synset(wn_words[iWnWord].name()).definition()
  #   print dict_words[i_max]["tv"]
  #   print p_max
  #
  # print "--------------------------------------"
  # for iDictWord in range(len(dict_words)):
  #   p_max = 0;
  #   i_max = 0;
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   for iWnWord in range(len(wn_words)):
  #     p = matrix_similarity[iWnWord][iDictWord];
  #     # if p != 0:
  #     #   print p;
  #
  #     if p > p_max:
  #       p_max = p;
  #       i_max = iWnWord;
  #
  #     # print "..............."
  #     # print dict_words[iDictWord]["tv"]
  #     # print wn_words[iWnWord]
  #     # print p
  #   # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #   print "\n";
  #   print dict_words[iDictWord]["tv"]
  #   print  wn.synset(wn_words[i_max].name()).definition()
  #   print p_max

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword.csv",arrRowDict,matrix_similarity)
  ####################################################################################################


####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword_reverse():

  WORD = 'bank'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  wn_words = ManualData.DATA_BANK();
  wn_words_synsets = DictProcess.get_nbest_synsets_with_word(wn_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  dict_words = wn.synsets(WORD, pos = 'n');
  # print wn_words;
  dict_words_synsets = WordnetProcess.get_synsets(WORD, dict_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # for bank in wn_words:
  #   print "\n"
  #   print bank.name()
  #   print wn.synset(bank.name()).hypernyms();
  #   print wn.synset(bank.name()).hyponyms();
  #   print wn.synset(bank.name()).definition();
  #
  # print "\n"
  #
  # for lemma in wn.synset('bank.n.01').lemmas():
  #   print  lemma.name()

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # print "---------------------- iwnword - iDict"
      # print wn_words[iWnWord]
      # print dict_words[iDictWord]
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          # print "------------ wn- dict"
          # print wn_synset;
          # print dict_synset


          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);

          # print p_max

          # p_dictNoun_wnNouns += p_max;
          # countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn_words[i]["tv"]);

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(wn.synset(dict_words[i].name()).definition());

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_reverse.csv",arrRowDict,matrix_similarity)
  ####################################################################################################


####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword_average():

  WORD = 'baby'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BABY();
  dict_words_synsets = DictProcess.get_nbest_synsets_n_v_with_word(dict_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets_n_v(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # for bank in wn_words:
  #   print "\n"
  #   print bank.name()
  #   print wn.synset(bank.name()).hypernyms();
  #   print wn.synset(bank.name()).hyponyms();
  #   print wn.synset(bank.name()).definition();
  #
  # print "\n"
  #
  # for lemma in wn.synset('bank.n.01').lemmas():
  #   print  lemma.name()

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # print "---------------------- iwnword - iDict"
      # print wn_words[iWnWord]
      # print dict_words[iDictWord]
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          # print "------------ wn- dict"
          # print wn_synset;
          # print dict_synset


          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);

          # print p_max

          # p_dictNoun_wnNouns += p_max;
          # countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 3;
        count = 0.0001;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 40;
      count = 5;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*10.;
            elif i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
          else:
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*10.;
            elif i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  wn_words = ManualData.DATA_BABY();
  wn_words_synsets = DictProcess.get_nbest_synsets_n_v_with_word(wn_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  dict_words = wn.synsets(WORD, pos = 'n');
  # print wn_words;
  dict_words_synsets = WordnetProcess.get_synsets_n_v(WORD, dict_words);

  print "sysnets -----------------------.----.-----.--.-"

  # matrix for similarity dict_words vs wn_words
  matrix_similarity_reverse = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # print "---------------------- iwnword - iDict"
      # print wn_words[iWnWord]
      # print dict_words[iDictWord]
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          # print "------------ wn- dict"
          # print wn_synset;
          # print dict_synset


          p_max = dict_synset.path_similarity(wn_synset);
          if p_max != None:
            arr_p.append(p_max);

          # print p_max

          # p_dictNoun_wnNouns += p_max;
          # countwnNouns = countwnNouns + 1;
          # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 3;
        count = 0
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count +=1

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 40;
      count = 5;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*10;
            elif i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
          else:
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*10.;
            elif i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_reverse[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity_reverse]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  dict_words = ManualData.DATA_BABY();

  wn_words = wn.synsets(WORD, pos = 'n');

  for iWnWord in range(len(wn_words)):
    for iDictWord in range(len(dict_words)):
      matrix_similarity[iWnWord][iDictWord] = matrix_similarity[iWnWord][iDictWord] + matrix_similarity_reverse[iDictWord][iWnWord];
      matrix_similarity[iWnWord][iDictWord] /= 2;

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_average.csv",arrRowDict,matrix_similarity)
  ####################################################################################################


# similarity_by_synsets_synsets_nbest_withword();

#
def similarity_by_synsets_synsets_nbest_withword_concept():

  WORD = 'board'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BOARD();
  dict_words_synsets = DictProcess.get_nbest_synsets_with_word(dict_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet dataG

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity_dict = [[0 for x in range(len(dict_words) + len(wn_words))] for x in range(len(dict_words))];
  matrix_similarity_wn = [[0 for x in range(len(wn_words)+len(dict_words))] for x in range(len(wn_words))];

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_wn[iWnWord][iDictWord] = p_iWnWord_iDictWord;

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(wn_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in wn_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_wn[iWnWord][iDictWord + len(dict_words)] = p_iWnWord_iDictWord;


  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity_wn]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  # ####################################################################################################
  # #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  # for i in range(len(wn_words)):
  #   matrix_similarity_wn[i].insert(0,wn.synset(wn_words[i].name()).definition());
  #
  # # - - - - - - - - - - - - - - - - - - - - - - - - -
  # # row
  arrRowDict = [];
  # arrRowDict.append("--");
  # for i in range(len(dict_words)):
  #   arrRowDict.append(dict_words[i]["tv"]);
  # for i in range(len(wn_words)):
  #   arrRowDict.append(wn.synset(wn_words[i].name()).definition());

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_concept_wn.csv",arrRowDict,matrix_similarity_wn)

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(dict_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in dict_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 10;
        count = 0;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 3;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_dict[iWnWord][iDictWord] = p_iWnWord_iDictWord;

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(wn_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in wn_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in dict_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 10;
        count = 0;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 3;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/2:
              p_iWnWord_iDictWord += arr_p_word[i]*1.0;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_dict[iWnWord][iDictWord + len(dict_words)] = p_iWnWord_iDictWord;


  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity_dict]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  # ####################################################################################################
  # #
  # write fie

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  # for i in range(len(dict_words)):
  #   matrix_similarity_dict[i].insert(0,dict_words[i]["tv"]);
  #
  # # - - - - - - - - - - - - - - - - - - - - - - - - -
  # # row
  arrRowDict = [];
  # arrRowDict.append("--");
  # for i in range(len(dict_words)):
  #   arrRowDict.append(dict_words[i]["tv"]);
  # for i in range(len(wn_words)):
  #   arrRowDict.append(wn.synset(wn_words[i].name()).definition());

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_concept_dict.csv",arrRowDict,matrix_similarity_dict)
  ####################################################################################################

  matrix_similarity_cosine = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  ####################################################################################################
  #
  # calculate 2d matrix of cosine

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):
      vector_dict = matrix_similarity_dict[iDictWord];
      vector_wn = matrix_similarity_wn[iWnWord];

      matrix_similarity_cosine[iWnWord][iDictWord] = cosine_similarity(vector_dict,vector_wn);


  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  # write
  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity_cosine[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_concept_cosine.csv",arrRowDict,matrix_similarity_cosine)

  ####################################################################################################


# similarity_by_synsets_synsets_nbest_withword_concept()

#
def similarity_by_synsets_synsets_nbest_withword_concept_other():

  WORD = 'bank'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BANK();
  dict_words_synsets = DictProcess.get_nbest_synsets_with_word(dict_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets(WORD, wn_words);

  WORD_PLUS = 'bank';
  wn_words_plus = wn.synsets(WORD_PLUS, pos = 'n');
  wn_words_synsets_plus = WordnetProcess.get_synsets(WORD_PLUS, wn_words_plus);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity_dict = [[0 for x in range(len(dict_words) + len(wn_words)+len(wn_words_plus))] for x in range(len(dict_words))];
  matrix_similarity_wn = [[0 for x in range(len(wn_words)+len(dict_words) + len(wn_words_plus))] for x in range(len(wn_words))];

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_wn[iWnWord][iDictWord] = p_iWnWord_iDictWord;

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(wn_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in wn_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_wn[iWnWord][iDictWord + len(dict_words)] = p_iWnWord_iDictWord;


    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(wn_words_plus)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in wn_words_synsets_plus[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_wn[iWnWord][iDictWord + len(dict_words) + len(wn_words)] = p_iWnWord_iDictWord;


  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity_wn]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  # ####################################################################################################
  # #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  # for i in range(len(wn_words)):
  #   matrix_similarity_wn[i].insert(0,wn.synset(wn_words[i].name()).definition());
  #
  # # - - - - - - - - - - - - - - - - - - - - - - - - -
  # # row
  arrRowDict = [];
  # arrRowDict.append("--");
  # for i in range(len(dict_words)):
  #   arrRowDict.append(dict_words[i]["tv"]);
  # for i in range(len(wn_words)):
  #   arrRowDict.append(wn.synset(wn_words[i].name()).definition());

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_concept_other_wn.csv",arrRowDict,matrix_similarity_wn)

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(dict_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in dict_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 10;
        count = 0;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 3;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_dict[iWnWord][iDictWord] = p_iWnWord_iDictWord;

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(wn_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in wn_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in dict_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 10;
        count = 0;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 3;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/2:
              p_iWnWord_iDictWord += arr_p_word[i]*1.0;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_dict[iWnWord][iDictWord + len(dict_words)] = p_iWnWord_iDictWord;

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for iDictWord in range(len(wn_words_plus)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      # - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      for dict_synset in wn_words_synsets_plus[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in dict_words_synsets[iWnWord]:
          p_max = dict_synset.path_similarity(wn_synset);
          arr_p.append(p_max);
        # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/nBest;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;
          else:
            if i< len(arr_p_word)/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.25;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.875;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity_dict[iWnWord][iDictWord + len(dict_words) + len(wn_words)] = p_iWnWord_iDictWord;


  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity_dict]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  # ####################################################################################################
  # #
  # write fie

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  # for i in range(len(dict_words)):
  #   matrix_similarity_dict[i].insert(0,dict_words[i]["tv"]);
  #
  # # - - - - - - - - - - - - - - - - - - - - - - - - -
  # # row
  arrRowDict = [];
  # arrRowDict.append("--");
  # for i in range(len(dict_words)):
  #   arrRowDict.append(dict_words[i]["tv"]);
  # for i in range(len(wn_words)):
  #   arrRowDict.append(wn.synset(wn_words[i].name()).definition());

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_concept_other_dict.csv",arrRowDict,matrix_similarity_dict)


  ####################################################################################################

  matrix_similarity_cosine = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  ####################################################################################################
  #
  # calculate 2d matrix of cosine

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):
      vector_dict = matrix_similarity_dict[iDictWord];
      vector_wn = matrix_similarity_wn[iWnWord];

      matrix_similarity_cosine[iWnWord][iDictWord] = cosine_similarity(vector_dict,vector_wn);


  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  # write
  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity_cosine[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_concept_other_cosine.csv",arrRowDict,matrix_similarity_cosine)

  ####################################################################################################

# similarity_by_synsets()
# similarity_by_synsets_synsets()
# similarity_by_synsets_synsets_nbest()
# similarity_by_synsets_synsets_nbest_withword()
# similarity_by_synsets_synsets_nbest_withword_reverse()
similarity_by_synsets_synsets_nbest_withword_average()
# # similarity_by_synsets_synsets_nbest_withword_concept()
# similarity_by_synsets_synsets_nbest_withword_concept_other()



####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword_verb():

  WORD = 'bee'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BEE();
  dict_words_synsets = DictProcess.get_nbest_synsets_n_v_with_word(dict_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets_n_v(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];

      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:

          p_max = dict_synset.path_similarity(wn_synset);

          if p_max == None:
            continue

          arr_p.append(p_max);

        arr_p = sorted(arr_p, reverse=True);

        nBest = 10;
        count =0;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/5.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.8;
            elif i < nBest*2/5.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.4;
          else:
            if i< len(arr_p_word)/5.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.8;
            elif i < nBest*2/5.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.4;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/verb/"+WORD+"_synsets_synsets_nbest_n_v_withword.csv",arrRowDict,matrix_similarity)
  ####################################################################################################



####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword_verb_x():

  WORD = 'bag'
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data

  dict_words = ManualData.DATA_BAG();
  dict_words_synsets = DictProcess.get_nbest_synsets_n_v_x_with_word(dict_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print wn_words;
  wn_words_synsets = WordnetProcess.get_synsets_n_v(WORD, wn_words);

  print "sysnets -----------------------.----.-----.--.-"
  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];

      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:

          p_max = dict_synset.path_similarity(wn_synset);

          if p_max == None:
            continue

          arr_p.append(p_max);

        arr_p = sorted(arr_p, reverse=True);

        nBest = 30;
        count =0;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 30;
      count = 0;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i< nBest/8.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.8;
            elif i < nBest*2/8.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.4;
          else:
            if i< len(arr_p_word)/8.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.8;
            elif i < nBest*2/8.:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*0.4;

          count += 1;

      if count == 0:
        p_iWnWord_iDictWord = 0;
      else:
        p_iWnWord_iDictWord = p_iWnWord_iDictWord/count
      matrix_similarity[iWnWord][iDictWord] = p_iWnWord_iDictWord;
      # - - - - - - - - - - - - - - - - - - - - - - - - -

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  ####################################################################################################

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################
  #
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # col
  arrColWn = [];
  for i in range(len(wn_words)):
    matrix_similarity[i].insert(0,wn.synset(wn_words[i].name()).definition());

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    arrRowDict.append(dict_words[i]["tv"]);

  FileProcess.write_to_excel_file("Results/verb/"+WORD+"_synsets_synsets_nbest_n_v_x_withword.csv",arrRowDict,matrix_similarity)
  ####################################################################################################

# similarity_by_synsets_synsets_nbest_withword_verb_x()

  # xử lí biến cách: infection. books, book
  #



  # xử lí biến cách: infection. books, book
  # dẫn xuất:  Porter's stemmer
