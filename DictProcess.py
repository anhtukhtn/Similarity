#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tu'

import nltk
from nltk.corpus import wordnet as wn
import POSWrapper


####################################################################################################
#
# @brief: get nouns of a word from sd, d
#
# @param: dict_words
#         list of word. Each word is a dictionary. E.g. 
              #  bank_1["en"] = "bank";
              #  bank_1["sd"] = "money";
              #  bank_1["d"] = "an organization that provides various financial services, for example keeping or lending money";
              #  bank_1["tv"] = "ngan hang";
              #  bank_1["x1"] = "My salary is paid directly into my bank";
              #  bank_1["x2"] = "I need to go to the bank(= the local office of the bank)";
              #  bank_1["x3"] = "a bank loan";
              #  bank_1["x4"] = "a bank manager"
#
# @return list of nouns of each word
#
def get_nouns(dict_words):

  dict_words_nouns = [];

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);

    wordDict = dict_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["sd"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # d

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

  ########################################
  return dict_words_nouns;
  ########################################

####################################################################################################
#
# @brief: get synsets of a word from sd, d
#
# @param: dict_words
#         list of word. Each word is a dictionary. E.g.
              #  bank_1["en"] = "bank";
              #  bank_1["sd"] = "money";
              #  bank_1["d"] = "an organization that provides various financial services, for example keeping or lending money";
              #  bank_1["tv"] = "ngan hang";
              #  bank_1["x1"] = "My salary is paid directly into my bank";
              #  bank_1["x2"] = "I need to go to the bank(= the local office of the bank)";
              #  bank_1["x3"] = "a bank loan";
              #  bank_1["x4"] = "a bank manager"
#
# @return list of synsets of each word
#
def get_synsets(dict_words):

  dict_words_nouns = [];
  dict_synsets_nouns = [];

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_nouns.append([]);

    wordDict = dict_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["sd"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      if noun != "sth" and noun != 'etc' and noun not in dict_words_nouns[iWord]:
        dict_words_nouns[iWord].append(noun);

    print dict_words_nouns[iWord]
    synsetsSD = wn.synsets(dict_words_nouns[iWord][len(dict_words_nouns[iWord])-1], pos = 'n');

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # d

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)-1):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      for iNoun in range(len(dict_words_nouns[iWord])-1):
        if iNoun == 0:
          continue;
        synsets_noun = wn.synsets(dict_words_nouns[iWord][iNoun], pos = 'n');
        p_noun_max = 0;

        for synset_noun in synsets_noun:
          p = synsetSD.path_similarity(synset_noun);
          # print synsetSD
          # print synset_noun
          # print p
          if p > p_noun_max:
            p_noun_max = p;

        pSD += p_noun_max;

      # print "\n"

      if pSD > pSD_max:
        # print pSD
        # print pSD_max
        pSD_max = pSD;
        # print iSyn
        # print iSDMax
        iSDMax = iSyn;

    # print "\n"

    synsetRoot = synsetsSD[0];
    print "synsetroot"
    print synsetRoot

    for noun in dict_words_nouns[iWord]:
      synsets_noun = wn.synsets(noun, pos = 'n');
      if len(synsets_noun) <= 0:
        continue;

      p_noun_max = 0;
      synMax = synsets_noun[0];

      for synset_noun in synsets_noun:
        p = synsetRoot.path_similarity(synset_noun);
        if p > p_noun_max:
          p_noun_max = p;
          synMax = synset_noun;

      dict_synsets_nouns[iWord].append(synMax);
      # dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_nouns[iWord]



  ########################################
  return dict_synsets_nouns;
  ########################################


####################################################################################################
#
# @brief: get synsets of a word from sd, d
#
# @param: dict_words
#         list of word. Each word is a dictionary. E.g.
              #  bank_1["en"] = "bank";
              #  bank_1["sd"] = "money";
              #  bank_1["d"] = "an organization that provides various financial services, for example keeping or lending money";
              #  bank_1["tv"] = "ngan hang";
              #  bank_1["x1"] = "My salary is paid directly into my bank";
              #  bank_1["x2"] = "I need to go to the bank(= the local office of the bank)";
              #  bank_1["x3"] = "a bank loan";
              #  bank_1["x4"] = "a bank manager"
#
# @return list of synsets of each word
#
def get_nbest_synsets(dict_words):

  dict_words_nouns = [];
  dict_synsets_nouns = [];

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_nouns.append([]);

    wordDict = dict_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["sd"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != "sth" and noun != 'etc' and noun not in dict_words_nouns[iWord]:
        dict_words_nouns[iWord].append(noun);

    print dict_words_nouns[iWord]
    synsetsSD = wn.synsets(dict_words_nouns[iWord][len(dict_words_nouns[iWord])-1], pos = 'n');

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # d

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)-1):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      arr_p = [];

      for iNoun in range(len(dict_words_nouns[iWord])-1):
        if iNoun == 0:
          continue;
        synsets_noun = wn.synsets(dict_words_nouns[iWord][iNoun], pos = 'n');
        p_noun_max = 0;

        for synset_noun in synsets_noun:
          p = synsetSD.path_similarity(synset_noun);
          # arr_p.append(p);
          # print synsetSD
          # print synset_noun
          # print p
          if p > p_noun_max:
            p_noun_max = p;

        arr_p.append(p_noun_max);

      arr_p = sorted(arr_p, reverse=True);

      for i in xrange(0, len(arr_p)-1):
        if i <= 3:
          pSD += arr_p[i];

      # print "\n"

      if pSD > pSD_max:
        # print pSD
        # print pSD_max
        pSD_max = pSD;
        # print iSyn
        # print iSDMax
        iSDMax = iSyn;

    # print "\n"

    synsetRoot = synsetsSD[iSDMax];
    print "synsetroot"
    print synsetRoot

    for noun in dict_words_nouns[iWord]:
      synsets_noun = wn.synsets(noun, pos = 'n');
      if len(synsets_noun) <= 0:
        continue;

      p_noun_max = 0;
      synMax = synsets_noun[0];

      for synset_noun in synsets_noun:
        p = synsetRoot.path_similarity(synset_noun);
        if p > p_noun_max:
          p_noun_max = p;
          synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synMax);
      if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 2:
    #   synsetRoot = synsetsSD[1];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 3:
    #   synsetRoot = synsetsSD[2];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_nouns[iWord]



  ########################################
  return dict_synsets_nouns;
  ########################################

####################################################################################################
#
# @brief: get synsets of a word from sd, d
#
# @param: dict_words
#         list of word. Each word is a dictionary. E.g.
              #  bank_1["en"] = "bank";
              #  bank_1["sd"] = "money";
              #  bank_1["d"] = "an organization that provides various financial services, for example keeping or lending money";
              #  bank_1["tv"] = "ngan hang";
              #  bank_1["x1"] = "My salary is paid directly into my bank";
              #  bank_1["x2"] = "I need to go to the bank(= the local office of the bank)";
              #  bank_1["x3"] = "a bank loan";
              #  bank_1["x4"] = "a bank manager"
#
# @return list of synsets of each word
#
def get_nbest_synsets_with_word(dict_words,word_concept):

  dict_words_nouns = [];
  dict_synsets_nouns = [];

  wn_words = wn.synsets(word_concept, pos = 'n');

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_nouns.append([]);

    wordDict = dict_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["sd"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != "sth" and noun != 'etc' and noun not in dict_words_nouns[iWord]:
        dict_words_nouns[iWord].append(noun);

    print dict_words_nouns[iWord]
    synsetsSD = wn.synsets(dict_words_nouns[iWord][len(dict_words_nouns[iWord])-1], pos = 'n');

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # d

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)-1):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      arr_p = [];

      for synset in wn_words:
        p_noun_max = 0;
        p = synsetSD.path_similarity(synset);
          # arr_p.append(p);
        # print "-----------------------"
        # print synsetSD
        # print synset
        # print p
        if p > p_noun_max:
          p_noun_max = p;

        arr_p.append(p_noun_max);

      arr_p = sorted(arr_p, reverse=True);

      for i in xrange(0, len(arr_p)-1):
        if i <= 1:
          pSD += arr_p[i];

      # print "\n"

      if pSD > pSD_max:
        # print pSD
        # print pSD_max
        pSD_max = pSD;
        # print iSyn
        # print iSDMax
        iSDMax = iSyn;

    # print "\n"

    synsetRoot = synsetsSD[iSDMax];
    print "synsetroot"
    print synsetRoot

    for noun in dict_words_nouns[iWord]:
      synsets_noun = wn.synsets(noun, pos = 'n');
      if len(synsets_noun) <= 0:
        continue;

      p_noun_max = 0;
      synMax = synsets_noun[0];

      for synset_noun in synsets_noun:
        p = synsetRoot.path_similarity(synset_noun);
        if p > p_noun_max:
          p_noun_max = p;
          synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synMax);
      if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 1:
    #   synsetRoot = synsetsSD[0];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 3:
    #   synsetRoot = synsetsSD[2];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_nouns[iWord]



  ########################################
  return dict_synsets_nouns;
  ########################################

def get_nbest_synsets_n_v_with_word(dict_words,word_concept):

  dict_words_nouns = [];
  dict_synsets_nouns = [];

  wn_words = wn.synsets(word_concept, pos = 'n');

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_nouns.append([]);

    wordDict = dict_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["sd"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != "sth" and noun != 'etc' and noun not in dict_words_nouns[iWord]:
        dict_words_nouns[iWord].append(noun);

    print dict_words_nouns[iWord]
    synsetsSD = wn.synsets(dict_words_nouns[iWord][len(dict_words_nouns[iWord])-1], pos = 'n');

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # d

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ')];

    # print  tagged_sent

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)-1):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      arr_p = [];

      for synset in wn_words:
        p_noun_max = 0;
        p = synsetSD.path_similarity(synset);
          # arr_p.append(p);
        # print "-----------------------"
        # print synsetSD
        # print synset
        # print p
        if p > p_noun_max:
          p_noun_max = p;

        arr_p.append(p_noun_max);

      arr_p = sorted(arr_p, reverse=True);

      for i in xrange(0, len(arr_p)-1):
        if i <= 1:
          pSD += arr_p[i];

      # print "\n"

      if pSD > pSD_max:
        # print pSD
        # print pSD_max
        pSD_max = pSD;
        # print iSyn
        # print iSDMax
        iSDMax = iSyn;

    # print "\n"

    synsetRoot = synsetsSD[iSDMax];
    print "synsetroot"
    print synsetRoot

    for noun in dict_words_nouns[iWord]:
      synsets_noun = wn.synsets(noun, pos = 'n');
      if len(synsets_noun) <= 0:
        continue;

      p_noun_max = 0;
      synMax = synsets_noun[0];

      for synset_noun in synsets_noun:
        p = synsetRoot.path_similarity(synset_noun);
        if p > p_noun_max:
          p_noun_max = p;
          synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synMax);
      if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 1:
    #   synsetRoot = synsetsSD[0];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 3:
    #   synsetRoot = synsetsSD[2];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);


    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBN' or pos == 'VBD')];
    print "VVVVV"
    print nouns
    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)-1):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      arr_p = [];

      for synset in wn_words:
        p_noun_max = 0;
        p = synsetSD.path_similarity(synset);
          # arr_p.append(p);
        # print "-----------------------"
        # print synsetSD
        # print synset
        # print p
        if p > p_noun_max:
          p_noun_max = p;

        arr_p.append(p_noun_max);

      arr_p = sorted(arr_p, reverse=True);

      for i in xrange(0, len(arr_p)-1):
        if i <= 1:
          pSD += arr_p[i];

      # print "\n"

      if pSD > pSD_max:
        # print pSD
        # print pSD_max
        pSD_max = pSD;
        # print iSyn
        # print iSDMax
        iSDMax = iSyn;

    # print "\n"

    synsetRoot = synsetsSD[iSDMax];
    print "synsetroot"
    print synsetRoot

    for noun in dict_words_nouns[iWord]:
      synsets_noun = wn.synsets(noun, pos = 'v');
      if len(synsets_noun) <= 0:
        continue;

      p_noun_max = 0;
      synMax = synsets_noun[0];

      for synset_noun in synsets_noun:
        p = synsetRoot.path_similarity(synset_noun);
        if p > p_noun_max:
          p_noun_max = p;
          synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        print synMax
        dict_synsets_nouns[iWord].append(synMax);
      if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_nouns[iWord]

  ########################################
  return dict_synsets_nouns;
  ########################################


def get_nbest_synsets_n_v_x_with_word(dict_words,word_concept):

  dict_words_nouns = [];
  dict_synsets_nouns = [];

  wn_words = wn.synsets(word_concept, pos = 'n');

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_nouns.append([]);

    wordDict = dict_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["sd"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != "sth" and noun != 'etc' and noun not in dict_words_nouns[iWord]:
        dict_words_nouns[iWord].append(noun);

    print dict_words_nouns[iWord]
    synsetsSD = wn.synsets(dict_words_nouns[iWord][len(dict_words_nouns[iWord])-1], pos = 'n');

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # d

    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)-1):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      arr_p = [];

      for synset in wn_words:
        p_noun_max = 0;
        p = synsetSD.path_similarity(synset);
          # arr_p.append(p);
        # print "-----------------------"
        # print synsetSD
        # print synset
        # print p
        if p > p_noun_max:
          p_noun_max = p;

        arr_p.append(p_noun_max);

      arr_p = sorted(arr_p, reverse=True);

      for i in xrange(0, len(arr_p)-1):
        if i <= 1:
          pSD += arr_p[i];

      # print "\n"

      if pSD > pSD_max:
        # print pSD
        # print pSD_max
        pSD_max = pSD;
        # print iSyn
        # print iSDMax
        iSDMax = iSyn;

    # print "\n"

    synsetRoot = synsetsSD[iSDMax];
    print "synsetroot"
    print synsetRoot

    for noun in dict_words_nouns[iWord]:
      synsets_noun = wn.synsets(noun, pos = 'n');
      if len(synsets_noun) <= 0:
        continue;

      p_noun_max = 0;
      synMax = synsets_noun[0];

      for synset_noun in synsets_noun:
        p = synsetRoot.path_similarity(synset_noun);
        if p > p_noun_max:
          p_noun_max = p;
          synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synMax);
      if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 1:
    #   synsetRoot = synsetsSD[0];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);

    # if len(synsetsSD) >= 3:
    #   synsetRoot = synsetsSD[2];
    #   print "synsetroot"
    #   print synsetRoot
    #
    #   for noun in dict_words_nouns[iWord]:
    #     synsets_noun = wn.synsets(noun, pos = 'n');
    #     if len(synsets_noun) <= 0:
    #       continue;
    #
    #     p_noun_max = 0;
    #     synMax = synsets_noun[0];
    #
    #     for synset_noun in synsets_noun:
    #       p = synsetRoot.path_similarity(synset_noun);
    #       if p > p_noun_max:
    #         p_noun_max = p;
    #         synMax = synset_noun;
    #
    #     if synMax not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synMax);
    #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
    #       dict_synsets_nouns[iWord].append(synsets_noun[0]);


    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBN' or pos == 'VBD')];
    print "VVVVV"
    print nouns
    for noun in nouns:
      noun = wn.morphy(noun);
      if noun == None:
        continue

      if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
        # print noun;
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)-1):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      arr_p = [];

      for synset in wn_words:
        p_noun_max = 0;
        p = synsetSD.path_similarity(synset);
          # arr_p.append(p);
        # print "-----------------------"
        # print synsetSD
        # print synset
        # print p
        if p > p_noun_max:
          p_noun_max = p;

        arr_p.append(p_noun_max);

      arr_p = sorted(arr_p, reverse=True);

      for i in xrange(0, len(arr_p)-1):
        if i <= 1:
          pSD += arr_p[i];

      # print "\n"

      if pSD > pSD_max:
        # print pSD
        # print pSD_max
        pSD_max = pSD;
        # print iSyn
        # print iSDMax
        iSDMax = iSyn;

    # print "\n"

    synsetRoot = synsetsSD[iSDMax];
    print "synsetroot"
    print synsetRoot

    for noun in dict_words_nouns[iWord]:
      synsets_noun = wn.synsets(noun, pos = 'v');
      if len(synsets_noun) <= 0:
        continue;

      p_noun_max = 0;
      synMax = synsets_noun[0];

      for synset_noun in synsets_noun:
        p = synsetRoot.path_similarity(synset_noun);
        if p > p_noun_max:
          p_noun_max = p;
          synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        print synMax
        dict_synsets_nouns[iWord].append(synMax);
      if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synsets_noun[0]);


    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # x1

    if wordDict.has_key("x1"):
      tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["x1"]));
      nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

      for noun in nouns:
        noun = wn.morphy(noun);
        if noun == None:
          continue

        if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
          # print noun;
          dict_words_nouns[iWord].append(noun);

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      print wordDict["tv"]
      print dict_words_nouns[iWord]

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      # synsets

      iSDMax = 0;
      pSD_max = 0;

      for iSyn in range(len(synsetsSD)-1):
        synsetSD = synsetsSD[iSyn];
        pSD = 0;

        arr_p = [];

        for synset in wn_words:
          p_noun_max = 0;
          p = synsetSD.path_similarity(synset);
            # arr_p.append(p);
          # print "-----------------------"
          # print synsetSD
          # print synset
          # print p
          if p > p_noun_max:
            p_noun_max = p;

          arr_p.append(p_noun_max);

        arr_p = sorted(arr_p, reverse=True);

        for i in xrange(0, len(arr_p)-1):
          if i <= 1:
            pSD += arr_p[i];

        # print "\n"

        if pSD > pSD_max:
          # print pSD
          # print pSD_max
          pSD_max = pSD;
          # print iSyn
          # print iSDMax
          iSDMax = iSyn;

      # print "\n"

      synsetRoot = synsetsSD[iSDMax];
      print "synsetroot"
      print synsetRoot

      for noun in dict_words_nouns[iWord]:
        synsets_noun = wn.synsets(noun, pos = 'n');
        if len(synsets_noun) <= 0:
          continue;

        p_noun_max = 0;
        synMax = synsets_noun[0];

        for synset_noun in synsets_noun:
          p = synsetRoot.path_similarity(synset_noun);
          if p > p_noun_max:
            p_noun_max = p;
            synMax = synset_noun;

        if synMax not in dict_synsets_nouns[iWord]:
          dict_synsets_nouns[iWord].append(synMax);
        if synsets_noun[0] not in dict_synsets_nouns[iWord]:
          dict_synsets_nouns[iWord].append(synsets_noun[0]);

      # if len(synsetsSD) >= 1:
      #   synsetRoot = synsetsSD[0];
      #   print "synsetroot"
      #   print synsetRoot
      #
      #   for noun in dict_words_nouns[iWord]:
      #     synsets_noun = wn.synsets(noun, pos = 'n');
      #     if len(synsets_noun) <= 0:
      #       continue;
      #
      #     p_noun_max = 0;
      #     synMax = synsets_noun[0];
      #
      #     for synset_noun in synsets_noun:
      #       p = synsetRoot.path_similarity(synset_noun);
      #       if p > p_noun_max:
      #         p_noun_max = p;
      #         synMax = synset_noun;
      #
      #     if synMax not in dict_synsets_nouns[iWord]:
      #       dict_synsets_nouns[iWord].append(synMax);
      #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
      #       dict_synsets_nouns[iWord].append(synsets_noun[0]);

      # if len(synsetsSD) >= 3:
      #   synsetRoot = synsetsSD[2];
      #   print "synsetroot"
      #   print synsetRoot
      #
      #   for noun in dict_words_nouns[iWord]:
      #     synsets_noun = wn.synsets(noun, pos = 'n');
      #     if len(synsets_noun) <= 0:
      #       continue;
      #
      #     p_noun_max = 0;
      #     synMax = synsets_noun[0];
      #
      #     for synset_noun in synsets_noun:
      #       p = synsetRoot.path_similarity(synset_noun);
      #       if p > p_noun_max:
      #         p_noun_max = p;
      #         synMax = synset_noun;
      #
      #     if synMax not in dict_synsets_nouns[iWord]:
      #       dict_synsets_nouns[iWord].append(synMax);
      #     if synsets_noun[0] not in dict_synsets_nouns[iWord]:
      #       dict_synsets_nouns[iWord].append(synsets_noun[0]);


      tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(wordDict["x1"]));
      nouns = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBN' or pos == 'VBD')];
      print "VVVVV"
      print nouns
      for noun in nouns:
        noun = wn.morphy(noun);
        if noun == None:
          continue

        if noun != wordDict["en"] and noun != "sth" and noun not in dict_words_nouns[iWord]:
          # print noun;
          dict_words_nouns[iWord].append(noun);

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      print wordDict["tv"]
      print dict_words_nouns[iWord]

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      # synsets

      iSDMax = 0;
      pSD_max = 0;

      for iSyn in range(len(synsetsSD)-1):
        synsetSD = synsetsSD[iSyn];
        pSD = 0;

        arr_p = [];

        for synset in wn_words:
          p_noun_max = 0;
          p = synsetSD.path_similarity(synset);
            # arr_p.append(p);
          # print "-----------------------"
          # print synsetSD
          # print synset
          # print p
          if p > p_noun_max:
            p_noun_max = p;

          arr_p.append(p_noun_max);

        arr_p = sorted(arr_p, reverse=True);

        for i in xrange(0, len(arr_p)-1):
          if i <= 1:
            pSD += arr_p[i];

        # print "\n"

        if pSD > pSD_max:
          # print pSD
          # print pSD_max
          pSD_max = pSD;
          # print iSyn
          # print iSDMax
          iSDMax = iSyn;

      # print "\n"

      synsetRoot = synsetsSD[iSDMax];
      print "synsetroot"
      print synsetRoot

      for noun in dict_words_nouns[iWord]:
        synsets_noun = wn.synsets(noun, pos = 'v');
        if len(synsets_noun) <= 0:
          continue;

        p_noun_max = 0;
        synMax = synsets_noun[0];

        for synset_noun in synsets_noun:
          p = synsetRoot.path_similarity(synset_noun);
          if p > p_noun_max:
            p_noun_max = p;
            synMax = synset_noun;

        if synMax not in dict_synsets_nouns[iWord]:
          print synMax
          dict_synsets_nouns[iWord].append(synMax);
        if synsets_noun[0] not in dict_synsets_nouns[iWord]:
          dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_nouns[iWord]



  ########################################
  return dict_synsets_nouns;
  ########################################

