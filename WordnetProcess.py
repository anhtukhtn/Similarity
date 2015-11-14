__author__ = 'tu'

import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

####################################################################################################
#
# @brief    get nouns of a word in Wordnet by hyponym, definition, ..
#
# @param    word_origin
#           word will be detected. E.g. 'bank', ..
#
# @param    wn_words
#           wn.synsets(word_origin)
#
# @return   list of nouns for each synset of word_origin
#
def get_nouns(word_origin, wn_words):
  
  wn_words_nouns = [];

  for iWord in range(len(wn_words)):

    print "- - - - - - - - - - - - - - - - - - - - - - - - - - -";
    print iWord;
    wn_words_nouns.append([]);
    # get a bank in wn_words
    wordDict = wn_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get synsets of bank
    print "synsets -------";
    synsets_of_word = wn.synset(wordDict.name());

    for lemma in synsets_of_word.lemmas():

      lemma_name = lemma.name();
      if lemma_name != word_origin:

        print lemma_name;
        wn_words_nouns[iWord].append(lemma_name);

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # get hypernyms
    # print "\nhypernyms ------";
    # for hypernym in wn.synset(wordDict.name()).hypernyms():
    #
    #   for lemma in wn.synset(hypernym.name()).lemmas():
    #     lemma_name = lemma.name();
    #     if lemma_name != "bank":
    #
    #       if not(lemma_name in wn_words_nouns[iWord]):
    #         print lemma_name;
    #         wn_words_nouns[iWord].append(lemma_name);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hyponyms
    print "\nhyponyms ------";
    for hyponym in wn.synset(wordDict.name()).hyponyms():

      for lemma in wn.synset(hyponym.name()).lemmas():
        lemma_name = lemma.name();
        if lemma_name != "bank":

          if not(lemma_name in wn_words_nouns[iWord]):
            print lemma_name;
            wn_words_nouns[iWord].append(lemma_name);
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get description
    print "\ndefinition ------";
    # print wn.synset(bank.name()).definition();

    tagged_sent = nltk.pos_tag(nltk.word_tokenize(wn.synset(wordDict.name()).definition()));
    nouns = [word for word,pos in tagged_sent if pos == 'NN'];

    for noun in nouns:
      if noun != "bank" and noun != "sth" and noun not in wn_words_nouns[iWord]:
        print noun;
        wn_words_nouns[iWord].append(noun);


  ########################################
  return wn_words_nouns
  ########################################


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
def get_synsets(word_origin, wn_words):

  wn_words_synset = [];

  for iWord in range(len(wn_words)):

    print "- - - - - - - - - - - - - - - - - - - - - - - - - - -";
    print iWord;
    wn_words_synset.append([]);
    # get a bank in wn_words
    wordDict = wn_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get synsets of bank
    synset_of_word = wn.synset(wordDict.name());
    wn_words_synset[iWord].append(synset_of_word);
    print synset_of_word
    print "---"

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hypernyms
    # for hypernym in wn.synset(wordDict.name()).hypernyms():
      # print hypernym
      # wn_words_synset[iWord].append(hypernym);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hyponyms
    print "---"
    for hyponym in wn.synset(wordDict.name()).hyponyms():
      print hyponym
      wn_words_synset[iWord].append(hyponym);

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # get description
    print "\ndefinition ------";
    # print wn.synset(bank.name()).definition();

    tagged_sent = nltk.pos_tag(nltk.word_tokenize(wn.synset(wordDict.name()).definition()));
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS')];

    for noun in nouns:

      noun = wordnet_lemmatizer.lemmatize(noun, pos='n');
      if noun == None:
        continue

      # if noun != "bank" and noun != "sth" and noun not in wn_words_synset[iWord]:
      synsetsDictNoun = wn.synsets(noun, pos = "n");


      if len(synsetsDictNoun) > 0:
        synsetMax = synsetsDictNoun[0];
        p_max = 0;

        for synsetNoun in synsetsDictNoun:
          p = synsetNoun.path_similarity(synset_of_word);
          if p > p_max:
            p_max = p;
          # # synsetMax = synsetNoun

        print synsetMax
        if synsetMax not in wn_words_synset[iWord]:
          wn_words_synset[iWord].append(synsetMax);
        # if synsetsDictNoun[0] not in wn_words_synset[iWord]:
          # wn_words_synset[iWord].append(synsetsDictNoun[0]);


  ########################################
  return wn_words_synset
  ########################################


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
def get_synsets_n_v(word_origin, wn_words):

  wn_words_synset = [];

  for iWord in range(len(wn_words)):

    print "- - - - - - - - - - - - - - - - - - - - - - - - - - -";
    print iWord;
    wn_words_synset.append([]);
    # get a bank in wn_words
    wordDict = wn_words[iWord];

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get synsets of bank
    synset_of_word = wn.synset(wordDict.name());
    wn_words_synset[iWord].append(synset_of_word);
    print synset_of_word
    print "---"

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hypernyms
    # for hypernym in wn.synset(wordDict.name()).hypernyms():
      # print hypernym
      # wn_words_synset[iWord].append(hypernym);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hyponyms
    print "---"
    for hyponym in wn.synset(wordDict.name()).part_meronyms():
      print hyponym
      wn_words_synset[iWord].append(hyponym);

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # get hyponyms
    # print "---"
    # for hyponym in wn.synset(wordDict.name()).member_holonyms():
    #   print hyponym
    #   wn_words_synset[iWord].append(hyponym);

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get hyponyms
    print "---"
    for hyponym in wn.synset(wordDict.name()).hyponyms():
      print hyponym
      wn_words_synset[iWord].append(hyponym);

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # get description
    print "\ndefinition ------";
    # print wn.synset(bank.name()).definition();

    tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(wn.synset(wordDict.name()).definition()));
    print tagged_sent
    nouns = [word for word,pos in tagged_sent if (pos == 'NN' or pos == 'NNS'  or pos == 'JJ')];

    for noun in nouns:

      noun = wordnet_lemmatizer.lemmatize(noun, pos='n');

      if noun == None:
        continue

      # if noun != "bank" and noun != "sth" and noun not in wn_words_synset[iWord]:
      synsetsDictNoun = wn.synsets(noun, pos = "n");


      if len(synsetsDictNoun) > 0:
        synsetMax = synsetsDictNoun[0];
        p_max = 0;

        for synsetNoun in synsetsDictNoun:
          p = synsetNoun.path_similarity(synset_of_word);
          if p > p_max:
            p_max = p;
          # # synsetMax = synsetNoun

        print synsetMax
        if synsetMax not in wn_words_synset[iWord]:
          wn_words_synset[iWord].append(synsetMax);
        # if synsetsDictNoun[0] not in wn_words_synset[iWord]:
        #   # wn_words_synset[iWord].append(synsetsDictNoun[0]);



    tagged_sent = nltk.pos_tag(nltk.word_tokenize(wn.synset(wordDict.name()).definition()));
    nouns = [word for word,pos in tagged_sent if (pos == 'VB' or pos == 'VBD' or pos == 'VBN')];

    for noun in nouns:

      noun = wordnet_lemmatizer.lemmatize(noun, pos='n');

      if noun == None:
        continue

      # if noun != "bank" and noun != "sth" and noun not in wn_words_synset[iWord]:
      synsetsDictNoun = wn.synsets(noun, pos = "v");


      if len(synsetsDictNoun) > 0:
        synsetMax = synsetsDictNoun[0];
        p_max = 0;

        for synsetNoun in synsetsDictNoun:
          p = synsetNoun.path_similarity(synset_of_word);
          if p > p_max:
            p_max = p;
          # # synsetMax = synsetNoun

        print synsetMax
        if synsetMax not in wn_words_synset[iWord]:
          wn_words_synset[iWord].append(synsetMax);
        # if synsetsDictNoun[0] not in wn_words_synset[iWord]:
        #   wn_words_synset[iWord].append(synsetsDictNoun[0]);


  ########################################
  return wn_words_synset
  ########################################


