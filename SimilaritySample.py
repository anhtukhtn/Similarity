__author__ = 'tu'

from nltk.corpus import wordnet as wn
import nltk
import OxfordParser
import DictProcess
import WordnetProcess
import FileProcess
from nltk.stem import WordNetLemmatizer
from nltk.metrics import jaccard_distance
import ManualData
import POSWrapper

wordnet_lemmatizer = WordNetLemmatizer()


def get_nbest_synsets_n_v_with_word(dict_words,word_concept):

  dict_words_nouns = [];
  dict_synsets_nouns = [];

  wn_words = wn.synsets(word_concept, pos = 'n');

  if word_concept == 'bedroom':
    asdf = 0;

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_nouns.append([]);

    wordDict = dict_words[str(iWord)];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    if not wordDict.has_key('tv'):
      continue

    if not wordDict.has_key('d'):
      continue

    nouns = [];
    if wordDict.has_key("sd"):
      tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["sd"]));
      nouns = [word for word,pos in tagged_sent if ((pos == 'NN' or pos == 'NNS') and (word != 'sth' and word != 'etc'))];

      if len(nouns) == 0:
        tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
        print tagged_sent
        nouns = [word for word,pos in tagged_sent if ((pos == 'NN' or pos == 'NNS') and (word != 'sth' and word != 'etc'))];

    elif wordDict.has_key("d") and wordDict["d"] != None:
      tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
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

    tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    if wordDict.has_key('xh0') and wordDict['xh0'] is not None and wordDict['xh0'] != 'nn':
      nouns.append(wordDict['xh0']);
    # if wordDict.has_key('xh1') and wordDict['xh1'] is not None:
    #   nouns.append(wordDict['xh1']);
    # if wordDict.has_key('xh2') and wordDict['xh2'] is not None:
    #   nouns.append(wordDict['xh2']);

    # print  tagged_sent

    for noun in nouns:
      noun = wordnet_lemmatizer.lemmatize(noun, pos='n');
      if noun == None:
        continue

      if noun.encode('utf8') != word_concept and noun != "sth" and noun not in dict_words_nouns[iWord]:
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

    for iSyn in range(len(synsetsSD)):
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
        if i <= 0:
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
        # dict_synsets_nouns[iWord].append(synMax);
        for synset in wn_words:
          p = synset.path_similarity(synset_noun);
        # p = synsetRoot.path_similarity(synset_noun);
          if p > p_noun_max:
            p_noun_max = p;
            synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synMax);

      # if synsets_noun[0] not in dict_synsets_nouns[iWord]:
      #   dict_synsets_nouns[iWord].append(synsets_noun[0]);

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


    # continue
    tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBN' or pos == 'VBD')];

    print "VVVVV"
    print nouns
    for noun in nouns:
      noun = wordnet_lemmatizer.lemmatize(noun, pos='v');
      if noun == None:
        continue

      if noun.encode('utf8') != word_concept and noun != "sth" and noun not in dict_words_nouns[iWord]:
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

    for iSyn in range(len(synsetsSD)):
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
        dict_synsets_nouns[iWord].append(synMax);
      # if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        # dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_nouns[iWord]

  ########################################
  return dict_synsets_nouns;
  ########################################

####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword_average(WORD, dict_words):


  if WORD == "bank":
    asf = 0;
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data
  dict_words_synsets = get_nbest_synsets_n_v_with_word(dict_words,WORD);
  # print "dict-word_synsets"
  # print dict_words_synsets

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print "wn_words -------"
  print wn_words;

  wn_words_synsets = WordnetProcess.get_synsets_n_v(WORD, wn_words);

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
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          p_max = dict_synset.path_similarity(wn_synset);
          if p_max == None:
            continue

          arr_p.append(p_max);

          # print p_max

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        count = 0.0001;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 5;
      for i in range(len(arr_p_word)):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*5.;
            elif i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
          else:
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*5.;
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

  wn_words = dict_words;
  wn_words_synsets = get_nbest_synsets_n_v_with_word(wn_words,WORD);

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

        nBest = 8;
        count = 0.0001
        for i in range(len(arr_p)):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count +=1

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
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

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  dict_words = wn_words;
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
  # @brief:
  #

  matrix_similarity_jaccard = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  for iWnWord in range(len(wn_words)):

    tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wn.synset(wn_words[iWnWord].name()).definition()));
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

      tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(dict_words[str(iDictWord)]["d"]));
      words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

      # words = nltk.wordpunct_tokenize(dict_words[str(iDictWord)]["d"]);
      # print words
      for i in range(len(words)):
        words[i] = wordnet_lemmatizer.lemmatize(words[i]);
      dict_set = set(words);
      # print
      # dict_set = set(dict_words[str(iDictWord)]["d"].encode('utf8').split());
      matrix_similarity_jaccard[iWnWord][iDictWord] = jaccard_distance(wn_set,dict_set);


  for iWnWord in range(len(wn_words)):
    for iDictWord in range(len(dict_words)):
      matrix_similarity[iWnWord][iDictWord] = matrix_similarity[iWnWord][iDictWord]*10 + 2*(1-matrix_similarity_jaccard[iWnWord][iDictWord]);
      matrix_similarity[iWnWord][iDictWord] /= 12;

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
    if not dict_words[str(i)].has_key('tv'):
      dict_words[str(i)]['tv'] = "--";
    if dict_words[str(i)]['tv'] == None:
      dict_words[str(i)]['tv'] = "--"
    arrRowDict.append(dict_words[str(i)]["tv"].encode('utf8'));

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_average.csv",arrRowDict,matrix_similarity)
  ####################################################################################################

####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword(WORD, dict_words):

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data
  dict_words_synsets = get_nbest_synsets_n_v_with_word(dict_words,WORD);
  print "dict-word_synsets"
  print dict_words_synsets

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print "wn_words -------"
  print wn_words;

  wn_words_synsets = WordnetProcess.get_synsets_n_v(WORD, wn_words);

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
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          p_max = dict_synset.path_similarity(wn_synset);
          if p_max == None:
            continue

          arr_p.append(p_max);

          # print p_max

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
  # write file

  # - - - - - - - - - - - - - - - - - - - - - - - - -
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
    if not dict_words[str(i)].has_key('tv'):
      dict_words[str(i)]['tv'] = "--";
    if dict_words[str(i)]['tv'] == None:
      dict_words[str(i)]['tv'] = "--"
    arrRowDict.append(dict_words[str(i)]["tv"].encode('utf8'));

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword.csv",arrRowDict,matrix_similarity)
  ####################################################################################################


def get_nbest_synsets_n_v_with_word_vn(dict_words,word_concept):

  dict_words_nouns = [];
  dict_synsets_nouns = [];

  wn_words = wn.synsets(word_concept, pos = 'n');

  if word_concept == 'bedroom':
    asdf = 0;

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_nouns.append([]);

    wordDict = dict_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #
    # sd

    if not wordDict.has_key('tv'):
      continue

    if not wordDict.has_key('d'):
      continue

    nouns = [];
    if wordDict.has_key("sd"):
      tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["sd"]));
      nouns = [word for word,pos in tagged_sent if ((pos == 'NN' or pos == 'NNS') and (word != 'sth' and word != 'etc'))];

      if len(nouns) == 0:
        tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
        print tagged_sent
        nouns = [word for word,pos in tagged_sent if ((pos == 'NN' or pos == 'NNS') and (word != 'sth' and word != 'etc'))];

    elif wordDict.has_key("d") and wordDict["d"] != None:
      tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
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

    tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    if wordDict.has_key('xh0') and wordDict['xh0'] is not None and wordDict['xh0'] != 'nn':
      nouns.append(wordDict['xh0']);
    # if wordDict.has_key('xh1') and wordDict['xh1'] is not None:
    #   nouns.append(wordDict['xh1']);
    # if wordDict.has_key('xh2') and wordDict['xh2'] is not None:
    #   nouns.append(wordDict['xh2']);

    # print  tagged_sent

    for noun in nouns:
      noun = wordnet_lemmatizer.lemmatize(noun, pos='n');
      if noun == None:
        continue

      if noun.encode('utf8') != word_concept and noun != "sth" and noun not in dict_words_nouns[iWord]:
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

    for iSyn in range(len(synsetsSD)):
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
        if i <= 0:
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
        # dict_synsets_nouns[iWord].append(synMax);
        for synset in wn_words:
          p = synset.path_similarity(synset_noun);
        # p = synsetRoot.path_similarity(synset_noun);
          if p > p_noun_max:
            p_noun_max = p;
            synMax = synset_noun;

      if synMax not in dict_synsets_nouns[iWord]:
        dict_synsets_nouns[iWord].append(synMax);

      # if synsets_noun[0] not in dict_synsets_nouns[iWord]:
      #   dict_synsets_nouns[iWord].append(synsets_noun[0]);

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


    # continue
    tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wordDict["d"]));
    nouns = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBN' or pos == 'VBD')];

    print "VVVVV"
    print nouns
    for noun in nouns:
      noun = wordnet_lemmatizer.lemmatize(noun, pos='v');
      if noun == None:
        continue

      if noun.encode('utf8') != word_concept and noun != "sth" and noun not in dict_words_nouns[iWord]:
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

    for iSyn in range(len(synsetsSD)):
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
        dict_synsets_nouns[iWord].append(synMax);
      # if synsets_noun[0] not in dict_synsets_nouns[iWord]:
        # dict_synsets_nouns[iWord].append(synsets_noun[0]);

    print "dict_synsets_nouns"
    print dict_synsets_nouns[iWord]

  ########################################
  return dict_synsets_nouns;
  ########################################


####################################################################################################
#
# @brief:   calculate similarity by synsets
#
def similarity_by_synsets_synsets_nbest_withword_average_VN(WORD, dict_words):


  if WORD == "bank":
    asf = 0;
  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # dictionary data
  dict_words_synsets = get_nbest_synsets_n_v_with_word(dict_words,WORD);
  # print "dict-word_synsets"
  # print dict_words_synsets

  # - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  # wordnet data

  wn_words = wn.synsets(WORD, pos = 'n');
  print "wn_words -------"
  print wn_words;

  wn_words_synsets = WordnetProcess.get_synsets_n_v(WORD, wn_words);

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
      #
      for dict_synset in dict_words_synsets[iDictWord]:

        # print "------------ dict noun"
        # print dictNoun;
        p_dictNoun_wnNouns = 0;

        # for some nouns don't have synsets

        arr_p  = [];

        # - - - - - - - - - - - - - - - - - - - - - - - -

        for wn_synset in wn_words_synsets[iWnWord]:
          #
          p_max = dict_synset.path_similarity(wn_synset);
          if p_max == None:
            continue

          arr_p.append(p_max);

          # print p_max

        arr_p = sorted(arr_p, reverse=True);

        nBest = 8;
        count = 0.0001;
        for i in xrange(0, len(arr_p)-1):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count += 1;

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
      count = 5;
      for i in range(len(arr_p_word)):
        if i < nBest:
          if nBest > len(arr_p_word):
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*5.;
            elif i< nBest/3:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
            else:
              p_iWnWord_iDictWord += arr_p_word[i]*1;
          else:
            if i == 0:
              p_iWnWord_iDictWord += arr_p_word[i]*5.;
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

  wn_words = dict_words;
  wn_words_synsets = get_nbest_synsets_n_v_with_word(wn_words,WORD);

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

        nBest = 8;
        count = 0.0001
        for i in range(len(arr_p)):
          if i < nBest:
            p_dictNoun_wnNouns += arr_p[i];
            count +=1

        p_dictNoun_wnNouns = p_dictNoun_wnNouns/count;
        arr_p_word.append(p_dictNoun_wnNouns);

      arr_p_word = sorted(arr_p_word, reverse=True);
      nBest = 10;
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

    # word-word
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

  dict_words = wn_words;
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
  # @brief:
  #

  matrix_similarity_jaccard = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  for iWnWord in range(len(wn_words)):

    tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(wn.synset(wn_words[iWnWord].name()).definition()));
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

      tagged_sent = POSWrapper.pos_tag(nltk.wordpunct_tokenize(dict_words[str(iDictWord)]["d"]));
      words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

      # words = nltk.wordpunct_tokenize(dict_words[str(iDictWord)]["d"]);
      # print words
      for i in range(len(words)):
        words[i] = wordnet_lemmatizer.lemmatize(words[i]);
      dict_set = set(words);
      # print
      # dict_set = set(dict_words[str(iDictWord)]["d"].encode('utf8').split());
      matrix_similarity_jaccard[iWnWord][iDictWord] = jaccard_distance(wn_set,dict_set);


  for iWnWord in range(len(wn_words)):
    for iDictWord in range(len(dict_words)):
      matrix_similarity[iWnWord][iDictWord] = matrix_similarity[iWnWord][iDictWord]*10 + 2*(1-matrix_similarity_jaccard[iWnWord][iDictWord]);
      matrix_similarity[iWnWord][iDictWord] /= 12;

 ####################################################################################################
  #
  # @brief: vn
  #

  wn_words = ManualData.DATA_VN_BANK();

  matrix_similarity_jaccard = [[0 for x in range(len(dict_words))] for x in range(len(wn_words))];

  for iWnWord in range(len(wn_words)):

    words = (wn_words[iWnWord]["tv"].replace(',', ' ')).split();
    # words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

    # words = nltk.wordpunct_tokenize(wn.synset(wn_words[iWnWord].name()).definition());
    # print words
    for i in range(len(words)):
      words[i] = words[i];

    wn_set = set(words);
    # wn_set = set(wn.synset(wn_words[iWnWord].name()).definition().split())
    # print wn_set

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # word-word
    for iDictWord in range(len(dict_words)):

      if not dict_words[str(iDictWord)].has_key("tv") or dict_words[str(iDictWord)]["tv"] == None:
        matrix_similarity_jaccard[iWnWord][iDictWord] = 1;
        continue

      words = (dict_words[str(iDictWord)]["tv"].replace(',', ' ')).split();
      # words = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS' or pos == 'JJ' or pos == '' or pos == 'VB' or pos == 'VBN' or pos == 'VBD' or pos == 'RB')];

      # words = nltk.wordpunct_tokenize(dict_words[str(iDictWord)]["d"]);
      # print words
      for i in range(len(words)):
        words[i] = words[i].encode('utf8');
      dict_set = set(words);
      # print
      # dict_set = set(dict_words[str(iDictWord)]["d"].encode('utf8').split());
      matrix_similarity_jaccard[iWnWord][iDictWord] = jaccard_distance(wn_set,dict_set);

  print "----------------------------------------------------"
  s = [[str(e) for e in row] for row in matrix_similarity_jaccard]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print '\n'.join(table)


  for iWnWord in range(len(wn_words)):
    for iDictWord in range(len(dict_words)):
      matrix_similarity[iWnWord][iDictWord] = matrix_similarity[iWnWord][iDictWord]*1 + 1*(1-matrix_similarity_jaccard[iWnWord][iDictWord]);
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
    matrix_similarity[i].insert(0,wn_words[i]["tv"]);

  # - - - - - - - - - - - - - - - - - - - - - - - - -
  # row
  arrRowDict = [];
  arrRowDict.append("--");
  for i in range(len(dict_words)):
    if not dict_words[str(i)].has_key('tv'):
      dict_words[str(i)]['tv'] = "--";
    if dict_words[str(i)]['tv'] == None:
      dict_words[str(i)]['tv'] = "--"
    arrRowDict.append(dict_words[str(i)]["tv"].encode('utf8'));

  FileProcess.write_to_excel_file("Results/"+WORD+"_synsets_synsets_nbest_withword_average_vn.csv",arrRowDict,matrix_similarity)
  ####################################################################################################



dictOxford = OxfordParser.readOxfordNouns();
print dictOxford



def similarityWordB():

  for word in dictOxford:
    print word
    print dictOxford[word]
    if word == 'bank':
      similarity_by_synsets_synsets_nbest_withword_average(word,dictOxford[word]);

  ########################################

  ########################################

similarityWordB();

