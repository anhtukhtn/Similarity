#!/usr/bin/env python
# -*- coding: utf-8 -*-

import OxfordParser

####################################################################################################
#
# @return: return dict of words: dict["bank"]: array of bank sysets. dict["bank"][0]["gloss"],dict["bank"][0]["vie"]
#
def readCoFile(fileName):

  p_dict_words = {};

  f = open(fileName, "r");
  data = f.read();

  # - - - - - - - - - - - - - - - - - - - - - - - - - - - paragraph
  # No: 7988_1
  # KEY: b-complex vitamin
  # POS: noun
  # RELATED_ENG: B-complex vitamin, B complex, vitamin B complex, vitamin B, B vitamin, B, b vitamins
  # RELATED_VIE: vitamin nhóm B
  # GLOSS_ENG: originally thought to be a single vitamin but now separated into several B vitamins
  # GLOSS_VIE: ban đầu được cho là một chất vitamin nhưng bây giờ tách ra thành một số vitamin B
  # EX_ENG:
  # EX_VIE:

  paragraphs = data.split("\n\n");

  # read each word and add to return dict
  for paragraph in paragraphs:
    print paragraph
    print("\n")

    # read word
    dictSynsetLaconet = {};
    lines = paragraph.split("\n")
    for line in lines:
      if line == "":
        continue
      if len(line.split(": ")) != 2:
        continue
      (key, value) = line.split(": ");
      dictSynsetLaconet[key] = value;

    # add word to return value
    (_,indexNo) = dictSynsetLaconet["No"].split("_");
    if indexNo == "1":
      p_dict_words[dictSynsetLaconet["KEY"]] = [];

    if not dictSynsetLaconet.has_key("GLOSS_ENG") or not dictSynsetLaconet.has_key("RELATED_VIE"):
      continue

    dicSynset = {};
    dicSynset["gloss"] = dictSynsetLaconet["GLOSS_ENG"];
    dicSynset["vie"] = dictSynsetLaconet["RELATED_VIE"];

    p_dict_words[dictSynsetLaconet["KEY"]].append(dicSynset);

  # print p_dict_words
  return p_dict_words;

def compare_oxford_co():

 dict_words_co = readCoFile("WN/laconet_B.txt")

 dict_words_oxford = OxfordParser.readOxfordNouns();

 for word in dict_words_oxford:

   if dict_words_co.has_key(word):
     for synset_co in dict_words_co[word]:
       for synset_oxford in dict_words_oxford[word]:
         if word == "bank":
           print synset_co["vie"]
           print synset_oxford[word]

compare_oxford_co();
