__author__ = 'tu'

import OxfordParser

import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import FileProcess
import heapq
import CompareVietNetOxford
import CompareWithGold

import copy

from nltk.metrics import jaccard_distance
wordnet_lemmatizer = WordNetLemmatizer()

from Parameters import PARAMETERS

####################################################################################################
#
# @brief    get synsets of a word in Wordnet by hyponym, definition, ..
#
# @param    word_origin
#           word will be detected. E.g. 'bank', ..
#
# @param    wn_words
#           wn.synsets(word_origin)
#
# @return   list of synsets for each synset of word_origin
#
def get_synsets_for_word_in_wn(word_origin, wn_synsets_for_word_origin):

  # arr synsets for arr words
  # each word has an array of synsets
  wn_synsets_for_words = [];

  # add p
  p_synsets_for_words = [];

  for iWord in range(len(wn_synsets_for_word_origin)):

    print "- - - - - - - - - - - - - - - - - - - - - - - - - - -";
    print iWord;
    wn_synsets_for_words.append([]);

    # add p
    p_synsets_for_words.append([]);

    # get a bank in wn_words
    wordDict = wn_synsets_for_word_origin[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get synsets of bank
    synset_of_word = wn.synset(wordDict.name());
    wn_synsets_for_words[iWord].append(synset_of_word);

    # add p
    p_synsets_for_words[iWord].append(1.5);

    print synset_of_word
    print "---"

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hypernyms

    if PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms == 1:
      print "hypernyms"
      for hypernym in wn.synset(wordDict.name()).hypernyms():
        print hypernym
        wn_synsets_for_words[iWord].append(hypernym);

        # add p
        p_synsets_for_words[iWord].append(1.2);


    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get meronyms
    if PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms == 1:
      print "meronyms"
      for meronym in wn.synset(wordDict.name()).part_meronyms():
        print meronym
        wn_synsets_for_words[iWord].append(meronym);

        # add p
        p_synsets_for_words[iWord].append(1.2);

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # get holonyms
    if PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms == 1:
      print "holonyms"
      for holonym in wn.synset(wordDict.name()).member_holonyms():
        print holonym
        wn_synsets_for_words[iWord].append(holonym);

        # add p
        p_synsets_for_words[iWord].append(1.2);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hyponyms
    if PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms == 1:
      print "hyponyms"
      for hyponym in wn.synset(wordDict.name()).hyponyms():
        print hyponym
        wn_synsets_for_words[iWord].append(hyponym);

        # add p
        p_synsets_for_words[iWord].append(1.2);

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # get description

    if PARAMETERS.DICT_WN_FEATURE_RELATION_definition == 1:

      print "\ndefinition ------";

      tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wn.synset(wordDict.name()).definition()));
      print tagged_sent

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      if PARAMETERS.POS_FEATURE_n == 1:
        nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS'  or pos == 'JJ')];

        for noun in nouns:

          noun = wordnet_lemmatizer.lemmatize(noun, pos='n');

          if noun == None:
            continue

          if noun != word_origin and noun != "sth":
            synsetsDictNoun = wn.synsets(noun, pos = "n");

            if len(synsetsDictNoun) > 0:
              synsetMax = synsetsDictNoun[0];
              p_max = 0;

              for synsetNoun in synsetsDictNoun:
                p = synsetNoun.path_similarity(synset_of_word);
                if p > p_max:
                  p_max = p;
                  synsetMax = synsetNoun

              print synsetMax
              if synsetMax not in wn_synsets_for_words[iWord]:
                wn_synsets_for_words[iWord].append(synsetMax);

                # add p
                p_synsets_for_words[iWord].append(1.);

            # if synsetsDictNoun[0] not in wn_words_synset[iWord]:
            #   # wn_words_synset[iWord].append(synsetsDictNoun[0]);
      # - - - - - - - - - - - - - - - - - - - - - - - - - - -

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      if PARAMETERS.POS_FEATURE_v == 1:
        verbs = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBD' or pos == 'VBN')];

        for verb in verbs:

          verb = wordnet_lemmatizer.lemmatize(verb, pos='v');

          if verb == None:
            continue

          if verb != "bank":
            synsetsDictVerb = wn.synsets(verb, pos = "v");


            if len(synsetsDictVerb) > 0:
              synsetMax = synsetsDictVerb[0];
              p_max = 0;

              for synsetVerb in synsetsDictVerb:
                p = synsetVerb.path_similarity(synset_of_word);
                if p > p_max:
                  p_max = p;
                  synsetMax = synsetVerb
              #
              print synsetMax
              if synsetMax not in wn_synsets_for_words[iWord]:
                wn_synsets_for_words[iWord].append(synsetMax);

                # add p
                p_synsets_for_words[iWord].append(1.);

            # if synsetsDictNoun[0] not in wn_words_synset[iWord]:
            #   wn_words_synset[iWord].append(synsetsDictNoun[0]);

    print wn_synsets_for_words[iWord]

  ########################################
  return wn_synsets_for_words,p_synsets_for_words;
  ########################################


# wn_words = wn.synsets("bank", pos = 'n');

# wn_synsets_for_words = get_synsets_for_word("bank", wn_words);

# print wn_synsets_for_words


def get_nbest_synsets_for_word_in_oxford(dict_words,word_concept):

  dict_words_nouns = [];
  dict_words_verbs = [];
  dict_synsets_for_words = [];

  wn_words = wn.synsets(word_concept, pos = 'n');

  # add p
  p_synsets_for_words = [];

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_for_words.append([]);

    # add p
    p_synsets_for_words.append([]);

    wordDict = dict_words[str(iWord)];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    if not wordDict.has_key('tv'):
      continue

    if not wordDict.has_key('d'):
      continue

    nouns = [];
    if wordDict.has_key("sd") and PARAMETERS.DICT_OX_FEATURE_RELATION_sd == 1:
      tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wordDict["sd"]));
      nouns = [word for word,pos in tagged_sent if ((pos == 'NN' or pos == 'NNS') and (word != 'sth' and word != 'etc'))];

      if len(nouns) == 0:
        tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
        print tagged_sent
        nouns = [word for word,pos in tagged_sent if ((pos == 'NN' or pos == 'NNS') and (word != 'sth' and word != 'etc'))];

    elif wordDict.has_key("d") and wordDict["d"] != None:
      tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
      print tagged_sent
      nouns = [word for word,pos in tagged_sent if ((pos == 'NN' or pos == 'NNS') and (word != 'sth' or word != 'etc'))];
    else:
      continue

    for noun in nouns:
      noun = wordnet_lemmatizer.lemmatize(noun, pos='n');
      if noun == None:
        continue

      if noun != "sth" and noun != 'etc' and noun not in dict_words_nouns[iWord]:
        dict_words_nouns[iWord].append(noun);

    if len(dict_words_nouns[iWord]) == 0:
      continue

    print dict_words_nouns[iWord]
    synsetsSD = [];

    for word in dict_words_nouns[iWord]:
      synsets = wn.synsets(word, pos = 'n');
      for synset in synsets:
        synsetsSD.append(synset)

    if len(synsetsSD) == 0:
      continue

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # d

    if PARAMETERS.DICT_OX_FEATURE_RELATION_d == 1:
      tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
      nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    if PARAMETERS.DICT_OX_FEATURE_RELATION_xh == 1:
      if wordDict.has_key('xh0') and wordDict['xh0'] is not None and wordDict['xh0'] != 'nn':
        nouns.append(wordDict['xh0']);
      if wordDict.has_key('xh1') and wordDict['xh1'] is not None:
        nouns.append(wordDict['xh1']);
      if wordDict.has_key('xh2') and wordDict['xh2'] is not None:
        nouns.append(wordDict['xh2']);

    # print  tagged_sent

    for noun in nouns:
      noun = wordnet_lemmatizer.lemmatize(noun, pos='n');
      if noun == None:
        continue

      if noun.encode('utf8') != word_concept and noun != "sth" and noun not in dict_words_nouns[iWord]:
        dict_words_nouns[iWord].append(noun);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print wordDict["tv"]
    print dict_words_nouns[iWord]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # synsets

    iSDMax = 0;
    pSD_max = 0;

    for iSyn in range(len(synsetsSD)):
      synsetSD = synsetsSD[iSyn];
      pSD = 0;

      arr_p = [];

      for synset in wn_words:
        # p_noun_max = 0;
        p = synsetSD.path_similarity(synset);
        # print "-----------------------"
        # if p > p_noun_max:
        p_noun_max = p;

        arr_p.append(p_noun_max);

      arr_p = sorted(arr_p, reverse=True);

      for i in xrange(0, len(arr_p)-1):
        if i <= 0:
          pSD += arr_p[i];

      # print "\n"

      if pSD > pSD_max:
        pSD_max = pSD;
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
        # dict_synsets_nouns[iWord].append(synMax);
        for synset in wn_words:
          p = synset.path_similarity(synset_noun);
        # p = synsetRoot.path_similarity(synset_noun);
          if p > p_noun_max:
            p_noun_max = p;
            synMax = synset_noun;

      if synMax not in dict_synsets_for_words[iWord]:
        dict_synsets_for_words[iWord].append(synMax);

    if PARAMETERS.POS_FEATURE_v:

      dict_words_verbs.append([]);
      # continue
      tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
      verbs = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBN' or pos == 'VBD')];

      print "VVVVV"
      print verbs
      for verb in verbs:
        verb = wordnet_lemmatizer.lemmatize(verb, pos='v');
        if verb == None:
          continue

        if verb.encode('utf8') != word_concept and verb != "sth" and verb not in dict_words_verbs[iWord]:
          # print noun;
          dict_words_verbs[iWord].append(verb);

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      print dict_words_verbs[iWord]

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      #
      # synsets

      iSDMax = 0;
      pSD_max = 0;

      for iSyn in range(len(synsetsSD)):
        synsetSD = synsetsSD[iSyn];
        pSD = 0;

        arr_p = [];

        for synset in wn_words:
          # p_noun_max = 0;
          p = synsetSD.path_similarity(synset);
            # arr_p.append(p);
          # print "-----------------------"
          # print synsetSD
          # print synset
          # print p
          # if p > p_noun_max:
          p_verb_max = p;

          arr_p.append(p_verb_max);

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

      for verb in dict_words_verbs[iWord]:
        synsets_verb = wn.synsets(verb, pos = 'v');
        if len(synsets_verb) <= 0:
          continue;

        p_verb_max = 0;
        synMax = synsets_verb[0];

        for synset_verb in synsets_verb:
          # p = synsetRoot.path_similarity(synset_verb);
          for synset in wn_words:
            p = synset.path_similarity(synset_verb);

            if p > p_verb_max:
              p_verb_max = p;
              synMax = synset_verb;

        if synMax not in dict_synsets_for_words[iWord]:
          dict_synsets_for_words[iWord].append(synMax);
        # if synsets_noun[0] not in dict_synsets_nouns[iWord]:
          # dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_for_words[iWord]

  ########################################
  return dict_synsets_for_words;
  ########################################

def choose_pair(matrix_similarity, wn_words, dict_words):
  if len(wn_words) == 1 and len(dict_words) == 1:
    matrix_similarity[0][0] += matrix_similarity[0][0] + 100;

  if len(wn_words) == 1 and len(dict_words) > 1:

    order = heapq.nlargest(2, range(len(matrix_similarity[0])), matrix_similarity[0].__getitem__);

    if matrix_similarity[0][order[0]] >= 1.1*matrix_similarity[0][order[1]]:
      matrix_similarity[0][order[0]] += 100;

  if len(wn_words) > 1 and len(dict_words) > 1:
    for iWnWord in range(len(wn_words)):
      order = heapq.nlargest(2, range(len(matrix_similarity[iWnWord])), matrix_similarity[iWnWord].__getitem__);

      if matrix_similarity[iWnWord][order[0]] >= 1.1*matrix_similarity[iWnWord][order[1]]:
        matrix_similarity[iWnWord][order[0]] += 100;


def choose_pair_0_1(matrix_similarity, wn_words, dict_words):
  if len(wn_words) == 1 and len(dict_words) == 1:
    matrix_similarity[0][0] = 1;

  if len(wn_words) == 1 and len(dict_words) > 1:

    order = heapq.nlargest(2, range(len(matrix_similarity[0])), matrix_similarity[0].__getitem__);

    if matrix_similarity[0][order[0]] >= 1.1*matrix_similarity[0][order[1]]:
      matrix_similarity[0][order[0]] = 1;

  if len(wn_words) > 1 and len(dict_words) > 1:
    for iWnWord in range(len(wn_words)):
      order = heapq.nlargest(2, range(len(matrix_similarity[iWnWord])), matrix_similarity[iWnWord].__getitem__);

      if matrix_similarity[iWnWord][order[0]] >= 1.1*matrix_similarity[iWnWord][order[1]]:
        matrix_similarity[iWnWord][order[0]] = 1;

# dictOxfordNouns = OxfordParser.readOxfordNouns();
# get_nbest_synsets_for_word_in_oxford(dictOxfordNouns['bank'],'bank')

def similarity_by_synsets_synsets_nbest_withword_dict_wn(WORD, dict_words, wn_words):
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data
  dict_words_synsets = get_nbest_synsets_for_word_in_oxford(dict_words,WORD);

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data


  if len(wn_words) == 0:
    return ;

  print "wn_words -------"
  print wn_words;

  (wn_words_synsets,p_wn_words_synsets) = get_synsets_for_word_in_wn(WORD, wn_words);

  print wn_words_synsets

  # matrix for similarity dict_words vs wn_words
  matrix_similarity = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  ####################################################################################################
  #
  # calculate 2d matrix of p

  for iWnWord in range(len(wn_words)):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      p_iWnWord_iDictWord = 0.;

      arr_p_word = [];
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        # for wn_synset in wn_words_synsets[iWnWord]:
        for synsetIndex in range(len(wn_words_synsets[iWnWord])):

          wn_synset = wn_words_synsets[iWnWord][synsetIndex]
          #
          p_max = dict_synset.path_similarity(wn_synset);

          # p_max = p_max*p_wn_words_synsets[iWnWord][synsetIndex]

          print p_wn_words_synsets[iWnWord][synsetIndex]

          if p_max == None:
            continue

          arr_p.append(p_max);

          # print p_max
        print "\n"

        arr_p = sorted(arr_p, reverse=True);

        nBest = PARAMETERS.N_BEST_CALCULATE_SIMILARITY;
        count = 0.0001;

        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = PARAMETERS.N_BEST_CALCULATE_SIMILARITY;
      count = 0;
      for i in range(len(arr_p_word)):
        if i < nBest:
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

  ########################################
  return matrix_similarity


def similarity_by_synsets_synsets_nbest_withword_wn_dict(WORD, dict_words, wn_words):

  wn_words_synsets = get_nbest_synsets_for_word_in_oxford(wn_words,WORD);

  # print wn_words;
  (dict_words_synsets,p_dict_words_synsets) = get_synsets_for_word_in_wn(WORD, dict_words);

  print "sysnets -----------------------.----.-----.--.-"

  # matrix for similarity dict_words vs wn_words
  matrix_similarity_reverse = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

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

        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets
        countwnNouns = 0.00000001;

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:

          p_max = dict_synset.path_similarity(wn_synset);
          if p_max != None:
            arr_p.append(p_max);

          # print p_max
          # - - - - - - - - - - - - - - - - - - - - - - - -

        arr_p = sorted(arr_p, reverse=True);

        nBest = PARAMETERS.N_BEST_CALCULATE_SIMILARITY;
        count = 0.0001
        for i in range(len(arr_p)):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count +=1

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = PARAMETERS.N_BEST_CALCULATE_SIMILARITY;
      count = 5;
      for i in xrange(0, len(arr_p_word)-1):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*5;
            elif i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1.;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
          else:
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*5.;
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

  ########################################
  return matrix_similarity_reverse

def similarity_by_jaccard(WORD, dict_words, wn_words):

  matrix_similarity_jaccard = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  for iWnWord in range(len(wn_words)):

    tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wn.synset(wn_words[iWnWord].name()).definition()));
    words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

    # words = nltk.wordpunct_tokenize(wn.synset(wn_words[iWnWord].name()).definition());
    # print words
    for i in range(len(words)):
      words[i] = wordnet_lemmatizer.lemmatize(words[i]);
    wn_set = set(words);
    # wn_set = set(wn.synset(wn_words[iWnWord].name()).definition().split())
    # print wn_set

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      if not dict_words[str(iDictWord)].has_key("d") or dict_words[str(iDictWord)]["d"] == None:
        matrix_similarity_jaccard[iWnWord][iDictWord] = 1;
        continue

      tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(dict_words[str(iDictWord)]["d"]));
      words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

      # words = nltk.wordpunct_tokenize(dict_words[str(iDictWord)]["d"]);
      # print words
      for i in range(len(words)):
        words[i] = wordnet_lemmatizer.lemmatize(words[i]);
      dict_set = set(words);
      # print
      # dict_set = set(dict_words[str(iDictWord)]["d"].encode('utf8').split());
      matrix_similarity_jaccard[iWnWord][iDictWord] = jaccard_distance(wn_set,dict_set);

  ########################################
  return matrix_similarity_jaccard

####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword_average(WORD, dict_words):

  wn_words = wn.synsets(WORD, pos = 'n');

  matrix_similarity = similarity_by_synsets_synsets_nbest_withword_dict_wn(WORD, dict_words,wn_words)

  matrix_similarity_reverse = similarity_by_synsets_synsets_nbest_withword_wn_dict(WORD , wn_words, dict_words)

  for iWnWord in range(len(wn_words)):
    for iDictWord in range(len(dict_words)):
      matrix_similarity[iWnWord][iDictWord] = matrix_similarity[iWnWord][iDictWord] + matrix_similarity_reverse[iDictWord][iWnWord];
      matrix_similarity[iWnWord][iDictWord] /= 2;


  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)

  ####################################################################################################

  matrix_similarity_jaccard = similarity_by_jaccard(WORD, dict_words, wn_words)

  for iWnWord in range(len(wn_words)):
    for iDictWord in range(len(dict_words)):
      matrix_similarity[iWnWord][iDictWord] = matrix_similarity[iWnWord][iDictWord]*(1-PARAMETERS.JACCARD_WEIGHT) + PARAMETERS.JACCARD_WEIGHT*(1-matrix_similarity_jaccard[iWnWord][iDictWord]);

  choose_pair_0_1(matrix_similarity,wn_words,dict_words);

  formatAndWriteMatrixToFile(copy.deepcopy(matrix_similarity), wn_words, dict_words ,WORD)

  return matrix_similarity;

def formatAndWriteMatrixToFile(matrix_similarity, wn_words, dict_words,WORD):
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
  arrRowDict.append(WORD);
  for i in range(len(dict_words)):
    if not dict_words[str(i)].has_key('tv'):
      dict_words[str(i)]['tv'] = "--";
    if dict_words[str(i)]['tv'] == None:
      dict_words[str(i)]['tv'] = "--"
    arrRowDict.append(dict_words[str(i)]["tv"].encode('utf8'));

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # if dictVietNet.has_key(WORD):
  #   arrVietNet = dictVietNet[WORD];
  #
  #   for iVietNet in arrVietNet:
  #     vietNet = arrVietNet[iVietNet];
  #     for i in range(len(wn_words)):
  #       print "vietnet " + vietNet["tv"]
  #       if SequenceMatcher(None, vietNet["d"], wn.synset(wn_words[i].name()).definition()).ratio() > 0.6:
  #         matrix_similarity[i][0] = vietNet["tv"];
  #         break
  #
  # # - - - - - - - - - - - - - - - - - - - - - - - - - - -



  # FileProcess.write_to_excel_file("Results/parameters/path/"+WORD+"_synsets_synsets_nbest_withword_average.csv",arrRowDict,matrix_similarity)
  FileProcess.append_to_excel_file("Results/parameters/path/"+"synsets_synsets_nbest_withword_average.csv",arrRowDict,matrix_similarity)
  #####################################################################################################

def similarityWords(dictOxfordNouns):

  for word in dictOxfordNouns:
    print word
    print dictOxfordNouns[word]
    if word == 'baby':
      matrix_result = similarity_by_synsets_synsets_nbest_withword_average(word,dictOxfordNouns[word]);
      (precision, recall, accuracy) = CompareWithGold.compareGoldWithResult(matrix_result,word)
      print (precision, recall, accuracy)

dictOxfordNouns = OxfordParser.readOxfordNouns();
similarityWords(dictOxfordNouns)
