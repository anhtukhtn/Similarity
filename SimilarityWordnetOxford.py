__author__ = 'tu'

import OxfordParser

import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
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

  for iWord in range(len(wn_synsets_for_word_origin)):

    print "- - - - - - - - - - - - - - - - - - - - - - - - - - -";
    print iWord;
    wn_synsets_for_words.append([]);
    # get a bank in wn_words
    wordDict = wn_synsets_for_word_origin[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get synsets of bank
    synset_of_word = wn.synset(wordDict.name());
    wn_synsets_for_words[iWord].append(synset_of_word);
    print synset_of_word
    print "---"

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hypernyms

    if PARAMETERS.DICT_WN_FEATURE_RELATION_hypernyms == 1:
      print "hypernyms"
      for hypernym in wn.synset(wordDict.name()).hypernyms():
        print hypernym
        wn_synsets_for_words[iWord].append(hypernym);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get meronyms
    if PARAMETERS.DICT_WN_FEATURE_RELATION_part_meronyms == 1:
      print "meronyms"
      for meronym in wn.synset(wordDict.name()).part_meronyms():
        print meronym
        wn_synsets_for_words[iWord].append(meronym);

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # get holonyms
    if PARAMETERS.DICT_WN_FEATURE_RELATION_member_holonyms == 1:
      print "holonyms"
      for holonym in wn.synset(wordDict.name()).member_holonyms():
        print holonym
        wn_synsets_for_words[iWord].append(holonym);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hyponyms
    if PARAMETERS.DICT_WN_FEATURE_RELATION_hyponyms == 1:
      print "hyponyms"
      for hyponym in wn.synset(wordDict.name()).hyponyms():
        print hyponym
        wn_synsets_for_words[iWord].append(hyponym);

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
            # if synsetsDictNoun[0] not in wn_words_synset[iWord]:
            #   wn_words_synset[iWord].append(synsetsDictNoun[0]);

  ########################################
  return wn_synsets_for_words
  ########################################


# wn_words = wn.synsets("bank", pos = 'n');

# wn_synsets_for_words = get_synsets_for_word("bank", wn_words);

# print wn_synsets_for_words


def get_nbest_synsets_for_word_in_oxford(dict_words,word_concept):

  dict_words_nouns = [];
  dict_words_verbs = [];
  dict_synsets_for_words = [];

  wn_words = wn.synsets(word_concept, pos = 'n');

  for iWord in range(len(dict_words)):

    print iWord;

    dict_words_nouns.append([]);
    dict_synsets_for_words.append([]);

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
      print wordDict["tv"]
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


# dictOxfordNouns = OxfordParser.readOxfordNouns();
# get_nbest_synsets_for_word_in_oxford(dictOxfordNouns['bank'],'bank')
