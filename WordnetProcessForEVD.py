from nltk.corpus import wordnet as wn
import POSWrapper
import nltk


def read_nouns():
  dict_wn = {}
  for synset in list(wn.all_synsets('n')):
    lemmas =  [str(lemma.name()) for lemma in synset.lemmas()]
    dict_wn[synset.name()] = lemmas

      # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      # # get hypernyms
      # print "\nhypernyms ------";
    for hypernym in synset.hypernyms():
      for lemma in wn.synset(hypernym.name()).lemmas():
        lemma_name = lemma.name();
        dict_wn[synset.name()].append(lemma_name)

      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      # get hyponyms
    for hyponym in synset.hyponyms():
      for lemma in wn.synset(hyponym.name()).lemmas():
        lemma_name = lemma.name();
        dict_wn[synset.name()].append(lemma_name)
      # - - - - - - - - - - - - - - - - - - - - - - - - - - -
      # get description
      # print wn.synset(bank.name()).definition();

    for meronym in synset.part_meronyms():
      for lemma in wn.synset(meronym.name()).lemmas():
        lemma_name = lemma.name();
        dict_wn[synset.name()].append(lemma_name)

    for holonym in synset.member_holonyms():
      for lemma in wn.synset(holonym.name()).lemmas():
        lemma_name = lemma.name();
        dict_wn[synset.name()].append(lemma_name)


    tagged_sent = POSWrapper.pos_tag(nltk.word_tokenize(synset.definition()));
    nouns = [word for word,pos in tagged_sent if pos == 'NN'];

    for noun in nouns:
      dict_wn[synset.name()].append(noun)

  return dict_wn


#dict_wn = read_nouns()
#print dict_wn
