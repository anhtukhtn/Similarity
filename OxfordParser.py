__author__ = 'tu'

#!/usr/bin/env python
# -*- coding: utf-8 -

import xml.etree.ElementTree as ET
import csv
from collections import OrderedDict

def readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,level):
  oxfordNouns[runhd][str(iMeaning)] = OrderedDict();

  meaning = meanings[iMeaning]
  if level == 0:
    meaning = meanings;

  # get sd
  sd = meaning.find('.//sd');
  if sd != None:
    oxfordNouns[runhd][str(iMeaning)]['sd'] = sd.text;

  # get d
  d = meaning.find('.//d') or meaning.find('.//ud');
  if d != None:
    oxfordNouns[runhd][str(iMeaning)]['d'] = d.text;

  # get meaning
  vn = meaning.find('.//meaning');
  if vn == None:
    vn = meaning.find('.//txt_v_s_srf');
  if vn != None and vn.text != None:
    oxfordNouns[runhd][str(iMeaning)]['tv'] = vn.text;

  # get examples
  x = meaning.findall('.//x');
  for i in range(len(x)):
    oxfordNouns[runhd][str(iMeaning)]['x' + str(i)] = x[i].text;

  # get see also/async
  xh = meaning.findall('.//xh');
  for i in range(len(xh)):
    oxfordNouns[runhd][str(iMeaning)]['xh' + str(i)] = xh[i].text;


####################################################################################################
#
# @brief:   read nouns from oxford
#
# @ return: dictionary of nouns
#
def readOxfordNouns():

  oxfordNouns = OrderedDict();

  tree = ET.parse('OxfordXML/B_150107.xml');
  root = tree.getroot();

  # get all words
  for word in root.findall('entry'):

    # get word
    runhd = word.find('.//runhd');
    if runhd == None:
      continue

    print runhd.text

    runhd = runhd.text;

    if runhd == 'ballot box':
      adsf = 1;

    # get noun, verb of word
    findallpg = word.findall('.//p-g');
    if len(findallpg) != 0:
      for word_POS in findallpg:
        # get POS
        if word_POS.find('.//z_p_in_p-g') == None:
          continue

        POS = word_POS.find('.//z_p_in_p-g').text;

        if POS.strip() == 'noun':
          meanings = word_POS.findall('.//n-g');

          oxfordNouns[runhd] = OrderedDict();

          if len(meanings) != 0:
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
          else:
            meanings = word_POS.findall('.//d');
            if len(meanings)!= 0:
              readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
    else:
      POS = word.find('.//z_p');
      if POS != None:
        if POS.text.strip() == 'noun':

          oxfordNouns[runhd] = OrderedDict();
          meanings = word.findall('.//sd-g') or word.findall('.//n-g');

          if len(meanings) != 0:
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
          else:
            readContentOfWord(oxfordNouns,runhd,0,word,0);

    for word_2 in word.findall('.//entry'):

      # get word
      runhd = word_2.find('.//runhd');
      if runhd == None:
        continue

      runhd = runhd.text;

      if runhd == 'ballpark':
        adsf = 1;

      # get noun, verb of word
      findallpg = word_2.findall('.//p-g');
      if len(findallpg) != 0:
        for word_POS in findallpg:
          # get POS
          if word_POS.find('.//z_p_in_p-g') == None:
            continue

          POS = word_POS.find('.//z_p_in_p-g').text;

          if POS.strip() == 'noun':
            meanings = word_POS.findall('.//n-g');

            oxfordNouns[runhd] = OrderedDict();

            if len(meanings) != 0:
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            else:
              meanings = word_POS.findall('.//d')or word_POS.findall('.//ud');
              if len(meanings)!= 0:
                readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
      else:
        POS = word_2.find('.//z_p');
        if POS != None:
          if POS.text.strip() == 'noun':

            oxfordNouns[runhd] = OrderedDict();
            meanings = word_2.findall('.//sd-g') or word_2.findall('.//n-g');

            if len(meanings) != 0:
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            else:
              readContentOfWord(oxfordNouns,runhd,0,word_2,0);




  ########################################
  return oxfordNouns;
  ########################################

####################################################################################################
#
# @brief:   read nouns from oxford
#
# @ return: dictionary of nouns
#
def readOxfordVerbs():

  oxfordNouns = OrderedDict();

  tree = ET.parse('OxfordXML/B_150107.xml');
  root = tree.getroot();

  # get all words
  for word in root.findall('entry'):

    # get word
    runhd = word.find('.//runhd');
    if runhd == None:
      continue

    print runhd.text

    runhd = runhd.text;

    if runhd == 'ballot box':
      adsf = 1;

    # get noun, verb of word
    findallpg = word.findall('.//p-g');
    if len(findallpg) != 0:
      for word_POS in findallpg:
        # get POS
        if word_POS.find('.//z_p_in_p-g') == None:
          continue

        POS = word_POS.find('.//z_p_in_p-g').text;

        if POS.strip() == 'verb':
          meanings = word_POS.findall('.//n-g');

          oxfordNouns[runhd] = OrderedDict();

          if len(meanings) != 0:
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
          else:
            meanings = word_POS.findall('.//d');
            if len(meanings)!= 0:
              readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
    else:
      POS = word.find('.//z_p');
      if POS != None:
        if POS.text.strip() == 'verb':

          oxfordNouns[runhd] = OrderedDict();
          meanings = word.findall('.//sd-g') or word.findall('.//n-g');

          if len(meanings) != 0:
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
          else:
            readContentOfWord(oxfordNouns,runhd,0,word,0);

    for word_2 in word.findall('.//entry'):

      # get word
      runhd = word_2.find('.//runhd');
      if runhd == None:
        continue

      runhd = runhd.text;

      if runhd == 'ballpark':
        adsf = 1;

      # get noun, verb of word
      findallpg = word_2.findall('.//p-g');
      if len(findallpg) != 0:
        for word_POS in findallpg:
          # get POS
          if word_POS.find('.//z_p_in_p-g') == None:
            continue

          POS = word_POS.find('.//z_p_in_p-g').text;

          if POS.strip() == 'verb':
            meanings = word_POS.findall('.//n-g');

            oxfordNouns[runhd] = OrderedDict();

            if len(meanings) != 0:
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            else:
              meanings = word_POS.findall('.//d');
              if len(meanings)!= 0:
                readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
      else:
        POS = word_2.find('.//z_p');
        if POS != None:
          if POS.text.strip() == 'verb':

            oxfordNouns[runhd] = OrderedDict();
            meanings = word_2.findall('.//sd-g') or word_2.findall('.//n-g');

            if len(meanings) != 0:
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            else:
              readContentOfWord(oxfordNouns,runhd,0,word_2,0);

  ########################################
  return oxfordNouns;
  ########################################

####################################################################################################
#
# @brief:   write dictionary read from oxford to file
#
def writeDictFromOxfordToFile(filename, dict):

  file = open(filename, 'w');
  writer = csv.writer(file);

  for word in dict:
    # writer.writerow([word.encode('utf8')]);

    if dict[word] == None:
      continue

    for meaning in dict[word]:
      for key in dict[word][meaning]:
        if dict[word][meaning][key] == None:
          dict[word][meaning][key] = 'nn';
        writer.writerow([word.encode('utf8'),meaning,key,dict[word][meaning][key].encode('utf8')]);

  file.close();
  ########################################


# dict = readOxfordNouns();
# writeDictFromOxfordToFile("OxfordDict/b.csv",dict);
