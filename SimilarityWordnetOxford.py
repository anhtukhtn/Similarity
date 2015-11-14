__author__ = 'tu'


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
def get_synsets_for_word(word_origin, wn_synsets_for_word_origin):

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


wn_words = wn.synsets("bank", pos = 'n');

wn_synsets_for_words = get_synsets_for_word("bank", wn_words);

print wn_synsets_for_words
