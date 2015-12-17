#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ReadVietNet
import OxfordParser
import FileProcess
import csv
from nltk.corpus import wordnet as wn
from nltk.metrics import jaccard_distance

def compareVietNetAndOxford(dict_VietNet, dict_Oxford):

  for WORD in dict_Oxford:

    wn_words = wn.synsets(WORD, pos = 'n');
    if wn_words == None:
      continue

    # if WORD != 'bank':
    #   continue;

    if dict_VietNet.has_key(WORD):

      arr_VietNet = dict_VietNet[WORD];
      arr_Oxford = dict_Oxford[WORD]

      matrix_similarity = [[0 for x in range(len(arr_Oxford))] for x in range(len(wn_words))];


      for iWn in range(len(wn_words)):

        definitionWn = wn.synset(wn_words[iWn].name()).definition();

        vietNet = {};
        for iVietNet in arr_VietNet:
          if arr_VietNet[iVietNet]["d"] == definitionWn:
            vietNet = arr_VietNet[iVietNet];
            break

        if not vietNet.has_key("tv"):
          vietNet["tv"] = "";

        viet_net_tv = vietNet["tv"]

        for iOxford in range(len(arr_Oxford)):
          oxford = arr_Oxford[str(iOxford)];

          vietNet_tv = viet_net_tv

          if not oxford.has_key("tv"):
            continue
          oxford_tv = oxford["tv"].encode("utf-8")

          vietNet_tv.replace(";","")
          oxford_tv = oxford_tv.replace(";","")
          oxford_tv = oxford_tv.replace(",","")
          oxford_tv = oxford_tv.replace("/"," ")

          arr_tv_oxford = set(oxford_tv.split(" "))
          arr_tv_vietnet = set(vietNet_tv.split(" "))

          jaccard = jaccard_distance(arr_tv_oxford,arr_tv_vietnet);
          print arr_tv_vietnet
          print arr_tv_oxford
          print jaccard
          matrix_similarity[iWn][iOxford] = 0;
          if jaccard < 0.9:
            matrix_similarity[iWn][iOxford] = 1;

        matrix_similarity[iWn].insert(0,viet_net_tv + "<>" + definitionWn.encode("utf-8"));

      print matrix_similarity
        # - - - - - - - - - - - - - - - - - - - - - - - - -
      # col
      # for i in range(len(dict_VietNet[WORD])):
      #   matrix_similarity[i].insert(0,dict_VietNet[WORD][i]["tv"] + "<>" + dict_VietNet[WORD][i]["d"]);

      # - - - - - - - - - - - - - - - - - - - - - - - - -
      # row
      arrRowDict = [];
      arrRowDict.append(WORD);
      for i in range(len(dict_Oxford[WORD])):
        if not dict_Oxford[WORD][str(i)].has_key("tv"):
          dict_Oxford[WORD][str(i)]["tv"] = "-";
        if not dict_Oxford[WORD][str(i)].has_key("d"):
          dict_Oxford[WORD][str(i)]["d"] = "-";
        if dict_Oxford[WORD][str(i)]["d"] == None:
          dict_Oxford[WORD][str(i)]["d"] = "-";

        arrRowDict.append(dict_Oxford[WORD][str(i)]["tv"].encode("utf-8") + "<>" + dict_Oxford[WORD][str(i)]["d"].encode("utf-8"));

      FileProcess.append_to_excel_file("Results/parameters/VN_Ox/"+"compare_VN_Ox.csv",arrRowDict,matrix_similarity)

def readResultFile(fileName):

  dict = {};

  firstline = 1;

  f = open(fileName,'r');
  reader = csv.reader(f);
  word = "";
  length_of_col = 0;
  for row in reader:

    if firstline == 2 and len(row)!=0:
      row.pop(0)
      arr_temp = row;
      dict[word].append(arr_temp);

    # get word for key in dict
    if firstline == 1 and len(row)!=0:
      word = row[0];
      dict[word] = [];
      print "\n"
      firstline = 2;

    # end matrix of a word
    if len(row)==0:
      firstline = 1;
      print word
      print dict[word]

  ########################################
  return dict





  ########################################

# readResultFile("Results/parameters/VN_Ox/"+"compare_VN_Ox.csv");

dict_VN = ReadVietNet.readVietNetFile()
dict_Ox = OxfordParser.readOxfordNouns();
compareVietNetAndOxford(dict_VN,dict_Ox)